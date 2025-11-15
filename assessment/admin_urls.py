# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment/admin_urls.py
from django.urls import path
from . import admin_views

# El namespace será 'admin' y el app_name se resolverá a 'assessment'
# por cómo Django carga estos URLs.
urlpatterns = [
    path(
        "dashboard/",
        admin_views.assessment_dashboard,
        name="assessment_dashboard"
    ),
    path(
        "dashboard/toggle-engine/",
        admin_views.toggle_assessment_engine,
        name="assessment_toggle_engine"
    ),
    path(
        "task/<int:pk>/pause/",
        admin_views.pause_assessment_task,
        name="assessment_pause_task"
    ),
    path(
        "task/<int:pk>/resume/",
        admin_views.resume_assessment_task,
        name="assessment_resume_task"
    ),
    path(
        "task/<int:pk>/retry/",
        admin_views.retry_failed_task,
        name="assessment_retry_task"
    ),
]
