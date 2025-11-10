# /home/MiguelAeTxio/CampuStudiOnline/assessment/urls.py
from django.urls import path
from . import views

app_name = "assessment"

urlpatterns = [
    path(
        "tour/take-assessment-demo/",
        views.take_assessment_demo,
        name="take_assessment_demo",
    ),
    path(
        "generate/<uuid:copy_pk>/",
        views.generate_ai_assessment,
        name="generate_ai_assessment",
    ),
    path(
        "status/<int:assessment_pk>/",
        views.get_assessment_status,
        name="get_assessment_status",
    ),
    path(
        "panel-content/<uuid:copy_pk>/",
        views.get_assessment_panel_content,
        name="get_assessment_panel_content",
    ),
    path("<int:pk>/", views.take_assessment, name="take_assessment"),
    path("<int:pk>/submit/", views.submit_assessment, name="submit_assessment"),
    path("results/<int:pk>/", views.view_results, name="view_results"),
    path(
        "retry/<int:assessment_pk>/",
        views.retry_assessment_generation,
        name="retry_assessment_generation",
    ),
    path(
        "cancel/<int:assessment_pk>/",
        views.cancel_assessment_generation,
        name="cancel_assessment_generation",
    ),
    path(
        "mark-as-viewed/<int:pk>/",
        views.mark_as_viewed_ajax,
        name="mark_as_viewed_ajax",
    ),
]
