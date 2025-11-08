# /home/MiguelAeTxio/CampuStudiOnline/chat/views.py
import json
import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from .forms import ChatRoomForm
from .models import ChatMessage, ChatRoom, RoomMembership

logger = logging.getLogger(__name__)

# --- INICIO: Funciones Auxiliares para la nueva API de Polling ---


def _get_enriched_user_list_for_room(room):
    User = get_user_model()
    creator_username = room.creator.username if room.creator else None
    base_user_details = {}

    if room.is_platform_default:
        all_users = User.objects.filter(is_active=True).values("id", "username")
        memberships = {
            rm.user.username: rm
            for rm in RoomMembership.objects.filter(room=room).select_related("user")
        }
        for user_data in all_users:
            username = user_data["username"]
            membership = memberships.get(username)
            role = RoomMembership.ROLE_MEMBER
            if username == creator_username:
                role = "creator"
            elif membership:
                role = membership.role
            is_silenced = membership.is_silenced if membership else False
            base_user_details[username] = {
                "is_silenced": is_silenced,
                "role": role,
                "user_id": user_data["id"],
            }
    else:
        memberships = RoomMembership.objects.filter(
            room=room, status=RoomMembership.STATUS_MEMBER
        ).select_related("user")
        for m in memberships:
            if m.user:
                role = m.role
                if m.user.username == creator_username:
                    role = "creator"
                base_user_details[m.user.username] = {
                    "is_silenced": m.is_silenced,
                    "role": role,
                    "user_id": m.user.id,
                }

    def sort_key(user_tuple):
        username, details = user_tuple
        role, username_lower = details["role"], username.lower()
        if role == "creator":
            return (0, username_lower)
        if role == RoomMembership.ROLE_MODERATOR:
            return (1, username_lower)
        return (2, username_lower)

    sorted_user_items = sorted(base_user_details.items(), key=sort_key)
    return [
        {
            "username": u,
            "user_id": d["user_id"],
            "is_silenced_in_channel": d["is_silenced"],
            "role": d["role"],
        }
        for u, d in sorted_user_items
    ]


@login_required
@require_POST
def send_chat_message_api(request, room_slug):
    room = get_object_or_404(ChatRoom, slug=room_slug)
    user = request.user
    membership = RoomMembership.objects.filter(user=user, room=room).first()
    if room.is_private and (
        not membership or membership.status != RoomMembership.STATUS_MEMBER
    ):
        return JsonResponse(
            {"status": "error", "message": "No eres miembro de esta sala privada."},
            status=403,
        )
    if membership and membership.is_silenced:
        return JsonResponse(
            {"status": "error", "message": "Has sido silenciado en esta sala."},
            status=403,
        )
    try:
        data = json.loads(request.body)
        message_content = data.get("message")
        if (
            not message_content
            or not isinstance(message_content, str)
            or not message_content.strip()
        ):
            return JsonResponse(
                {"status": "error", "message": "El mensaje no puede estar vacío."},
                status=400,
            )
    except json.JSONDecodeError:
        return JsonResponse(
            {"status": "error", "message": "Cuerpo de la petición inválido."},
            status=400,
        )
    try:
        ChatMessage.objects.create(
            room=room,
            sender=user,
            sender_username_display=user.username,
            content=message_content,
        )
        room.updated_at = timezone.now()
        room.save(update_fields=["updated_at"])
        return JsonResponse({"status": "success", "message": "Mensaje enviado."})
    except Exception as e:
        logger.error(
            f"API: ERROR al guardar mensaje para sala '{room.slug}': {e}", exc_info=True
        )
        return JsonResponse(
            {"status": "error", "message": "Error interno del servidor."}, status=500
        )


@login_required
@require_GET
def get_chat_updates_api(request, room_slug):
    room = get_object_or_404(ChatRoom, slug=room_slug)
    user = request.user
    last_message_id = int(request.GET.get("last_message_id", "0"))
    if (
        room.is_private
        and not RoomMembership.objects.filter(
            user=user, room=room, status=RoomMembership.STATUS_MEMBER
        ).exists()
    ):
        return JsonResponse(
            {"status": "error", "message": "No tienes permiso para ver esta sala."},
            status=403,
        )

    new_messages_query = (
        ChatMessage.objects.filter(room=room, id__gt=last_message_id)
        .select_related("sender")
        .order_by("timestamp")
    )
    member_roles_map = {
        m.user.username: m.role
        for m in RoomMembership.objects.filter(room=room).select_related("user")
    }
    creator_username = room.creator.username if room.creator else None

    messages_data = []
    for msg in new_messages_query:
        sender_username = msg.sender_username_display
        role = member_roles_map.get(sender_username, RoomMembership.ROLE_MEMBER)
        if sender_username == creator_username:
            role = "creator"
        messages_data.append(
            {
                "message_id": msg.id,
                "sender_username": sender_username,
                "message": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "role": role,
                "is_deleted": msg.is_deleted_by_moderator,
            }
        )

    return JsonResponse(
        {
            "status": "success",
            "messages": messages_data,
            "users_enriched": _get_enriched_user_list_for_room(room),
        }
    )


