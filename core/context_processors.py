# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/core/context_processors.py
from django.conf import settings
from django.db.models import Count, Q
from messaging.models import DirectMessage
# [CLEANUP HITO 6] Eliminada importación de Assessment
from chat.models import ChatRoom
import logging
from contents.services.navigation_builder import refresh_user_navigation
from contents.models import UserStudyNavigation

logger = logging.getLogger(__name__)


def global_context(request):
    """
    Adds global variables to the context of all templates.
    Includes VAPID key, P2P message counters, and general site settings.
    """
    context = {
        "SITE_URL": settings.SITE_URL,
        "VAPID_PUBLIC_KEY": settings.VAPID_PUBLIC_KEY,
        "META_PIXEL_ID": getattr(settings, "META_PIXEL_ID", None),
        "show_preloader": True,
        "show_tour": False,
        "unread_p2p_message_count": 0,
        "protection_level": None,
        "study_room_iv_data": None,  # Mantenido como None para compatibilidad de plantillas
    }

    if request.user.is_authenticated:
        user = request.user
        context["show_tour"] = True

        # P2P message counter
        context["unread_p2p_message_count"] = DirectMessage.objects.filter(
            Q(session__user1=user) | Q(session__user2=user),
            ~Q(sender=user),
            is_read=False,
        ).count()

        # General chat room protection level
        general_room = ChatRoom.objects.filter(is_platform_default=True).first()
        if general_room:
            context["protection_level"] = general_room.is_private

        # --- Navbar Notification Logic (REMOVED HITO 6) ---
        # La lógica de insignias de evaluación se reconstruirá en fases posteriores.

        # --- Study Room Navigation Tree (User-Centric) ---
        try:
            # Acceso optimizado vía reverse relation
            nav_entry = getattr(user, 'study_navigation', None)
            if nav_entry:
                context["user_navigation_tree"] = nav_entry.navigation_tree
            else:
                raise UserStudyNavigation.DoesNotExist
        except (UserStudyNavigation.DoesNotExist, AttributeError):
            # Lazy generation: Si no existe, se crea al vuelo (Fail-safe)
            try:
                refresh_user_navigation(user)
                nav_entry = UserStudyNavigation.objects.get(user=user)
                context["user_navigation_tree"] = nav_entry.navigation_tree
            except Exception as e:
                logger.error(f"Failed to generate navigation tree for user {user.id}: {e}")
                context["user_navigation_tree"] = {}

    return context
