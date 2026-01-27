import markdown
from django.utils.safestring import mark_safe
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

@register.filter(name='render_markdown')
def render_markdown(text):
    """
    Renderiza texto Markdown a HTML seguro.
    Soporta bloques de código (fenced_code) y tablas.
    """
    if not text:
        return ""
    try:
        # Extensions: fenced_code (para ```), tables, nl2br (saltos de línea)
        return mark_safe(markdown.markdown(text, extensions=['fenced_code', 'tables']))
    except Exception:
        return text


@register.simple_tag
def render_cloze_engine(text, response_mode, question_id, external_options=None):
    """
    [HITO 6] Motor de renderizado para preguntas Cloze (Huecos).
    Transforma patrones [opcion1/opcion2] o [...] en widgets HTML.
    """
    import re
    from django.utils.safestring import mark_safe

    if not text:
        return ""

    def replace_callback(match):
        content = match.group(1) # Lo que hay dentro de los corchetes
        
        # Modo DROPDOWN (Select)
        if response_mode == 'REQ_DROP':
            # Estrategia Híbrida:
            # 1. Si hay barras, es un Cloze Inline [op1/op2]
            if '/' in content:
                options = content.split('/')
            # 2. Si no, usamos las opciones externas (si existen)
            elif external_options and isinstance(external_options, list):
                options = external_options
            else:
                # Fallback final: usar el contenido tal cual (ej: [...])
                options = [content]

            options_html = f'<option value="" selected disabled>---</option>'
            for opt in options:
                opt = str(opt).strip()
                # Limpieza extra de comillas si se colaron
                opt = opt.replace('"', '&quot;')
                options_html += f'<option value="{opt}">{opt}</option>'
            
            # Usamos un nombre de array para capturar múltiples respuestas: answer_q_ID_cloze[]
            return f'<select name="answer_q_{question_id}_cloze[]" class="form-select d-inline-block w-auto mx-1 border-primary bg-light fw-bold text-primary" style="min-width: 120px;">{options_html}</select>'
        
        # Modo INPUT (Caja de texto)
        elif response_mode == 'REQ_INPUT':
            # Ignoramos el contenido del corchete visualmente y mostramos input vacío
            return f'<input type="text" name="answer_q_{question_id}_cloze[]" class="form-control d-inline-block w-auto mx-1 border-primary bg-light text-center fw-bold" style="min-width: 140px; max-width: 200px;" placeholder="...">'
        

    # Regex para capturar contenido entre corchetes: [algo]
    pattern = r'\[(.*?)\]'
    rendered_text = re.sub(pattern, replace_callback, text)
    
    return mark_safe(rendered_text)
