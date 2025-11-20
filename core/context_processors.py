# /home/MiguelAeTxio/CampuStudiOnline/core/context_processors.py
from django.conf import settings
from django.db.models import Count, Q
from messaging.models import DirectMessage
from assessment.models import Assessment
from chat.models import ChatRoom


def global_context(request):
    """
    Adds global variables to the context of all templates.
    Includes VAPID key, P2P message counters, and assessment indicators
    for the Study Room, visible globally in the navigation bar.
    """
    context = {
        "SITE_URL": settings.SITE_URL,
        "VAPID_PUBLIC_KEY": settings.VAPID_PUBLIC_KEY,
        "show_preloader": True,
        "show_tour": False,
        "unread_p2p_message_count": 0,
        "protection_level": None,
        "study_room_iv_data": None,
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

        # --- Navbar Notification Logic (Intelligent Badge) ---
        base_query = Assessment.objects.filter(user=user)

        # Individual notification counters (only for UNSEEN items)
        notifications = {
            "COMPLETED": {
                "count": base_query.filter(status=Assessment.AssessmentStatus.COMPLETED, was_viewed=False).count(),
                "status": "COMPLETED",
            },
            "RESULTS_AVAILABLE": {
                "count": base_query.filter(status=Assessment.AssessmentStatus.RESULTS_AVAILABLE, was_viewed=False).count(),
                "status": "RESULTS_AVAILABLE",
            },
            "PROCESSING": {
                "count": base_query.filter(status__in=[
                    Assessment.AssessmentStatus.PROCESSING,
                    Assessment.AssessmentStatus.CORRECTING,
                    Assessment.AssessmentStatus.AWAITING_CORRECTION,
                ]).count(),
                "status": "PROCESSING",
            },
            "PENDING": {
                "count": base_query.filter(status=Assessment.AssessmentStatus.PENDING).count(),
                "status": "PENDING", # Note: 'PENDING' doesn't have a specific badge style, but is counted.
            },
        }

        # Filter out notification types with a zero count
        active_notifications = [v for k, v in notifications.items() if v["count"] > 0]
        
        # Determine the final badge to display
        if len(active_notifications) == 1:
            # If there's only one type of notification, use its specific style
            context["study_room_iv_data"] = active_notifications[0]
        elif len(active_notifications) > 1:
            # If there are multiple types, show a consolidated 'MULTIPLE' badge
            total_count = sum(item["count"] for item in active_notifications)
            context["study_room_iv_data"] = {
                "count": total_count,
                "status": "MULTIPLE",
            }
            
    return context
