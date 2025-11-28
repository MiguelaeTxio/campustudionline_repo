import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from orchestrator.models import AutomationSettings, PendingContentTask, ApiKey
from academic_structure.models import Subject
from orchestrator.tasks import _get_next_subject_queryset

def diagnose():
    print("\n--- DIAGNÓSTICO DEL MOTOR DE AUTOMATIZACIÓN ---\n")
    
    # 1. Verificar Interruptor Maestro
    try:
        settings = AutomationSettings.load()
        print(f"1. INTERRUPTOR MAESTRO: {'ENCENDIDO ✅' if settings.is_running else 'APAGADO ❌'}")
        print(f"   Último Estado Registrado: '{settings.last_run_status}'")
    except Exception as e:
        print(f"1. ERROR LEYENDO SETTINGS: {e}")

    # 2. Verificar Tareas Bloqueantes
    active_tasks = PendingContentTask.objects.filter(
        status__in=[PendingContentTask.StatusChoices.PROCESSING, PendingContentTask.StatusChoices.PENDING]
    )
    count = active_tasks.count()
    print(f"\n2. TAREAS ACTIVAS (BLOQUEANTES): {count}")
    if count > 0:
        for t in active_tasks:
            print(f"   - [{t.get_status_display()}] {t.course_title or t.subject} (ID: {t.id})")
    else:
        print("   (El carril de ejecución está libre)")

    # 3. Verificar Claves API
    active_key = settings.active_api_key
    valid_keys = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).count()
    print(f"\n3. CLAVES API:")
    print(f"   - Clave Activa Asignada: {active_key.name if active_key else 'NINGUNA ❌'}")
    print(f"   - Claves Disponibles en Pool: {valid_keys}")

    # 4. Verificar Disponibilidad de Trabajo (Tolva)
    print(f"\n4. FILTROS DE SEMILLA (CONFIGURACIÓN):")
    print(f"   - Rama: {settings.seed_branch}")
    print(f"   - Grado: {settings.seed_degree}")
    print(f"   - Año: {settings.seed_year}")
    
    subjects_in_queue = _get_next_subject_queryset(settings).count()
    print(f"\n5. DISPONIBILIDAD DE TRABAJO:")
    print(f"   - Asignaturas pendientes que coinciden con los filtros: {subjects_in_queue}")

    print("\n--- CONCLUSIÓN ---")
    if not settings.is_running:
        print("🔴 CAUSA: El sistema está apagado manualmente.")
    elif count > 0:
        print("🟠 CAUSA: Hay tareas atascadas bloqueando la cola.")
    elif valid_keys == 0:
        print("🔴 CAUSA: No hay claves API válidas (todas en cuarentena o deshabilitadas).")
    elif subjects_in_queue == 0:
        print("🟡 CAUSA: Se han agotado las asignaturas para los filtros actuales (Semillas).")
    else:
        print("🟢 ESTADO: El sistema debería estar generando. Si no lo hace, revisa los logs de Celery.")

if __name__ == '__main__':
    diagnose()
