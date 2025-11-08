# /home/MiguelAeTxio/CampuStudiOnline/content_automation/urls.py
from django.urls import path
from . import views

app_name = 'content_automation'

urlpatterns = [
    # --- Vistas de Usuario Final ---
    path(
        "",
        views.request_free_content_view,
        name="request_free_content",
    ),
]
