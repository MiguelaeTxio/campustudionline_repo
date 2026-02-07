# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/feedback/urls.py
from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('report/content/<uuid:content_pk>/', views.report_content_error, name='report_content_error'),
    path('general/', views.submit_general_feedback, name='submit_general_feedback'),
    # [CLEANUP HITO 6] Ruta manual_format_request eliminada por obsolescencia
]
