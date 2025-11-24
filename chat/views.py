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
# (Se mantienen idénticas para no romper la funcionalidad de chat en tiempo real)

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
    
    # En salas privadas, se requiere membresía activa
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
    
    # Verificación de permisos
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
    user = request.user
    
    # 1. Salas Globales (Visibles para todos, unirse es automático al registrarse)
    # Filtramos por platform_default
    global_rooms = ChatRoom.objects.filter(is_platform_default=True)
    
    academic_rooms = []
    interest_rooms = []
    
    if user.is_authenticated:
        # Obtener IDs de salas donde el usuario es miembro activo
        joined_room_ids = RoomMembership.objects.filter(
            user=user, 
            status=RoomMembership.STATUS_MEMBER
        ).values_list('room_id', flat=True)
        
        # 2. Mis Asignaturas (Salas con target_subject donde soy miembro)
        academic_rooms = ChatRoom.objects.filter(
            id__in=joined_room_ids,
            target_subject__isnull=False
        ).select_related('target_subject').order_by('target_subject__name')
        
        # 3. Mis Intereses (Salas con target_sub_category o target_master_category donde soy miembro)
        interest_rooms = ChatRoom.objects.filter(
            id__in=joined_room_ids
        ).filter(
            Q(target_sub_category__isnull=False) | Q(target_master_category__isnull=False)
        ).select_related('target_sub_category', 'target_master_category').order_by('name')

    context = {
        "global_rooms": global_rooms,
        "academic_rooms": academic_rooms,
        "interest_rooms": interest_rooms,
        "user_is_authenticated": user.is_authenticated,
        "show_tour": True, # Se puede mantener o actualizar el tour
    }
    return render(request, "chat/index.html", context)


# create_room ELIMINADO


@login_required
def room_detail(request, room_slug):
    try:
        chat_room = ChatRoom.objects.select_related("creator").get(slug=room_slug)
    except ChatRoom.DoesNotExist:
        raise Http404("La sala de chat especificada no existe.")

    user = request.user
    membership = RoomMembership.objects.filter(user=user, room=chat_room).first()

    # Lógica simplificada: Si es privada, DEBE tener membresía.
    # Ya no hay "unirse automáticamente" a públicas desde aquí, 
    # porque la única forma de entrar a una sala privada es vía automatización.
    # Las globales (platform_default) ya tienen membresía creada al inicio.
    
    if chat_room.is_private and not chat_room.is_platform_default:
        if not membership or membership.status != RoomMembership.STATUS_MEMBER:
            messages.error(
                request,
                f"No tienes permiso para acceder a la sala '{chat_room.name}'. Acceso restringido.",
            )
            return redirect("chat:index")
    
    # Autorecovery para globales si por alguna razón falló la señal
    if chat_room.is_platform_default and not membership:
        membership = RoomMembership.objects.create(
            user=user,
            room=chat_room,
            status=RoomMembership.STATUS_MEMBER,
            role=RoomMembership.ROLE_MEMBER,
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
            request, "No puedes abandonar las salas globales de la plataforma."
        )
        return redirect(reverse("chat:room_detail", kwargs={"room_slug": room.slug}))
    
    # En el nuevo modelo contextual, ¿tiene sentido abandonar una sala de asignatura?
    # Si abandonas, ¿cómo vuelves? (Solo borrando la copia de estudio y creándola de nuevo?)
    # Por ahora permitimos salir, asumiendo que el usuario quiere "silenciar" esa sala de su lista.
    # Pero el trigger de entrada solo salta al CREAR copia.
    
    membership = get_object_or_404(RoomMembership, user=request.user, room=room)
    membership.delete()
    messages.success(request, f"Has abandonado la sala '{room.name}'.")
    return redirect("chat:index")


# request_join ELIMINADO (Ya no hay solicitud manual)


@login_required
@require_POST
def manage_membership(request, membership_id, action):
    # Mantenido para gestión legacy si queda alguna pendiente, o para moderadores.
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
