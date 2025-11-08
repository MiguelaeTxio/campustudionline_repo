# /home/MiguelAeTxio/CampuStudiOnline/academic_directory/urls.py
from django.urls import path
from . import views

app_name = "academic_directory"

urlpatterns = [
    # --- Ruta de Prueba para Depuración de Estilos ---

    # --- Endpoint de Acción para Solicitudes ---
    # NOTE: This path must be defined BEFORE the dynamic slug paths to be correctly resolved.
    path('request-content/', views.request_content_view, name='request_content'),
    
    # Nivel 1: Lista de Universidades
    path("", views.university_list_view, name="university_list"),
    # Nivel 2: Lista de Ramas para una Universidad
    path("<slug:university_slug>/", views.branch_list_view, name="branch_list"),
    # Nivel 3: Lista de Titulaciones para una Rama
    path(
        "<slug:university_slug>/<slug:branch_slug>/",
        views.degree_list_view,
        name="degree_list",
    ),
    # Nivel 4: Lista de Años Académicos para una Titulación
    path(
        "<slug:university_slug>/<slug:branch_slug>/<slug:degree_slug>/",
        views.academic_year_list_view,
        name="academic_year_list",
    ),
    # Nivel 5: Lista de Asignaturas para un Año Académico
    path(
        "<slug:university_slug>/<slug:branch_slug>/<slug:degree_slug>/<int:year>/",
        views.subject_list_view,
        name="subject_list",
    ),
    # Nivel 6: Lista de Contenidos Públicos para una Asignatura
    path(
        "<slug:university_slug>/<slug:branch_slug>/<slug:degree_slug>/<int:year>/<slug:subject_slug>/",
        views.public_content_list_view,
        name="public_content_list",
    ),
]
