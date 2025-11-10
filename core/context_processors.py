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
        # Navbar Assessment Indicators (Study Room specific)
        "assessments_to_take_count": 0,
        "assessments_with_results_count": 0,
        "assessments_in_progress_count": 0,
        "assessments_in_queue_count": 0,
        "assessments_failed_count": 0,
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

        # --- Study Room Navbar Indicator Logic (Refactored) ---
        base_assessments = Assessment.objects.filter(user=user)

        # Count assessments ready to be taken (not expired)
        context["assessments_to_take_count"] = base_assessments.filter(
            status=Assessment.AssessmentStatus.COMPLETED
        ).count()

        # Count available results that have not been viewed yet
        context["assessments_with_results_count"] = base_assessments.filter(
            status=Assessment.AssessmentStatus.RESULTS_AVAILABLE, was_viewed=False
        ).count()
        
        # Count assessments currently being generated or corrected
        context["assessments_in_progress_count"] = base_assessments.filter(
            status__in=[
                Assessment.AssessmentStatus.PROCESSING,
                Assessment.AssessmentStatus.CORRECTING,
            ]
        ).count()

        # Count assessments waiting in the queue
        context["assessments_in_queue_count"] = base_assessments.filter(
            status=Assessment.AssessmentStatus.PENDING
        ).count()

        # Count failed assessments that have not been viewed/acknowledged yet
        context["assessments_failed_count"] = base_assessments.filter(
            status__in=[
                Assessment.AssessmentStatus.FAILED,
                Assessment.AssessmentStatus.TIMEOUT_FAILURE,
                Assessment.AssessmentStatus.GENERATION_FAILURE,
            ],
            was_viewed=False,
        ).count()

    return context
