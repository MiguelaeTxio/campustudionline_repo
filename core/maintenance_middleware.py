from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from global_settings.models import MaintenanceSettings

ALLOWED_IPS_MAINTENANCE = getattr(settings, "MAINTENANCE_MODE_ALLOWED_IPS", [])


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            settings_obj = MaintenanceSettings.get_settings()
            is_maintenance_mode = settings_obj.maintenance_mode_active
        except Exception:
            is_maintenance_mode = False

        if not is_maintenance_mode:
            return self.get_response(request)

        # --- MAINTENANCE LOGIC (SIMPLIFIED AND FINAL VERSION) ---

        # RULE 1: THE ADMIN LOGIN PAGE IS ALWAYS ACCESSIBLE
        try:
            admin_login_url = reverse("admin:login")
            if request.path_info == admin_login_url:
                return self.get_response(request)
        except Exception:
            pass  # Continue if there is an error resolving the URL

        # RULE 2: AUTHENTICATED STAFF HAVE ACCESS TO EVERYTHING
        if (
            hasattr(request, "user")
            and request.user.is_authenticated
            and request.user.is_staff
        ):
            return self.get_response(request)

        # RULE 3: AUTHORIZED IPs HAVE ACCESS
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        client_ip = (
            x_forwarded_for.split(",")[0].strip()
            if x_forwarded_for
            else request.META.get("REMOTE_ADDR")
        )

        if client_ip in ALLOWED_IPS_MAINTENANCE:
            return self.get_response(request)

        # If no exception is met, the maintenance page is displayed.
        rendered_template = render(request, "maintenance.html")
        response = HttpResponse(rendered_template.content, status=503)
        return response
