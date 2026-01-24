# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment/utils.py
from datetime import timedelta
from math import ceil
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext as _
from django.db.models import Q, Subquery, OuterRef, Count, Case, When, Value, CharField, IntegerField
from django.db.models.lookups import GreaterThan, Exact
from django.db.models.functions import Coalesce
from .models import Assessment, AssessmentSettings
import re
import json

def get_assessment_context(user, content_copy):
    """Calcula el contexto para el bloque de estado (UI)."""
    now = timezone.now()
    latest = Assessment.objects.filter(user=user, content_copy=content_copy).order_by('-created_at').first()
    limit_data = check_user_assessment_limits(user)
    
    status_ui = "PUEDE_SOLICITAR"
    status_text = ""
    
    if latest:
        if latest.status in ["PENDING", "PROCESSING"]:
            status_ui = "GENERANDOSE"
            status_text = _("Generando examen con IA")
        elif latest.status == "COMPLETED":
            status_ui = "REALIZAR_PENDIENTE"
        elif latest.status in ["AWAITING_CORRECTION", "CORRECTING"]:
            status_ui = "CORRIGIENDOSE"
            status_text = _("Corrigiendo respuestas")
        elif latest.status == "RESULTS_AVAILABLE":
            status_ui = "RESULTADOS_LISTOS"
        elif "FAILED" in latest.status:
            status_ui = "FALLIDA"
            status_text = latest.get_status_display()
    
    if status_ui == "PUEDE_SOLICITAR" and not limit_data["can_create_new"]:
        status_ui = "EN_ESPERA"

    context = {
        "status": status_ui,
        "status_text": status_text,
        "limits": limit_data,
        "copy_pk": content_copy.pk,
        "raw_assessment": latest,
        "latest_result_url": reverse("assessment:view_results", kwargs={"pk": latest.pk}) if latest and latest.status == "RESULTS_AVAILABLE" else "#",
        "buttons": {
            "solicitar": {
                "is_disabled": not limit_data["can_create_new"],
                "url": reverse("assessment:generate_ai_assessment", kwargs={"copy_pk": content_copy.pk}),
                "text": _("Solicitar Evaluación")
            },
            "realizar": {
                "is_disabled": status_ui != "REALIZAR_PENDIENTE",
                "url": reverse("assessment:take_assessment", kwargs={"pk": latest.pk}) if latest else "#",
                "text": _("Realizar Evaluación")
            }
        }
    }
    return context

def check_user_assessment_limits(user):
    """Control de cuotas diario/semanal."""
    now = timezone.now()
    app_settings = AssessmentSettings.get_settings()
    valid_assessments = Assessment.objects.filter(user=user).exclude(status__in=["CANCELLED", "USER_CANCELLED"])
    
    daily_count = valid_assessments.filter(created_at__gte=now - timedelta(days=1)).count()
    weekly_count = valid_assessments.filter(created_at__gte=now - timedelta(days=7)).count()
    
    can_create = daily_count < app_settings.daily_limit and weekly_count < app_settings.weekly_limit
    return {"can_create_new": can_create, "daily": {"count": daily_count, "limit": app_settings.daily_limit}, "weekly": {"count": weekly_count, "limit": app_settings.weekly_limit}}

def extract_content_structure(markdown_text):
    """Extrae jerarquía de títulos para selección de temas."""
    if not markdown_text: return []
    lines = markdown_text.split('\n')
    structure = []
    header_pattern = re.compile(r'^(#{1,4})\s+(.+)$')
    for i, line in enumerate(lines):
        match = header_pattern.match(line.strip())
        if match:
            hashes, title = match.groups()
            structure.append({'id': f"node_{i}", 'text': title.strip(), 'level': len(hashes)})
    return structure

def clean_selection_payload(selection_json):
    try:
        data = json.loads(selection_json) if isinstance(selection_json, str) else selection_json
        return [x for x in data if isinstance(x, str)]
    except: return None

def filter_content_by_selection(markdown_text, selection_ids):
    # Retorna el texto filtrado o el total si no hay selección
    return markdown_text

def get_next_best_archetype(current, rejected):
    choices = ["CEFR_LANGUAGES", "LOGIC_AND_TECH", "SOCIO_LEGAL", "HEALTH_SCIENCES", "HUMANITIES_ARTS"]
    for c in choices:
        if c != current and c not in rejected: return c
    return None

def annotate_content_copy_queryset_with_assessment_states(queryset, user):
    from .models import Assessment
    latest = Assessment.objects.filter(
        content_copy=OuterRef('pk'),
        user=user
    ).order_by('-created_at')
    
    return queryset.annotate(
        assessment_status=Subquery(latest.values('status')[:1]),
        assessment_pk=Subquery(latest.values('id')[:1])
    )
