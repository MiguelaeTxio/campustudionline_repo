import logging
from django.views.generic import FormView, View
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from .forms import TranslationForm
from .services import TranslationService

logger = logging.getLogger(__name__)

class TranslationHomeView(FormView):
    template_name = 'translation_room/translation_home.html'
    form_class = TranslationForm

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

class TranslationStreamView(View):
    """Vista dedicada exclusivamente a manejar el stream de datos."""
    
    def post(self, request, *args, **kwargs):
        form = TranslationForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data.get('text_content', '')
            doc = form.cleaned_data.get('document')
            source = form.cleaned_data.get('source_lang')
            # Convertir código a nombre legible para el prompt si es 'auto'
            source_display = dict(form.fields['source_lang'].choices).get(source, source)
            
            target = dict(form.fields['target_lang'].choices).get(form.cleaned_data['target_lang'])

            # Prioridad al documento
            if doc:
                try:
                    ext = '.' + doc.name.split('.')[-1]
                    file_text = TranslationService.extract_text_from_file(doc, ext)
                    text = f"{text}\n\n{file_text}".strip()
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=400)

            if not text:
                return JsonResponse({'error': 'No hay texto para traducir.'}, status=400)

            # Generador Streaming
            def event_stream():
                for chunk in TranslationService.stream_translation(text, target, request.user, source_display):
                    # Formato SSE (Server-Sent Events) simple o chunked text
                    yield chunk

            return StreamingHttpResponse(event_stream(), content_type='text/plain')
        
        return JsonResponse({'error': 'Formulario inválido'}, status=400)
