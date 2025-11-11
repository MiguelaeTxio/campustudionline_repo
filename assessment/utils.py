# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment/utils.py
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext as _
from django.db.models import Q, Subquery, OuterRef, Count, Case, When, Value, CharField, IntegerField
from django.db.models.lookups import GreaterThan, Exact
from django.db.models.functions import Coalesce
from .models import Assessment, AssessmentSettings

# --- [INICIO] REFACTORIZACIÓN DE ANOTACIONES CONTEXTUALES ---

def _get_base_assessment_subqueries(user_filter):
    """
    Función de ayuda interna para construir las subconsultas base reutilizables.
    """
    related_assessments = Assessment.objects.filter(**user_filter).order_by()

    distinct_states_subquery = related_assessments.annotate(
        dummy=Value(1)
    ).values('dummy').annotate(
        c=Count('status', distinct=True)
    ).values('c')

    single_status_subquery = related_assessments.values('status').distinct()[:1]
    latest_pk_subquery = related_assessments.order_by('-created_at').values('pk')[:1]

    coalesced_subquery = Coalesce(Subquery(distinct_states_subquery, output_field=IntegerField()), Value(0))

    state_annotation = Case(
        When(GreaterThan(coalesced_subquery, Value(1)), then=Value('MULTIPLE')),
        When(Exact(coalesced_subquery, Value(1)), then=Subquery(single_status_subquery, output_field=CharField())),
        default=Value(None),
        output_field=CharField()
    )

    pk_annotation = Case(
        When(Exact(coalesced_subquery, Value(1)), then=Subquery(latest_pk_subquery, output_field=IntegerField())),
        default=Value(None),
        output_field=IntegerField()
    )

    return {'assessment_state': state_annotation, 'latest_assessment_pk': pk_annotation}

def annotate_content_copy_queryset_with_assessment_states(queryset, user):
    """
    Anota un queryset de ContentCopy con el estado de evaluación agregado.
    Esta es ahora la única función de anotación necesaria para la Sala de Estudio.
    """
    user_filter = {'user': user, 'content_copy': OuterRef('pk')}
    annotations = _get_base_assessment_subqueries(user_filter)
    return queryset.annotate(**annotations)

# --- [FIN] REFACTORIZACIÓN DE ANOTACIONES CONTEXTUALES ---

def check_user_assessment_limits(user):
    """
    Calcula los límites de evaluación para un usuario de forma GLOBAL.
    """
    now = timezone.now()
    settings = AssessmentSettings.get_settings()

    FAILURE_STATUSES = [
        Assessment.AssessmentStatus.FAILED,
        Assessment.AssessmentStatus.TIMEOUT_FAILURE,
        Assessment.AssessmentStatus.GENERATION_FAILURE,
        Assessment.AssessmentStatus.USER_CANCELLED,
    ]
    all_valid_user_assessments = Assessment.objects.filter(user=user).exclude(
        status__in=FAILURE_STATUSES
    )

    DAILY_LIMIT_COUNT = settings.daily_limit
    WEEKLY_LIMIT_COUNT = settings.weekly_limit
    DAILY_LIMIT_TIMEDELTA = timedelta(days=1)
    WEEKLY_LIMIT_TIMEDELTA = timedelta(days=7)
    PENALTY_WINDOW_TIMEDELTA = timedelta(days=14)

    assessments_in_last_week = all_valid_user_assessments.filter(
        created_at__gte=now - WEEKLY_LIMIT_TIMEDELTA
    )
    assessments_in_last_day = assessments_in_last_week.filter(
        created_at__gte=now - DAILY_LIMIT_TIMEDELTA
    )
    daily_count = assessments_in_last_day.count()
    weekly_count = assessments_in_last_week.count()

    penalized_assessments = all_valid_user_assessments.filter(
        status="CORRECTION_EXPIRED",
        created_at__gte=now - PENALTY_WINDOW_TIMEDELTA,
        created_at__lt=now - WEEKLY_LIMIT_TIMEDELTA,
    ).count()
    weekly_count += penalized_assessments

    is_daily_limit_reached = daily_count >= DAILY_LIMIT_COUNT
    is_weekly_limit_reached = weekly_count >= WEEKLY_LIMIT_COUNT

    return {
        "daily": {
            "count": daily_count,
            "limit": DAILY_LIMIT_COUNT,
            "is_reached": is_daily_limit_reached,
        },
        "weekly": {
            "count": weekly_count,
            "limit": WEEKLY_LIMIT_COUNT,
            "is_reached": is_weekly_limit_reached,
        },
        "can_create_new": not is_daily_limit_reached and not is_weekly_limit_reached,
        "assessments_in_last_day": assessments_in_last_day,
        "assessments_in_last_week": assessments_in_last_week,
    }


