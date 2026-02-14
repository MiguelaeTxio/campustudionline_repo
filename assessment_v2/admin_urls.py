# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/admin_urls.py
from django.urls import path
from . import admin_views

app_name = 'assessment_admin'

urlpatterns = [
    path('dashboard/', admin_views.assessment_dashboard_view, name='assessment_dashboard'),
    path('pause-task/<int:pk>/', admin_views.pause_exam_task, name='assessment_pause_task'),
]
