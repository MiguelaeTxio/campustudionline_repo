# /home/MiguelAeTxio/CampuStudiOnline/assessment/templatetags/assessment_tags.py
from django import template
from assessment.models import Assessment

register = template.Library()

@register.inclusion_tag('assessment/partials/_assessment_indicator_badge.html')
def render_assessment_indicators(obj):
    """
    [V3 - REFACTORIZADO Y UNIFICADO]
    Renderiza los indicadores de estado para las evaluaciones asociadas a un objeto.
    Este tag ahora espera que el objeto venga ANOTADO desde la vista con los campos:
    - latest_assessment_status
    - latest_assessment_pk
    - num_assessments (opcional, para mostrar el contador)
    """
    status = getattr(obj, 'latest_assessment_status', None)
    pk = getattr(obj, 'latest_assessment_pk', None)
    count = getattr(obj, 'num_assessments', 0)

    iv_data = None
    if status:
        iv_data = {
            "status": status,
            "pk": pk,
            "count": count
        }
        
    return {'iv_data': iv_data}
