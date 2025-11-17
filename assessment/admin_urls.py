# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment/admin_urls.py
from django.urls import path
from . import admin_views

app_name = 'assessment_admin'

urlpatterns = [
    path(
        "dashboard/",
        admin_views.assessment_dashboard,
        name="assessment_dashboard"
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
        "task/<int:pk>/cancel/",
        admin_views.cancel_assessment_task,
        name="assessment_cancel_task"
    ),
    path(
        "task/<int:pk>/log/",
        admin_views.view_assessment_log,
        name="assessment_view_log"
    ),
]
