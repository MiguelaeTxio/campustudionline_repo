# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/content_automation/views.py
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from orchestrator.forms import FreeContentRequestForm

@login_required
def request_free_content_view(request: HttpRequest) -> HttpResponse:
    """Vista para que los usuarios soliciten contenido libre (no-admin)."""
    form = FreeContentRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.instance.requester = request.user
        form.save()
        return HttpResponseRedirect(reverse("search:search_home"))
    return render(request, "content_automation/request_free_content.html", {"form": form})
