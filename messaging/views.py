# /home/MiguelAeTxio/CampuStudiOnline/messaging/views.py
import json
import logging
import traceback
import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models, transaction
from django.db.models import Count, Max, OuterRef, Q, Subquery
from django.db.models.functions import Coalesce
from django.http import (
    Http404,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import TemplateView

from contents.models import Annotation, ContentCopy
from users.models import UserProfile

from .models import (
    Browser,
    DirectChatSession,
    DirectMessage,
    PushEndpoint,
    SharedContent,
    UserSubscription,
)
from .tasks import send_push_notification_task

User = get_user_model()
logger = logging.getLogger(__name__)


# --- HELPER FUNCTIONS ---
def clean_message_content(content):
    if isinstance(content, dict):
        return content
    if isinstance(content, str):
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {}
    return {}


def serialize_shared_content(content_obj):
    if not content_obj:
        return None
    return {
        "id": content_obj.id,
        "title_snapshot": content_obj.title_snapshot,
        "description_snapshot": content_obj.description_snapshot,
        "url_snapshot": content_obj.url_snapshot,
        "shared_at": content_obj.shared_at.isoformat(),
    }


def serialize_message_list(messages):
    serialized_messages = []
    for msg in messages:
        reply_to_context = None
        if msg.reply_to and not msg.reply_to.is_deleted:
            reply_to_context = {
                "id": msg.reply_to.id,
                "content": clean_message_content(msg.reply_to.content),
                "sender_username": msg.reply_to.sender.username,
            }
        serialized_messages.append(
            {
                "message_id": msg.id,
                "sender_id": msg.sender_id,
                "sender_username": msg.sender.username,
                "content": clean_message_content(msg.content),
                "timestamp": msg.timestamp.isoformat(),
                "is_deleted": msg.is_deleted,
                "is_edited": msg.is_edited,
                "edited_at": msg.edited_at.isoformat() if msg.edited_at else None,
                "reply_to": reply_to_context,
                "shared_content": serialize_shared_content(
                    getattr(msg, "shared_content", None)
                ),
            }
        )
    return serialized_messages


# --- END HELPER FUNCTIONS ---


@login_required
def conversation_list(request):
    user = request.user
    search_query = request.GET.get("q", "").strip()
    search_results = None
    if search_query:
        query = (
            Q(username__icontains=search_query)
            | Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
        )
        search_results = (
            User.objects.filter(query)
            .exclude(pk=user.pk)
            .select_related("userprofile")
            .distinct()
        )

    last_message_subquery = (
        DirectMessage.objects.filter(session=OuterRef("pk"))
        .order_by("-timestamp")
        .values("id")[:1]
    )

    unread_messages_subquery = (
        DirectMessage.objects.filter(session=OuterRef("pk"), is_read=False)
        .exclude(sender=user)
        .values("session")
        .annotate(count=Count("id"))
        .values("count")
    )

    hide_conditions = Q(user1=user, is_hidden_by_user1=True) | Q(
        user2=user, is_hidden_by_user2=True
    )

    chat_sessions_qs = (
        DirectChatSession.objects.filter(Q(user1=user) | Q(user2=user))
        .exclude(hide_conditions)
        .annotate(
            last_message_id=Subquery(last_message_subquery),
            unread_count=Coalesce(
                Subquery(unread_messages_subquery, output_field=models.IntegerField()),
                0,
            ),
        )
        .select_related("user1", "user2")
        .order_by("-updated_at")
    )

    last_messages_ids = [
        s.last_message_id for s in chat_sessions_qs if s.last_message_id
    ]
    last_messages = {
        msg.session_id: msg
        for msg in DirectMessage.objects.filter(id__in=last_messages_ids).select_related(
            "sender", "shared_content"
        )
    }

    sessions_with_details = []
    for session in chat_sessions_qs:
        last_message = last_messages.get(session.id)
        other_user_obj = session.get_other_user(user)
        encrypted_payload_json = "{}"
        if (
            last_message
            and not last_message.is_deleted
            and isinstance(last_message.content, dict)
        ):
            encrypted_payload_json = json.dumps(last_message.content)

        if other_user_obj:
            sessions_with_details.append(
                {
                    "session_id": session.id,
                    "other_user": other_user_obj,
                    "last_message": last_message,
                    "encrypted_payload_json": encrypted_payload_json,
                    "updated_at": session.updated_at,
                    "unread_count": session.unread_count,
                    "detail_url": reverse(
                        "messaging:conversation_detail",
                        kwargs={"username": other_user_obj.username},
                    ),
                }
            )

    context = {
        "chat_sessions": sessions_with_details,
        "search_results": search_results,
        "search_query": search_query,
        "show_tour": True,
    }
    return render(request, "messaging/conversation_list.html", context)


@login_required
def start_chat(request, username):
    other_user = get_object_or_404(User, username=username)
    if other_user == request.user:
        return redirect("messaging:conversation_list")
    return redirect("messaging:conversation_detail", username=other_user.username)


@login_required
def conversation_detail(request, username):
    current_user = request.user
    try:
        other_user = User.objects.select_related("userprofile").get(username=username)
    except User.DoesNotExist:
        raise Http404("User not found.")

    other_user_profile, _ = UserProfile.objects.get_or_create(user=other_user)
    current_user_profile = request.user.userprofile

    if current_user == other_user:
        return redirect("messaging:conversation_list")

    user1, user2 = (
        (current_user, other_user)
        if current_user.id < other_user.id
        else (other_user, current_user)
    )
    session, created = DirectChatSession.objects.get_or_create(user1=user1, user2=user2)

    if created:
        session.updated_at = timezone.now()
        session.save(update_fields=["updated_at"])

    chat_data = {
        "other_username": other_user.username,
        "other_user_id": other_user.id,
        "other_user_public_key": other_user_profile.public_key,
        "current_user_id": current_user.id,
        "current_username": current_user.username,
        "chat_session_id": session.id,
        "user_has_public_key": bool(current_user_profile.public_key),
        "send_message_url": reverse(
            "messaging:api_send_message", kwargs={"username": other_user.username}
        ),
        "fetch_messages_url": reverse(
            "messaging:api_fetch_messages", kwargs={"username": other_user.username}
        ),
        "message_action_url": reverse(
            "messaging:api_message_action", kwargs={"username": other_user.username}
        ),
        "share_content_url": reverse(
            "messaging:api_share_content", kwargs={"username": other_user.username}
        ),
    }

    is_blocked_by_you = current_user_profile.blocked_users.filter(
        id=other_user.id
    ).exists()
    are_you_blocked = other_user_profile.blocked_users.filter(
        id=current_user.id
    ).exists()

    context = {
        "other_user": other_user,
        "chat_data": chat_data,
        "is_blocked": is_blocked_by_you,
        "are_you_blocked": are_you_blocked,
    }
    return render(request, "messaging/conversation_detail.html", context)


@login_required
@require_POST
def send_message(request, username):
    try:
        data = json.loads(request.body)
        encrypted_payload = data.get("encrypted_payload")
        reply_to_id = data.get("reply_to_id")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON.")

    if not encrypted_payload:
        return HttpResponseBadRequest("Missing 'encrypted_payload'.")

    sender = request.user
    other_user = get_object_or_404(User, username=username)
    user1, user2 = (
        (sender, other_user) if sender.id < other_user.id else (other_user, sender)
    )
    session = get_object_or_404(DirectChatSession, user1=user1, user2=user2)

    reply_to_message = None
    if reply_to_id:
        try:
            reply_to_message = DirectMessage.objects.get(
                id=reply_to_id, session=session
            )
        except DirectMessage.DoesNotExist:
            pass

    new_message = DirectMessage.objects.create(
        session=session,
        sender=sender,
        content=encrypted_payload,
        reply_to=reply_to_message,
    )
    session.save(update_fields=["updated_at"])

    send_push_notification_task.delay(
        recipient_id=other_user.id,
        sender_username=sender.username,
        encrypted_payload=encrypted_payload,
    )

    message_data = serialize_message_list([new_message])[0]
    return JsonResponse({"status": "success", "message": message_data})


@login_required
@require_GET
def fetch_messages(request, username):
    user = request.user
    other_user = get_object_or_404(User, username=username)
    user1, user2 = (user, other_user) if user.id < other_user.id else (other_user, user)
    session = get_object_or_404(DirectChatSession, user1=user1, user2=user2)

    since_message_id = request.GET.get("since_message_id")
    before_message_id = request.GET.get("before_message_id")

    queryset = (
        DirectMessage.objects.filter(session=session)
        .select_related("sender", "reply_to", "reply_to__sender", "shared_content")
        .order_by("-timestamp")
    )

    if since_message_id:
        try:
            last_known_message = DirectMessage.objects.only("timestamp").get(
                id=since_message_id
            )
            queryset = queryset.filter(timestamp__gt=last_known_message.timestamp)
            DirectMessage.objects.filter(
                session=session, sender=other_user, is_read=False
            ).update(is_read=True, read_at=timezone.now())
        except DirectMessage.DoesNotExist:
            pass
    elif before_message_id:
        try:
            first_known_message = DirectMessage.objects.only("timestamp").get(
                id=before_message_id
            )
            queryset = queryset.filter(timestamp__lt=first_known_message.timestamp)
        except DirectMessage.DoesNotExist:
            return JsonResponse({"messages": []})

    messages = list(queryset[:50])[::-1]
    return JsonResponse({"messages": serialize_message_list(messages)})


@login_required
@require_POST
def message_action(request, username):
    try:
        data = json.loads(request.body)
        action = data.get("action")
        message_id = data.get("message_id")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON.")

    if not all([action, message_id]):
        return HttpResponseBadRequest("Missing 'action' or 'message_id'.")

    try:
        message = DirectMessage.objects.select_related(
            "sender", "reply_to", "reply_to__sender", "shared_content"
        ).get(id=message_id, sender=request.user)
    except DirectMessage.DoesNotExist:
        return HttpResponseForbidden("You cannot modify this message.")

    if action == "delete":
        message.is_deleted = True
        message.deleted_at = timezone.now()
        message.save(update_fields=["is_deleted", "deleted_at"])
        return JsonResponse({"status": "success", "message": "Message deleted."})

    elif action == "edit":
        new_payload = data.get("new_encrypted_payload")
        if not new_payload:
            return HttpResponseBadRequest("Missing 'new_encrypted_payload' for edit.")

        message.content = new_payload
        message.is_edited = True
        message.edited_at = timezone.now()
        message.save(update_fields=["content", "is_edited", "edited_at"])

        serialized_message = serialize_message_list([message])[0]

        return JsonResponse({"status": "success", "message": serialized_message})

    return HttpResponseBadRequest("Invalid action.")


@login_required
@require_POST
def send_invitation(request, username):
    sender = request.user
    recipient = get_object_or_404(User, username=username)
    if hasattr(recipient, "userprofile") and recipient.userprofile.public_key:
        return JsonResponse(
            {
                "status": "error",
                "message": "This user is already active in messaging.",
            },
            status=400,
        )
    if not recipient.email:
        return JsonResponse(
            {
                "status": "error",
                "message": "This user does not have a registered email address.",
            },
            status=400,
        )
    subject = f"{sender.username} wants to chat with you on CampuStudiOnline!"
    chat_url = request.build_absolute_uri(reverse("messaging:conversation_list"))
    context = {
        "recipient_name": recipient.get_full_name() or recipient.username,
        "sender_name": sender.get_full_name() or sender.username,
        "chat_url": chat_url,
    }
    message_body = render_to_string("messaging/email/invitation_email.txt", context)
    html_message = render_to_string("messaging/email/invitation_email.html", context)
    try:
        send_mail(
            subject,
            message_body,
            settings.DEFAULT_FROM_EMAIL,
            [recipient.email],
            fail_silently=False,
            html_message=html_message,
        )
        return JsonResponse(
            {"status": "success", "message": "Invitation sent successfully."}
        )
    except Exception as e:
        logger.error(f"Error sending invitation email: {e}", exc_info=True)
        return JsonResponse(
            {"status": "error", "message": "There was a problem sending the email."},
            status=500,
        )


@login_required
@require_POST
def hide_conversation(request, session_id):
    session = get_object_or_404(DirectChatSession, pk=session_id)
    user = request.user
    if user != session.user1 and user != session.user2:
        return HttpResponseForbidden("You do not have permission to perform this action.")
    if session.user1 == user:
        session.is_hidden_by_user1 = True
    elif session.user2 == user:
        session.is_hidden_by_user2 = True
    session.save()
    return redirect("messaging:conversation_list")


@login_required
@require_POST
def save_webpush_subscription(request):
    logger.info("--- START save_webpush_subscription ---")
    logger.info(f"User: {request.user.username}, Method: {request.method}")
    logger.info(f"Request body (raw): {request.body}")

    try:
        logger.info("Attempting to parse JSON...")
        data = json.loads(request.body)
        logger.info(f"JSON parsed successfully: {data}")

        browser_uuid_str = data.get("browser_uuid")
        user_agent_str = data.get("user_agent")
        subscription_data = data.get("subscription_data")

        if not all([browser_uuid_str, subscription_data]):
            logger.error("Missing key data (browser_uuid, subscription_data).")
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Missing key data (browser_uuid, subscription_data).",
                },
                status=400,
            )

        endpoint = subscription_data.get("endpoint")
        keys = subscription_data.get("keys")
        if not all([endpoint, keys]):
            logger.error("Incomplete subscription data.")
            return JsonResponse(
                {"status": "error", "message": "Incomplete subscription data."},
                status=400,
            )

        try:
            browser_uuid = uuid.UUID(browser_uuid_str)
            logger.info(f"browser_uuid validated: {browser_uuid}")
        except (ValueError, TypeError):
            logger.error(f"Invalid UUID: {browser_uuid_str}")
            return JsonResponse(
                {"status": "error", "message": "The browser_uuid is not a valid UUID."},
                status=400,
            )

        with transaction.atomic():
            logger.info(f"Getting or creating Browser with UUID: {browser_uuid}")
            browser, created_browser = Browser.objects.get_or_create(
                uuid=browser_uuid, defaults={"user_agent": user_agent_str or ""}
            )
            logger.info(f"Browser: {browser.uuid}, Created: {created_browser}")

            logger.info(
                f"Updating or creating PushEndpoint for Browser: {browser.uuid}"
            )
            endpoint_obj, created_endpoint = PushEndpoint.objects.update_or_create(
                browser=browser, defaults={"endpoint": endpoint, "keys": keys}
            )
            logger.info(
                f"PushEndpoint for Browser: {browser.uuid}, Created: {created_endpoint}"
            )

            device_name = "Unknown Device"
            if hasattr(request, "user_agent") and request.user_agent:
                ua = request.user_agent
                device_name = f"{ua.browser.family} on {ua.os.family}"
            logger.info(
                f"Updating or creating UserSubscription for User: {request.user.username} and Browser: {browser.uuid}"
            )
            subscription_obj, created_subscription = (
                UserSubscription.objects.update_or_create(
                    user=request.user,
                    browser=browser,
                    defaults={"is_active": True, "device_name": device_name},
                )
            )
            logger.info(
                f"UserSubscription for User: {request.user.username}, Created: {created_subscription}"
            )

        logger.info("Sending success response.")
        logger.info("--- END save_webpush_subscription ---")
        return JsonResponse(
            {"status": "success", "message": "Subscription registered successfully."}
        )

    except json.JSONDecodeError:
        logger.error(
            "JSONDecodeError: The request body is not valid JSON.",
            exc_info=True,
        )
        return JsonResponse(
            {"status": "error", "message": "Invalid JSON."}, status=400
        )
    except Exception as e:
        logger.error(f"Unexpected error in save_webpush_subscription", exc_info=True)
        return JsonResponse(
            {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
            status=500,
        )


class ServiceWorkerView(TemplateView):
    template_name = "service-worker.js"
    content_type = "application/javascript"


@login_required
@require_POST
def save_public_key(request):
    try:
        user_profile = request.user.userprofile
        user_profile.public_key = request.POST.get("public_key")
        user_profile.encrypted_private_key = request.POST.get("encrypted_private_key")
        user_profile.save(update_fields=["public_key", "encrypted_private_key"])
        return JsonResponse({"status": "success", "message": "Keys saved."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@login_required
def get_crypto_keys(request):
    try:
        profile = request.user.userprofile
        if (
            profile.public_key
            and profile.encrypted_private_key
            and profile.encryption_salt
        ):
            return JsonResponse(
                {
                    "status": "success",
                    "public_key": profile.public_key,
                    "encrypted_private_key": profile.encrypted_private_key,
                    "encryption_salt": profile.encryption_salt,
                }
            )
        else:
            return JsonResponse({"status": "not_found"})
    except UserProfile.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Profile not found."}, status=404
        )


@login_required
@require_GET
def get_study_copies(request):
    user_copies = (
        ContentCopy.objects.filter(user=request.user)
        .select_related("original_content")
        .order_by("-updated_at")
    )
    data_to_send = [{"id": copy.id, "title": str(copy)} for copy in user_copies]
    return JsonResponse({"copies": data_to_send})


@login_required
@require_GET
def get_study_copy_details(request, copy_id):
    try:
        copy = ContentCopy.objects.select_related("original_content").get(
            pk=copy_id, user=request.user
        )
    except ContentCopy.DoesNotExist:
        return JsonResponse(
            {"error": "Copy not found or does not belong to you."}, status=404
        )
    annotations = copy.annotations.all().order_by("created_at")
    annotations_data = [
        {
            "id": ann.id,
            "type": ann.get_annotation_type_display(),
            "content": ann.content,
        }
        for ann in annotations
    ]
    copy_data = {"id": copy.id, "title": str(copy), "is_public": copy.is_public}
    return JsonResponse({"copy": copy_data, "annotations": annotations_data})


@login_required
@require_POST
def share_content(request, username):
    try:
        sender = request.user
        other_user = get_object_or_404(User, username=username)
        data = json.loads(request.body)
        content_type_str = data.get("content_type")
        content_id = data.get("content_id")
        copy_id = data.get("copy_id")

        if not all([content_type_str, content_id, copy_id]):
            return JsonResponse(
                {"status": "error", "message": "Missing data."}, status=400
            )

        parent_copy = get_object_or_404(ContentCopy, pk=copy_id, user=sender)

        if not parent_copy.is_public:
            parent_copy.is_public = True
            parent_copy.save(update_fields=["is_public"])

        shared_object, title_snapshot, description_snapshot = None, "", ""
        if content_type_str == "copia":
            shared_object = parent_copy
            title_snapshot = f"Document: {shared_object.original_content.title}"
            description_snapshot = f"Shared by {sender.username}."
        elif content_type_str == "anotacion":
            shared_object = get_object_or_404(
                Annotation, pk=content_id, copy=parent_copy
            )
            title_snapshot = (
                f"{shared_object.get_annotation_type_display()} in: "
                f"{parent_copy.original_content.title}"
            )
            description_snapshot = shared_object.content[:150]
        else:
            return JsonResponse(
                {"status": "error", "message": "Invalid content type."},
                status=400,
            )

        content_type_model = ContentType.objects.get_for_model(shared_object)
        shared_content_obj = SharedContent.objects.create(
            content_type=content_type_model,
            object_id=shared_object.pk,
            title_snapshot=title_snapshot,
            description_snapshot=description_snapshot,
            url_snapshot=request.build_absolute_uri(shared_object.get_absolute_url()),
            shared_by=sender,
        )
        user1, user2 = (
            (sender, other_user) if sender.id < other_user.id else (other_user, sender)
        )
        session, _ = DirectChatSession.objects.get_or_create(user1=user1, user2=user2)

        new_message = DirectMessage.objects.create(
            session=session,
            sender=sender,
            content={},
            shared_content=shared_content_obj,
        )
        session.save(update_fields=["updated_at"])

        notification_payload = {
            "title": f"{sender.username} has shared something with you",
            "body": title_snapshot,
        }
        send_push_notification_task.delay(
            recipient_id=other_user.id,
            sender_username=sender.username,
            encrypted_payload=notification_payload,
        )

        message_data = serialize_message_list([new_message])[0]

        return JsonResponse(
            {
                "status": "success",
                "message": "Content shared.",
                "message_data": message_data,
            }
        )

    except Exception as e:
        logger.error(f"ERROR CAUGHT IN share_content_view", exc_info=True)
        raise e
