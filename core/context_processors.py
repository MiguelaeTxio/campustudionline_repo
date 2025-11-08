# /home/MiguelAeTxio/CampuStudiOnline/core/context_processors.py
from django.conf import settings
from django.db.models import Count, Q
from messaging.models import DirectMessage
from assessment.models import Assessment
from chat.models import ChatRoom


def global_context(request):
    """
    Adds global variables to the context of all templates.
    Includes the VAPID public key, P2P message counters, and granular
    assessment indicators for the navigation bar.
    """
    context = {
        "SITE_URL": settings.SITE_URL,
        "VAPID_PUBLIC_KEY": settings.VAPID_PUBLIC_KEY,
        "show_preloader": True,
        "show_tour": False,  # Default value for anonymous users
        "unread_p2p_message_count": 0,
        "academic_dir_iv": None,
        "free_dir_iv": None,
        "protection_level": None, # Default value
    }

    if request.user.is_authenticated:
        user = request.user
        context["show_tour"] = True # Enable tour for authenticated users

        # Counter for unread P2P messages
        context["unread_p2p_message_count"] = DirectMessage.objects.filter(
            Q(session__user1=user) | Q(session__user2=user),
            ~Q(sender=user),
            is_read=False,
        ).count()

        # Get the general chat room to determine its protection level
        general_room = ChatRoom.objects.filter(is_platform_default=True).first()
        if general_room:
            context["protection_level"] = general_room.is_private

        # --- New NavBar Indicator Logic ---
        
        # Relevant statuses for indicators
        active_statuses = [
            Assessment.AssessmentStatus.COMPLETED,
            Assessment.AssessmentStatus.RESULTS_AVAILABLE,
            Assessment.AssessmentStatus.PROCESSING,
            Assessment.AssessmentStatus.CORRECTING,
            Assessment.AssessmentStatus.FAILED,
            Assessment.AssessmentStatus.TIMEOUT_FAILURE,
            Assessment.AssessmentStatus.GENERATION_FAILURE,
        ]

        # Base queryset for the user's active assessments
        base_assessments = Assessment.objects.filter(
            user=user, status__in=active_statuses
        )

        # 1. Academic Directory Indicators
        academic_assessments = base_assessments.filter(content__subject__isnull=False)
        academic_stats = academic_assessments.aggregate(
            total_count=Count("id"), distinct_statuses=Count("status", distinct=True)
        )

        if academic_stats["total_count"] > 0:
            if academic_stats["distinct_statuses"] == 1:
                status = academic_assessments.values_list("status", flat=True).first()
                context["academic_dir_iv"] = {
                    "count": academic_stats["total_count"], "status": status
                }
            else:
                context["academic_dir_iv"] = {
                    "count": academic_stats["total_count"], "status": "MULTIPLE"
                }

        # 2. Free Directory Indicators
        free_assessments = base_assessments.filter(content__topic__isnull=False)
        free_stats = free_assessments.aggregate(
            total_count=Count("id"), distinct_statuses=Count("status", distinct=True)
        )

        if free_stats["total_count"] > 0:
            if free_stats["distinct_statuses"] == 1:
                status = free_assessments.values_list("status", flat=True).first()
                context["free_dir_iv"] = {
                    "count": free_stats["total_count"], "status": status
                }
            else:
                context["free_dir_iv"] = {
                    "count": free_stats["total_count"], "status": "MULTIPLE"
                }

    return context
