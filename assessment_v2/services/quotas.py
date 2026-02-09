# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/quotas.py
import logging
from django.utils import timezone
from datetime import timedelta
from assessment_v2.models.plans import UserSubscription, SubscriptionPlan
from assessment_v2.models.main import Exam

logger = logging.getLogger(__name__)

class QuotaService:
    """
    Service to manage exam quotas and automatic subscription assignments.

    Servicio para gestionar las cuotas de exámenes y la asignación automática de suscripciones.
    """

    @classmethod
    def get_or_create_default_subscription(cls, user):
        """
        Assigns FREE plan to regular users and DIOS plan to superusers.

        Asigna el plan FREE a usuarios normales y el plan DIOS a superusuarios.
        """
        sub = UserSubscription.objects.filter(user=user, is_active=True).first()
        if not sub:
            target_code = SubscriptionPlan.CODE_DIOS if user.is_superuser else SubscriptionPlan.CODE_FREE
            
            # Default limits for initialization if plan doesn't exist in DB yet
            defaults = {
                'daily_exam_limit': 9999 if user.is_superuser else 1,
                'weekly_exam_limit': 9999 if user.is_superuser else 3,
                'description': 'Asignación automática por sistema.'
            }
            
            plan, _ = SubscriptionPlan.objects.get_or_create(
                name=target_code,
                defaults=defaults
            )
            sub = UserSubscription.objects.create(user=user, plan=plan)
            logger.info(f"Auto-assigned {target_code} plan to user {user.username}")
        return sub

    @classmethod
    def check_exam_eligibility(cls, user):
        """
        Checks if the user can generate an exam based on a sliding window.

        Verifica si el usuario puede generar un examen basado en una ventana móvil.
        """
        subscription = cls.get_or_create_default_subscription(user)
        plan = subscription.plan

        now = timezone.now()
        day_start = now - timedelta(hours=24)
        week_start = now - timedelta(days=7)

        # Count exams created in the last 24h
        daily_count = Exam.objects.filter(user=user, created_at__gte=day_start).count()
        if daily_count >= plan.daily_exam_limit:
            return False, f"Límite diario alcanzado ({daily_count}/{plan.daily_exam_limit})."

        # Count exams created in the last 7 days
        weekly_count = Exam.objects.filter(user=user, created_at__gte=week_start).count()
        if weekly_count >= plan.weekly_exam_limit:
            return False, f"Límite semanal alcanzado ({weekly_count}/{plan.weekly_exam_limit})."

        return True, "OK"
