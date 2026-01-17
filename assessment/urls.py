from django.urls import path
from . import views

app_name = "assessment"

urlpatterns = [
    # --- FASE 1: Configuración y Generación ---
    # Paso 1: Configurar parámetros (Selección de temas)
    path("copy/<uuid:copy_pk>/configure/", views.configure_assessment, name="configure_assessment"),
    
    # Paso 2: Lanzar generación (Action POST)
    path("copy/<uuid:copy_pk>/generate/", views.generate_ai_assessment, name="generate_ai_assessment"),
    
    # --- Flujo de Realización ---
    path("<int:pk>/take/", views.take_assessment, name="take_assessment"),
    path("<int:pk>/submit/", views.submit_assessment, name="submit_assessment"),
    
    # --- Resultados ---
    path("<int:pk>/results/", views.view_results, name="view_results"),
    
    # --- Utilidades AJAX / API ---
    path("status/<int:assessment_pk>/", views.get_assessment_status, name="get_assessment_status"),
    path("panel/<uuid:copy_pk>/", views.get_assessment_panel_content, name="get_assessment_panel_content"),
    path("<int:pk>/mark-viewed/", views.mark_as_viewed_ajax, name="mark_as_viewed_ajax"),
    
    # --- Acciones de Control ---
    path("<int:assessment_pk>/retry/", views.retry_assessment_generation, name="retry_assessment_generation"),
        path("<int:assessment_pk>/cancel/", views.cancel_assessment_generation, name="cancel_assessment_generation"),
    path("<int:pk>/report-archetype/", views.report_wrong_archetype, name="report_wrong_archetype"),
    
    # --- Demo (Dev only) ---
    path("demo/take/", views.take_assessment_demo, name="take_assessment_demo"),
]
