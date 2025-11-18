# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/admin_urls.py
from django.urls import path
from . import admin_views as views

app_name = "orchestrator"

urlpatterns = [
    path("dashboard/", views.task_dashboard_view, name="task_dashboard"),
    path("automation-control/", views.automation_control_view, name="automation_control_center"),
    path("toggle-automation-status/", views.toggle_automation_status_view, name="toggle_automation_status"),
    path("set-active-api-key/", views.set_active_api_key_view, name="set_active_api_key"),
    path("set-seed-filters/", views.set_seed_filters_view, name="set_seed_filters"),
    path("tasks/create-academic/", views.create_academic_task_view, name="create_academic_task"),
    path("tasks/create-free/", views.create_free_task_view, name="create_free_task"),
    path('tasks/<uuid:task_id>/log/', views.task_log_full_page_view, name='task_log_full_page'),
    path('tasks/<uuid:task_id>/pause/', views.pause_task_view, name='pause_task'),
    path('tasks/<uuid:task_id>/resume/', views.resume_task_view, name='resume_task'),
    path('tasks/<uuid:task_id>/cancel/', views.cancel_task_view, name='cancel_task'),
    path('tasks/<uuid:task_id>/revise/', views.revise_and_regenerate_view, name='revise_and_regenerate'),
    path('requests/free/<uuid:request_id>/reject/', views.reject_free_request_view, name='reject_free_request'),
    path('requests/free/<uuid:request_id>/delete/', views.delete_free_request_view, name='delete_free_request'),
    path('maintenance/logs/', views.manage_logs_view, name='manage_logs'),
    path("modal-log-content/<uuid:task_id>/", views.get_modal_log_content_view, name="get_modal_log_content"),
    path("get-automation-status/", views.get_automation_status_view, name="get_automation_status"),
    path('task-row-partial/<uuid:task_id>/', views.task_row_partial_view, name='task_row_partial'),
    path('academic-filters/', views.get_academic_filters_htmx, name='get_academic_filters'),
    path('get-sub-categories/', views.get_sub_categories_htmx, name='get_sub_categories_for_master'),
]