# --- FIN: Funciones para la nueva API de Polling ---


def chat_index(request):
    general_room = ChatRoom.objects.filter(is_platform_default=True).first()
    other_public_rooms_query = ChatRoom.objects.filter(
        is_private=False, is_platform_default=False
    )
    all_private_rooms_query = ChatRoom.objects.filter(is_private=True).exclude(
        academic_chat_link__isnull=False
    )
    user_memberships_map = {}
    if request.user.is_authenticated:
        memberships = RoomMembership.objects.filter(user=request.user).select_related(
            "room"
        )
        for m in memberships:
            user_memberships_map[m.room_id] = m
    my_joined_public_rooms, other_public_rooms_to_join = [], []
    for room in other_public_rooms_query:
        membership = user_memberships_map.get(room.id)
        if membership and membership.status == RoomMembership.STATUS_MEMBER:
            my_joined_public_rooms.append(room)
        else:
            other_public_rooms_to_join.append(room)
    my_active_private_rooms, other_private_rooms_info = [], []
    for room in all_private_rooms_query:
        user_room_status_key = "can_request_to_join"
        user_room_membership_obj = None
        is_actively_a_member = False
        if request.user.is_authenticated:
            membership = user_memberships_map.get(room.id)
            if membership:
                user_room_membership_obj = membership
                if membership.status == RoomMembership.STATUS_MEMBER:
                    user_room_status_key = "is_member"
                    my_active_private_rooms.append(room)
                    is_actively_a_member = True
                elif membership.status == RoomMembership.STATUS_PENDING:
                    user_room_status_key = "request_is_pending"
                elif membership.status == RoomMembership.STATUS_REJECTED:
                    user_room_status_key = "request_was_rejected"
        if not is_actively_a_member:
            final_status_key_for_other = (
                "login_to_interact"
                if not request.user.is_authenticated and room.is_private
                else user_room_status_key
            )
            other_private_rooms_info.append(
                {
                    "room": room,
                    "user_room_status_key": final_status_key_for_other,
                    "membership": user_room_membership_obj,
                }
            )
    context = {
        "general_room": general_room,
        "my_joined_public_rooms": my_joined_public_rooms,
        "other_public_rooms_to_join": other_public_rooms_to_join,
        "my_active_private_rooms": my_active_private_rooms,
        "other_private_rooms_info": other_private_rooms_info,
        "user_is_authenticated": request.user.is_authenticated,
        "all_private_rooms_exist": all_private_rooms_query.exists(),
        "show_tour": True,
    }
    return render(request, "chat/index.html", context)


@login_required
def create_room(request):
    if request.method == "POST":
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            new_room = form.save(commit=False)
            new_room.creator = request.user
            new_room.save()
            RoomMembership.objects.create(
                user=request.user,
                room=new_room,
                status=RoomMembership.STATUS_MEMBER,
                role=RoomMembership.ROLE_MEMBER,
            )
            messages.success(request, f"¡Sala '{new_room.name}' creada con éxito!")
            return redirect(reverse("chat:room_detail", kwargs={"room_slug": new_room.slug}))
    else:
        form = ChatRoomForm()
    return render(
        request,
        "chat/create_room.html",
        {"form": form, "page_title": "Crear Nueva Sala de Chat"},
    )


