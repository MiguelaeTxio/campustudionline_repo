import markdown
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from .services import UniversiaService
from .models import UniversiaSession


def _render_markdown(text):
    """Convierte markdown a HTML seguro para el chat."""
    try:
        return markdown.markdown(text, extensions=['nl2br', 'fenced_code', 'extra'])
    except Exception:
        return text


@require_POST
@login_required
def chat_api(request):
    """API Endpoint para enviar mensajes a UniversIA."""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        context_url = data.get('context_url', None)
        context_title = data.get('context_title', 'Material de Estudio')

        if not message:
            return JsonResponse({'error': 'El mensaje no puede estar vacío.'}, status=400)

        response_text = UniversiaService.process_user_message(request.user, message, context_url, context_title)
        
        return JsonResponse({
            'response': _render_markdown(response_text),
            'status': 'success'
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_GET
@login_required
def get_history_api(request):
    """Devuelve el historial de la sesión activa con contenido renderizado."""
    session = UniversiaSession.objects.filter(user=request.user, is_active=True).first()
    if not session:
        return JsonResponse({'messages': []})

    messages_data = []
    for msg in session.messages.order_by('timestamp'):
        content = msg.content
        rendered_content = _render_markdown(content)
        
        messages_data.append({
            'role': msg.role,
            'content': rendered_content,
            'timestamp': msg.timestamp
        })

    return JsonResponse({'messages': messages_data})