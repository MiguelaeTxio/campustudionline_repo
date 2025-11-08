# /home/MiguelAeTxio/CampuStudiOnline/academic_chat/views.py
import json
import logging
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import get_user_model
from django.utils import timezone

from academic_structure.models import University, Branch, Degree
from .models import AcademicChatLink, AcademicChatMessage
from .decorators import user_can_access_academic_chat
from .tasks import process_academic_chat_message

logger = logging.getLogger(__name__)

ACADEMIC_CHAT_NAVIGATOR_TEMPLATE = "academic_chat/academic_chat_navigator.html"
ACADEMIC_CHAT_ROOM_TEMPLATE = "academic_chat/academic_chat_room.html"


def _get_enriched_user_list_for_academic_room(academic_link, current_user):
    User = get_user_model()
    user_list = {}

    if academic_link.group:
        users_in_group = User.objects.filter(groups=academic_link.group).order_by(
            "username"
        )
        for user in users_in_group:
            user_list[user.username] = {
                "username": user.username,
                "user_id": user.id,
                "role": (
                    "creator"
                    if user == academic_link.chat_room.creator or user.is_superuser
                    else "member"
                ),
                "is_silenced_in_channel": False,
            }

    if current_user.is_superuser and current_user.username not in user_list:
        user_list[current_user.username] = {
            "username": current_user.username,
            "user_id": current_user.id,
            "role": "creator",
            "is_silenced_in_channel": False,
        }

    return sorted(
        user_list.values(), key=lambda u: (u["role"] != "creator", u["username"])
    )


def get_accessible_chat_links_queryset(user):
    if not user.is_authenticated:
        return AcademicChatLink.objects.none()
    if user.is_superuser:
        return AcademicChatLink.objects.all()
    q_objects = Q()
    if hasattr(user, "affiliated_university") and user.affiliated_university:
        if user.groups.filter(name__in=["rectors", "professors"]).exists():
            q_objects.add(
                Q(subject__academic_year__degree__branch__university=user.affiliated_university), Q.OR
            )
    q_objects.add(Q(enrolled_students=user), Q.OR)
    if user.groups.exists():
        q_objects.add(Q(group__in=user.groups.all()), Q.OR)
    return AcademicChatLink.objects.filter(q_objects).distinct()


