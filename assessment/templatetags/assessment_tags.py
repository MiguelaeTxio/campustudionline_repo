# /home/MiguelAeTxio/CampuStudiOnline/assessment/templatetags/assessment_tags.py
from django import template
from assessment.models import Assessment

register = template.Library()

@register.inclusion_tag('assessment/partials/_assessment_indicator_badge.html')
def render_assessment_indicators(obj):
    """
    [V4 - CORRECCIÓN DEFINITIVA]
    Renderiza los indicadores de estado para las evaluaciones asociadas a un objeto.
    Este tag ahora actúa como un passthrough directo, esperando que el objeto
    venga anotado desde la vista con los campos:
    - assessment_state
    - latest_assessment_pk
    """
    # Lee los nombres de atributo correctos que vienen de las funciones de anotación.
    assessment_state = getattr(obj, 'assessment_state', None)
    latest_assessment_pk = getattr(obj, 'latest_assessment_pk', None)

    # Pasa las variables directamente a la plantilla, alineando el contrato.
    return {
        'assessment_state': assessment_state,
        'latest_assessment_pk': latest_assessment_pk
    }
