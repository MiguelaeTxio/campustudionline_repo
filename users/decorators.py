# /users/decorators.py
# ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'

import time
from datetime import date
from functools import wraps

# Imports restaurados a su versión síncrona
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.template import Template, Context


def _render_error_html(title, message):
    """Función auxiliar para renderizar un fragmento HTML de error estandarizado."""
    template_string = """
    <div id="ia-assessment-results" class="alert alert-warning mt-3">
        <h5 class="alert-heading">{{ title }}</h5>
        <p>{{ message }}</p>
    </div>
    """
    context = Context({"title": title, "message": message})
    return Template(template_string).render(context)


def rate_limit_gemini_api(view_func):
    """
    Decorador SÍNCRONO y UNIFICADO para las vistas de IA.
    Maneja:
    1. Autenticación (@login_required)
    2. Método de petición (@require_POST)
    3. Límites de uso (diario y global)
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # --- Lógica de @login_required ---
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Autenticación requerida."}, status=401)

        # --- Lógica de @require_POST ---
        if request.method != "POST":
            return HttpResponseBadRequest(
                "Esta acción solo se permite a través de una petición POST."
            )

        # --- Lógica de Límites ---
        try:
            # Volvemos a la forma de acceso síncrona y directa
            profile = request.user.userprofile
            today = date.today()

            if profile.last_ia_request_date != today:
                profile.ia_requests_today = 0
                profile.last_ia_request_date = today
                profile.save(update_fields=["ia_requests_today", "last_ia_request_date"])

            daily_limit = int(settings.GEMINI_DAILY_REQUESTS_PER_USER)
            if profile.ia_requests_today >= daily_limit:
                msg = f"Has alcanzado tu límite de {daily_limit} consultas de IA por hoy. ¡Vuelve a intentarlo mañana!"
                html_response = _render_error_html(
                    "Límite de Uso Diario Alcanzado", msg
                )
                return HttpResponse(html_response)

        except AttributeError:
            msg = "No se pudo encontrar el profile de usuario. Contacta con soporte."
            html_response = _render_error_html("Error de Perfil", msg)
            return HttpResponse(html_response)

        # La lógica de Redis (cache) es 'sync-friendly', no necesita cambios.
        ppm_limit = int(settings.GEMINI_GLOBAL_PPM)
        cache_key = "gemini_api_global_timestamps"
        now = time.time()
        timestamps = cache.get(cache_key, [])
        recent_timestamps = [t for t in timestamps if now - t < 60]
        if len(recent_timestamps) >= ppm_limit:
            msg = "El servicio está experimentando un alto volumen de peticiones. Por favor, inténtalo de nuevo en un minuto."
            html_response = _render_error_html("Servicio Temporalmente Saturado", msg)
            return HttpResponse(html_response)

        profile.ia_requests_today += 1
        profile.save(update_fields=["ia_requests_today"])
        recent_timestamps.append(now)
        cache.set(cache_key, recent_timestamps, timeout=65)

        # --- Llamada final a la vista síncrona ---
        return view_func(request, *args, **kwargs)

    return wrapper
