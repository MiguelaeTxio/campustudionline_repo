# /home/MiguelAeTxio/CampuStudiOnline/core/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import TemplateView

from .context_processors import global_context

@login_required
def update_navbar_indicators(request):
    """
    HTMX view to update the notification indicators in the navbar.
    It returns only the HTML fragment of the indicators.
    """
    if not request.htmx:
        # Prevent direct access to this URL, it's for HTMX only
        return HttpResponse(status=400)

    # We manually call the global_context processor to get the updated counts
    context = global_context(request)
    return render(request, "core/partials/_navbar_indicators.html", context)


# --- Legal Views ---
class LegalNoticeView(TemplateView):
    template_name = "core/legal/legal_notice.html"

class PrivacyPolicyView(TemplateView):
    template_name = "core/legal/privacy_policy.html"

class CookiesPolicyView(TemplateView):
    template_name = "core/legal/cookies_policy.html"