@login_required
def university_list_view(request):
    accessible_links = get_accessible_chat_links_queryset(request.user)
    accessible_university_ids = accessible_links.values_list(
        "subject__academic_year__degree__branch__university_id", flat=True
    ).distinct()
    universities_list = University.objects.filter(
        pk__in=accessible_university_ids
    ).order_by("name")
    paginator = Paginator(universities_list, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    breadcrumb = [
        {"name": "Chats Académicos", "url": reverse("academic_chat:university_list")}
    ]
    context = {
        "page_title": "Universidades con Chats Académicos",
        "breadcrumb": breadcrumb,
        "current_level_name": "Chats Académicos",
        "next_level_name": "Universidades",
        "next_level_items": page_obj,
        "final_items": None,
        "next_url_name": "academic_chat:branch_list",
    }
    return render(request, ACADEMIC_CHAT_NAVIGATOR_TEMPLATE, context)


@login_required
def branch_list_view(request, university_slug):
    university = get_object_or_404(University, slug=university_slug)
    accessible_links = get_accessible_chat_links_queryset(request.user)
    accessible_branch_ids = (
        accessible_links.filter(
            subject__academic_year__degree__branch__university__slug=university_slug
        )
        .values_list("subject__academic_year__degree__branch_id", flat=True)
        .distinct()
    )
    branches_list = Branch.objects.filter(pk__in=accessible_branch_ids).order_by("name")
    paginator = Paginator(branches_list, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    breadcrumb = [
        {"name": "Chats Académicos", "url": reverse("academic_chat:university_list")},
        {
            "name": university.name,
            "url": reverse(
                "academic_chat:branch_list",
                kwargs={"university_slug": university.slug},
            ),
        },
    ]
    context = {
        "page_title": f"{university.name} - Ramas de Conocimiento",
        "breadcrumb": breadcrumb,
        "current_level_name": university.name,
        "next_level_name": "Ramas de Conocimiento",
        "next_level_items": page_obj,
        "final_items": None,
        "university_slug": university_slug,
        "next_url_name": "academic_chat:degree_list",
    }
    return render(request, ACADEMIC_CHAT_NAVIGATOR_TEMPLATE, context)


@login_required
def degree_list_view(request, university_slug, branch_slug):
    branch = get_object_or_404(
        Branch.objects.select_related("university"),
        slug=branch_slug,
        university__slug=university_slug,
    )
    accessible_links = get_accessible_chat_links_queryset(request.user)
    accessible_degree_ids = (
        accessible_links.filter(
            subject__academic_year__degree__branch__slug=branch_slug,
            subject__academic_year__degree__branch__university__slug=university_slug,
        )
        .values_list("subject__academic_year__degree_id", flat=True)
        .distinct()
    )
    degrees_list = Degree.objects.filter(pk__in=accessible_degree_ids).order_by("name")
    paginator = Paginator(degrees_list, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    breadcrumb = [
        {"name": "Chats Académicos", "url": reverse("academic_chat:university_list")},
        {
            "name": branch.university.name,
            "url": reverse(
                "academic_chat:branch_list",
                kwargs={"university_slug": branch.university.slug},
            ),
        },
        {
            "name": branch.name,
            "url": reverse(
                "academic_chat:degree_list",
                kwargs={
                    "university_slug": branch.university.slug,
                    "branch_slug": branch.slug,
                },
            ),
        },
    ]
    context = {
        "page_title": f"{branch.name} - Titulaciones",
        "breadcrumb": breadcrumb,
        "current_level_name": branch.name,
        "next_level_name": "Titulaciones",
        "next_level_items": page_obj,
        "final_items": None,
        "university_slug": university_slug,
        "branch_slug": branch_slug,
        "next_url_name": "academic_chat:academic_year_list",
    }
    return render(request, ACADEMIC_CHAT_NAVIGATOR_TEMPLATE, context)


@login_required
def academic_year_list_view(request, university_slug, branch_slug, degree_slug):
    degree = get_object_or_404(
        Degree.objects.select_related("branch__university"),
        slug=degree_slug,
        branch__slug=branch_slug,
        branch__university__slug=university_slug,
    )
    accessible_links = get_accessible_chat_links_queryset(request.user)
    years = (
        accessible_links.filter(subject__academic_year__degree=degree)
        .values_list("subject__year", flat=True)
        .distinct()
        .order_by("subject__year")
    )
    if not years:
        raise Http404(
            "No hay años académicos con chats disponibles para esta titulación o no tienes acceso."
        )
    year_items = [{"slug": year, "name": f"{year}º Año"} for year in years]
    paginator = Paginator(year_items, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    breadcrumb = [
        {"name": "Chats Académicos", "url": reverse("academic_chat:university_list")},
        {
            "name": degree.branch.university.name,
            "url": reverse(
                "academic_chat:branch_list",
                kwargs={"university_slug": degree.branch.university.slug},
            ),
        },
        {
            "name": degree.branch.name,
            "url": reverse(
                "academic_chat:degree_list",
                kwargs={
                    "university_slug": degree.branch.university.slug,
                    "branch_slug": degree.branch.slug,
                },
            ),
        },
        {
            "name": degree.name,
            "url": reverse(
                "academic_chat:academic_year_list",
                kwargs={
                    "university_slug": degree.branch.university.slug,
                    "branch_slug": degree.branch.slug,
                    "degree_slug": degree.slug,
                },
            ),
        },
    ]
    context = {
        "page_title": f"{degree.name} - Años Académicos",
        "breadcrumb": breadcrumb,
        "current_level_name": degree.name,
        "next_level_name": "Años Académicos",
        "next_level_items": page_obj,
        "final_items": None,
        "university_slug": university_slug,
        "branch_slug": branch_slug,
        "degree_slug": degree_slug,
        "next_url_name": "academic_chat:academic_chat_list",
    }
    return render(request, ACADEMIC_CHAT_NAVIGATOR_TEMPLATE, context)


@login_required
def academic_chat_list_view(request, university_slug, branch_slug, degree_slug, year):
    degree = get_object_or_404(
        Degree.objects.select_related("branch__university"),
        slug=degree_slug,
        branch__slug=branch_slug,
        branch__university__slug=university_slug,
    )
    accessible_links = get_accessible_chat_links_queryset(request.user)
    chat_links_list = (
        accessible_links.filter(subject__academic_year__degree=degree, subject__year=year)
        .select_related("subject", "chat_room")
        .order_by("subject__name")
    )
    if not chat_links_list.exists():
        raise Http404(
            "No se encontraron salas de chat para este año académico o no tienes acceso."
        )
    paginator = Paginator(chat_links_list, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    breadcrumb = [
        {"name": "Chats Académicos", "url": reverse("academic_chat:university_list")},
        {
            "name": degree.branch.university.name,
            "url": reverse(
                "academic_chat:branch_list",
                kwargs={"university_slug": degree.branch.university.slug},
            ),
        },
        {
            "name": degree.branch.name,
            "url": reverse(
                "academic_chat:degree_list",
                kwargs={
                    "university_slug": degree.branch.university.slug,
                    "branch_slug": degree.branch.slug,
                },
            ),
        },
        {
            "name": degree.name,
            "url": reverse(
                "academic_chat:academic_year_list",
                kwargs={
                    "university_slug": degree.branch.university.slug,
                    "branch_slug": degree.branch.slug,
                    "degree_slug": degree.slug,
                },
            ),
        },
        {
            "name": f"{year}º Año",
            "url": reverse(
                "academic_chat:academic_chat_list",
                kwargs={
                    "university_slug": degree.branch.university.slug,
                    "branch_slug": degree.branch.slug,
                    "degree_slug": degree.slug,
                    "year": year,
                },
            ),
        },
    ]
    context = {
        "page_title": f"{degree.name} ({year}º Año) - Salas de Chat",
        "breadcrumb": breadcrumb,
        "current_level_name": f"{year}º Año",
        "next_level_name": None,
        "next_level_items": None,
        "final_items": page_obj,
        "university_slug": university_slug,
        "branch_slug": branch_slug,
        "degree_slug": degree_slug,
        "year": year,
        "next_url_name": "academic_chat:academic_chat_room",
    }
    return render(request, ACADEMIC_CHAT_NAVIGATOR_TEMPLATE, context)


@login_required
@user_can_access_academic_chat
def academic_chat_room(request, chat_slug, academic_link, *args, **kwargs):
    year = academic_link.subject.year
    breadcrumb = [
        {"name": "Chats Académicos", "url": reverse("academic_chat:university_list")},
        {
            "name": academic_link.subject.academic_year.degree.branch.university.name,
            "url": reverse(
                "academic_chat:branch_list",
                kwargs={
                    "university_slug": academic_link.subject.academic_year.degree.branch.university.slug
                },
            ),
        },
        {
            "name": academic_link.subject.academic_year.degree.branch.name,
            "url": reverse(
                "academic_chat:degree_list",
                kwargs={
                    "university_slug": academic_link.subject.academic_year.degree.branch.university.slug,
                    "branch_slug": academic_link.subject.academic_year.degree.branch.slug,
                },
            ),
        },
        {
            "name": academic_link.subject.academic_year.degree.name,
            "url": reverse(
                "academic_chat:academic_year_list",
                kwargs={
                    "university_slug": academic_link.subject.academic_year.degree.branch.university.slug,
                    "branch_slug": academic_link.subject.academic_year.degree.branch.slug,
                    "degree_slug": academic_link.subject.academic_year.degree.slug,
                },
            ),
        },
        {
            "name": f"{year}º Año",
            "url": reverse(
                "academic_chat:academic_chat_list",
                kwargs={
                    "university_slug": academic_link.subject.academic_year.degree.branch.university.slug,
                    "branch_slug": academic_link.subject.academic_year.degree.branch.slug,
                    "degree_slug": academic_link.subject.academic_year.degree.slug,
                    "year": year,
                },
            ),
        },
        {
            "name": academic_link.subject.name,
            "url": reverse(
                "academic_chat:academic_chat_room",
                kwargs={"chat_slug": academic_link.slug},
            ),
        },
    ]
    initial_messages = (
        AcademicChatMessage.objects.filter(
            chat_link=academic_link, is_deleted_by_moderator=False
        )
        .select_related("sender")
        .order_by("-timestamp")[:50]
    )
    initial_messages_list = [
        {
            "message_id": msg.id,
            "sender_username": msg.sender_username_display,
            "message": msg.content,
            "timestamp": msg.timestamp.isoformat(),
            "is_deleted": msg.is_deleted_by_moderator,
            "role": (
                "creator"
                if msg.sender == academic_link.chat_room.creator
                or (msg.sender and msg.sender.is_superuser)
                else "member"
            ),
        }
        for msg in reversed(initial_messages)
    ]
    initial_users_list = _get_enriched_user_list_for_academic_room(
        academic_link, request.user
    )
    current_user_role = "member"
    if request.user.is_superuser or request.user == academic_link.chat_room.creator:
        current_user_role = "creator"
    context = {
        "page_title": academic_link.chat_room.name,
        "breadcrumb": breadcrumb,
        "academic_link": academic_link,
        "initial_messages_json": initial_messages_list,
        "initial_users_json": initial_users_list,
        "user_is_creator": current_user_role == "creator",
        "current_user_role": current_user_role,
    }
    return render(request, ACADEMIC_CHAT_ROOM_TEMPLATE, context)


@require_POST
@login_required
@user_can_access_academic_chat
def send_academic_chat_message_api(request, chat_slug, academic_link, *args, **kwargs):
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
            {"status": "error", "message": "Petición inválida, se esperaba JSON."},
            status=400,
        )
    process_academic_chat_message.delay(
        academic_link_id=str(academic_link.id),
        sender_id=request.user.id,
        content=message_content,
    )
    current_user_role = (
        "creator"
        if request.user.is_superuser or request.user == academic_link.chat_room.creator
        else "member"
    )
    message_data = {
        "sender_username": request.user.username,
        "message": message_content,
        "timestamp": timezone.now().isoformat(),
        "is_deleted": False,
        "role": current_user_role,
    }
    return JsonResponse({"status": "success", "message_data": message_data})


@require_GET
@login_required
@user_can_access_academic_chat
def get_academic_chat_updates_api(request, chat_slug, academic_link, *args, **kwargs):
    last_message_id = int(request.GET.get("last_message_id", "0"))
    new_messages = (
        AcademicChatMessage.objects.filter(
            chat_link=academic_link, id__gt=last_message_id
        )
        .select_related("sender")
        .order_by("timestamp")
    )
    messages_data = [
        {
            "message_id": msg.id,
            "sender_username": msg.sender_username_display,
            "message": msg.content,
            "timestamp": msg.timestamp.isoformat(),
            "is_deleted": msg.is_deleted_by_moderator,
            "role": (
                "creator"
                if msg.sender == academic_link.chat_room.creator
                or (msg.sender and msg.sender.is_superuser)
                else "member"
            ),
        }
        for msg in new_messages
    ]
    current_user_role = "member"
    if request.user.is_superuser or request.user == academic_link.chat_room.creator:
        current_user_role = "creator"
    return JsonResponse(
        {
            "status": "success",
            "messages": messages_data,
            "users_enriched": _get_enriched_user_list_for_academic_room(
                academic_link, request.user
            ),
            "current_user_role": current_user_role,
        }
    )


@require_POST
@login_required
@user_can_access_academic_chat
def delete_academic_chat_message(
    request, chat_slug, message_id, academic_link, *args, **kwargs
):
    is_creator = request.user == academic_link.chat_room.creator
    if not is_creator and not request.user.is_superuser:
        return JsonResponse(
            {"status": "error", "message": "No tienes permiso para borrar mensajes."},
            status=403,
        )
    try:
        message_to_delete = AcademicChatMessage.objects.get(
            id=message_id, chat_link=academic_link
        )
        if not message_to_delete.is_deleted_by_moderator:
            message_to_delete.content = f"Mensaje eliminado por moderador."
            message_to_delete.is_deleted_by_moderator = True
            message_to_delete.save(update_fields=["content", "is_deleted_by_moderator"])
        return JsonResponse(
            {
                "status": "success",
                "message": "Mensaje borrado.",
                "message_id": message_to_delete.id,
            }
        )
    except AcademicChatMessage.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Mensaje no encontrado."}, status=404
        )
