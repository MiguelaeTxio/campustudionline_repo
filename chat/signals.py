from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
import logging

from contents.models import ContentCopy
from .models import ChatRoom, RoomMembership

User = get_user_model()
logger = logging.getLogger(__name__)

# Constantes para salas globales
GLOBAL_ROOM_NAME = "CampuStudiOnline"
HELP_ROOM_NAME = "Ayuda de eLCampus"

@receiver(post_save, sender=User)
def add_user_to_global_rooms(sender, instance, created, **kwargs):
    """
    Añade automáticamente a los nuevos usuarios a las salas globales.
    """
    if created:
        _join_global_room(instance, GLOBAL_ROOM_NAME)
        _join_global_room(instance, HELP_ROOM_NAME)

def _join_global_room(user, room_name):
    try:
        # Usamos get_or_create para asegurar que la sala exista,
        # aunque idealmente deberían crearse vía migración de datos.
        room, _ = ChatRoom.objects.get_or_create(
            name=room_name,
            defaults={
                'is_private': False,
                'description': f"Sala global: {room_name}",
                'is_platform_default': True
            }
        )
        RoomMembership.objects.get_or_create(
            user=user,
            room=room,
            defaults={'status': RoomMembership.STATUS_MEMBER}
        )
    except Exception as e:
        logger.error(f"Error añadiendo usuario {user.username} a sala global {room_name}: {e}")

@receiver(post_save, sender=ContentCopy)
def add_user_to_context_room(sender, instance, created, **kwargs):
    """
    Añade al usuario a la sala de chat contextual correspondiente al crear una copia de estudio.
    """
    if created:
        target_subject = instance.subject_context
        # Determinar categorías desde el contenido original
        original = instance.original_content
        target_sub_category = original.sub_category
        target_master_category = original.master_category
        
        # Prioridad de contexto: Asignatura > Subcategoría > Categoría Maestra
        room = None
        
        try:
            with transaction.atomic():
                if target_subject:
                    room = _get_or_create_context_room(target_subject=target_subject)
                elif target_sub_category:
                    room = _get_or_create_context_room(target_sub_category=target_sub_category)
                elif target_master_category:
                    room = _get_or_create_context_room(target_master_category=target_master_category)
                
                if room:
                    RoomMembership.objects.get_or_create(
                        user=instance.user,
                        room=room,
                        defaults={'status': RoomMembership.STATUS_MEMBER}
                    )
        except Exception as e:
            logger.error(f"Error gestionando sala contextual para copia {instance.id}: {e}")

def _get_or_create_context_room(target_subject=None, target_sub_category=None, target_master_category=None):
    """
    Busca o crea una sala basada en el contexto.
    """
    # 1. Intentar buscar sala existente por vínculo directo
    if target_subject:
        room = ChatRoom.objects.filter(target_subject=target_subject).first()
        name_base = str(target_subject)
    elif target_sub_category:
        room = ChatRoom.objects.filter(target_sub_category=target_sub_category).first()
        name_base = f"{target_sub_category.master_category.name} - {target_sub_category.name}"
    elif target_master_category:
        room = ChatRoom.objects.filter(target_master_category=target_master_category).first()
        name_base = target_master_category.name
    else:
        return None

    if room:
        return room

    # 2. Si no existe, crearla.
    # Manejo de colisiones de nombre: ChatRoom.name debe ser único.
    # Usamos el slug del objeto de contexto o un nombre descriptivo.
    
    defaults = {
        'is_private': True, # Las salas contextuales son privadas por definición
        'is_platform_default': False,
    }
    
    if target_subject:
        defaults['target_subject'] = target_subject
        defaults['description'] = f"Sala de estudio para la asignatura: {target_subject.name}"
    elif target_sub_category:
        defaults['target_sub_category'] = target_sub_category
        defaults['description'] = f"Sala de interés para: {target_sub_category.name}"
    elif target_master_category:
        defaults['target_master_category'] = target_master_category
        defaults['description'] = f"Sala de interés para: {target_master_category.name}"

    # Intentamos crear con el nombre base. Si falla, añadimos sufijos.
    try:
        room = ChatRoom.objects.create(name=name_base, **defaults)
    except IntegrityError:
        # Si el nombre ya existe (raro si viene de contexto único, pero posible si el usuario creó una sala con ese nombre antes)
        # Intentamos con el slug o ID
        suffix = ""
        if target_subject: suffix = f" ({target_subject.slug})"
        elif target_sub_category: suffix = f" ({target_sub_category.slug})"
        elif target_master_category: suffix = f" ({target_master_category.slug})"
        
        final_name = f"{name_base}{suffix}"[:255] # Asegurar límite
        room = ChatRoom.objects.create(name=final_name, **defaults)
        
    return room
