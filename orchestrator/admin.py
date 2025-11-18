# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/admin.py
import json
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, include, reverse
from django.utils.html import format_html

from .models import ApiKey, AutomationSettings, PendingContentTask, ContentRequest, FreeContentRequest
from .tasks import generate_full_course_task
from .forms import RejectionReasonForm

# El resto de las clases Admin...
# ... (código omitido por brevedad)

@admin.register(PendingContentTask)
class PendingContentTaskAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include('orchestrator.admin_urls')),
        ]
        return custom_urls + urls
    # El resto del código de la clase no cambia...