@login_required
def room_detail(request, room_slug):
    try:
        chat_room = ChatRoom.objects.select_related("creator").get(slug=room_slug)
    except ChatRoom.DoesNotExist:
        raise Http404("La sala de chat especificada no existe.")

    user = request.user
    membership = RoomMembership.objects.filter(user=user, room=chat_room).first()

    if chat_room.is_private:
        if not membership or membership.status != RoomMembership.STATUS_MEMBER:
            messages.error(
                request,
                f"No tienes permiso para acceder a la sala privada '{chat_room.name}'.",
            )
            return redirect("chat:index")
    else:
        if not membership:
            membership = RoomMembership.objects.create(
                user=user,
                room=chat_room,
                status=RoomMembership.STATUS_MEMBER,
                role=RoomMembership.ROLE_MEMBER,
            )
            messages.info(
                request,
                f"Te has unido automáticamente a la sala pública '{chat_room.name}'.",
            )
        elif membership.status != RoomMembership.STATUS_MEMBER:
            membership.status = RoomMembership.STATUS_MEMBER
            membership.save(update_fields=["status"])
            messages.info(
                request, f"Tu membresía a '{chat_room.name}' ha sido reactivada."
            )

    initial_messages = (
        ChatMessage.objects.filter(room=chat_room, is_deleted_by_moderator=False)
        .select_related("sender")
        .order_by("-timestamp")[:50]
    )
    member_roles_map = {
        m.user.username: m.role
        for m in RoomMembership.objects.filter(room=chat_room).select_related("user")
    }
    creator_username = chat_room.creator.username if chat_room.creator else None

    initial_messages_list = []
    for msg in reversed(initial_messages):
        sender_username = msg.sender_username_display
        role = member_roles_map.get(sender_username, RoomMembership.ROLE_MEMBER)
        if sender_username == creator_username:
            role = "creator"
        initial_messages_list.append(
            {
                "message_id": msg.id,
                "sender_username": sender_username,
                "message": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "role": role,
                "is_deleted": msg.is_deleted_by_moderator,
            }
        )

    initial_users_list = _get_enriched_user_list_for_room(chat_room)

    user_is_creator_or_moderator = (user == chat_room.creator) or (
        membership and membership.role == RoomMembership.ROLE_MODERATOR
    )

    context = {
        "page_title": chat_room.name,
        "chat_room": chat_room,
        "initial_messages_json": initial_messages_list,
        "initial_users_json": initial_users_list,
        "user_is_creator_or_moderator": user_is_creator_or_moderator,
    }
    return render(request, "chat/room_detail.html", context)


@login_required
@require_POST
def leave_room(request, room_slug):
    room = get_object_or_404(ChatRoom, slug=room_slug)
    if room.is_platform_default:
        messages.warning(
            request, "No puedes abandonar la sala general de la plataforma."
        )
        return redirect(reverse("chat:room_detail", kwargs={"room_slug": room.slug}))
    membership = get_object_or_404(RoomMembership, user=request.user, room=room)
    membership.delete()
    messages.success(request, f"Has abandonado la sala '{room.name}'.")
    return redirect("chat:index")


@login_required
def request_join(request, room_slug):
    room = get_object_or_404(ChatRoom, slug=room_slug, is_private=True)
    if request.user == room.creator:
        messages.info(request, f"Ya eres el creador de la sala '{room.name}'.")
        return redirect(reverse("chat:room_detail", kwargs={"room_slug": room.slug}))
    membership, created = RoomMembership.objects.get_or_create(
        user=request.user, room=room, defaults={"status": RoomMembership.STATUS_PENDING}
    )
    if created:
        messages.success(
            request, f"Tu solicitud para unirte a '{room.name}' ha sido enviada."
        )
    else:
        messages.warning(
            request,
            f"Ya tienes una solicitud para esta sala (estado: {membership.get_status_display()}).",
        )
    return redirect("chat:index")


@login_required
@require_POST
def manage_membership(request, membership_id, action):
    membership_request = get_object_or_404(
        RoomMembership, id=membership_id, room__creator=request.user
    )
    if membership_request.status != RoomMembership.STATUS_PENDING:
        messages.warning(request, "Esta solicitud ya no está pendiente.")
        return redirect(
            reverse(
                "chat:room_detail",
                kwargs={"room_slug": membership_request.room.slug},
            )
        )
    if action == "approve":
        membership_request.status = RoomMembership.STATUS_MEMBER
        messages.success(
            request, f"Solicitud de {membership_request.user.username} aprobada."
        )
    elif action == "reject":
        membership_request.status = RoomMembership.STATUS_REJECTED
        messages.info(
            request, f"Solicitud de {membership_request.user.username} rechazada."
        )
    membership_request.save()
    return redirect(
        reverse(
            "chat:room_detail", kwargs={"room_slug": membership_request.room.slug}
        )
    )


@login_required
@require_POST
def toggle_moderator(request, room_slug, user_id_to_toggle):
    pass


@login_required
@require_POST
def toggle_silence(request, room_slug, user_id_to_silence):
    pass


@login_required
@require_POST
def delete_message(request, room_slug, message_id):
    room = get_object_or_404(ChatRoom, slug=room_slug)
    message = get_object_or_404(ChatMessage, id=message_id, room=room)
    membership = RoomMembership.objects.filter(user=request.user, room=room).first()
    is_moderator = (request.user == room.creator) or (
        membership and membership.role == RoomMembership.ROLE_MODERATOR
    )
    if not is_moderator:
        return JsonResponse(
            {"status": "error", "message": "No tienes permisos para borrar mensajes."},
            status=403,
        )
    message.is_deleted_by_moderator = True
    message.content = f"Mensaje eliminado por moderador."
    message.save()
    return JsonResponse({"status": "success", "message_id": message.id})