def get_assessment_context(user, content_copy):
    """
    Calcula el contexto completo para el bloque de estado de la autoevaluación.
    """
    now = timezone.now()
    all_user_assessments_for_content = Assessment.objects.filter(
        user=user, content_copy=content_copy
    ).select_related("content_copy__original_content")

    limit_data = check_user_assessment_limits(user)
    can_create_new = limit_data["can_create_new"]

    FAILURE_STATUSES = [
        Assessment.AssessmentStatus.FAILED,
        Assessment.AssessmentStatus.TIMEOUT_FAILURE,
        Assessment.AssessmentStatus.GENERATION_FAILURE,
        Assessment.AssessmentStatus.USER_CANCELLED,
    ]

    context = {
        "status": "PUEDE_SOLICITAR",
        "status_text": "",
        "creation_timer": None,
        "take_assessment_timer": None,
        "available_corrections": [],
        "buttons": {
            "solicitar": { "is_disabled": True, "url": "#", "text": _("No Disponible") },
            "realizar": { "is_disabled": True, "url": "#", "text": _("No Disponible") },
        },
        "limits": limit_data,
        "raw_assessment": None,
        "copy_pk": content_copy.pk,
        "assessment_to_take": None,
    }

    assessment_to_take = all_user_assessments_for_content.filter(
        status=Assessment.AssessmentStatus.COMPLETED, expiration_date__gt=now
    ).order_by("-created_at").first()

    if assessment_to_take:
        context["assessment_to_take"] = assessment_to_take
        context["status"] = "REALIZAR_PENDIENTE"
        context["take_assessment_timer"] = {
            "label": _("Debes realizar esta evaluación en:"),
            "end_time_iso": assessment_to_take.expiration_date.isoformat(),
        }
    else:
        latest_assessment = all_user_assessments_for_content.order_by("-created_at").first()
        context["raw_assessment"] = latest_assessment

        if latest_assessment and latest_assessment.status in FAILURE_STATUSES:
            context["status"] = "FALLIDA"
            context["status_text"] = _("Error: {}").format(latest_assessment.get_status_display())
        
        elif not can_create_new:
            context["status"] = "EN_ESPERA"
            daily_slot, weekly_slot = None, None
            if limit_data["daily"]["is_reached"]:
                oldest_in_day = limit_data["assessments_in_last_day"].order_by("created_at").first()
                if oldest_in_day:
                    daily_slot = oldest_in_day.created_at + timedelta(days=1)
            if limit_data["weekly"]["is_reached"]:
                oldest_in_week = limit_data["assessments_in_last_week"].order_by("created_at").first()
                if oldest_in_week:
                    weekly_slot = oldest_in_week.created_at + timedelta(days=7)
            
            potential_slots = [s for s in [daily_slot, weekly_slot] if s]
            if potential_slots:
                context["creation_timer"] = {
                    "label": _("Próxima evaluación disponible en:"),
                    "end_time_iso": max(potential_slots).isoformat(),
                }
        
        if latest_assessment:
            s = latest_assessment.status
            if s in ["PENDING", "PROCESSING"]:
                context["status"] = "GENERANDOSE"
                context["status_text"] = latest_assessment.get_status_display()
            elif s == "CORRECTING":
                context["status"] = "CORRIGIENDOSE"
                context["status_text"] = latest_assessment.get_status_display()

    visible_assessments = Assessment.objects.filter(
        user=user,
        status=Assessment.AssessmentStatus.RESULTS_AVAILABLE,
        results_expiration_date__gt=now,
    ).select_related("content_copy__original_content")

    for assessment in visible_assessments:
        context["available_corrections"].append({
            "pk": assessment.pk,
            "url": reverse("assessment:view_results", kwargs={"pk": assessment.pk}),
            "content_title": assessment.content_copy.original_content.title,
            "expiration_iso": assessment.results_expiration_date.isoformat(),
        })

    can_solicitar = (
        (not context["assessment_to_take"])
        and (context["status"] in ["PUEDE_SOLICITAR", "FALLIDA"])
        and can_create_new
    )

    realizar_url = (
        reverse("assessment:take_assessment", kwargs={"pk": context["assessment_to_take"].pk})
        if context["assessment_to_take"]
        else "#"
    )

    context["buttons"] = {
        "solicitar": {
            "is_disabled": not can_solicitar,
            "url": reverse("assessment:generate_ai_assessment", kwargs={"copy_pk": content_copy.pk}),
            "text": _("Solicitar Evaluación"),
        },
        "realizar": {
            "is_disabled": not bool(context["assessment_to_take"]),
            "url": realizar_url,
            "text": _("Realizar Evaluación"),
        },
    }

    if context["status"] == "FALLIDA" and not context["assessment_to_take"]:
        context["buttons"]["solicitar"]["text"] = _("Generar de Nuevo")

    return context
