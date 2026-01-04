import django
import os
import sys

# Configurar entorno
sys.path.append('/home/MiguelAeTxio/PROJECTS/CampuStudiOnline')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from orchestrator.models import PendingContentTask, AutomationSettings

def check_integrity():
    print("--- INICIO AUDITORÍA DE MODELOS (HITO 24) ---")
    
    # 1. Verificar PendingContentTask
    print("\n[PendingContentTask] Verificando campos de resiliencia...")
    task_fields = [f.name for f in PendingContentTask._meta.get_fields()]
    required_task_fields = [
        'global_actuation_count', 
        'consecutive_api_errors', 
        'last_api_error_at', 
        'last_error_api_key', 
        'current_step', 
        'last_heartbeat'
    ]
    
    all_ok = True
    for field in required_task_fields:
        if field in task_fields:
            print(f"  OK: Campo '{field}' detectado.")
        else:
            print(f"  ERROR: Campo '{field}' NO detectado.")
            all_ok = False
            
    # 2. Verificar AutomationSettings
    print("\n[AutomationSettings] Verificando parámetros de configuración...")
    settings_fields = [f.name for f in AutomationSettings._meta.get_fields()]
    required_settings_fields = [
        'max_task_actuations',
        'max_consecutive_api_errors',
        'zombie_task_threshold_hours'
    ]
    
    for field in required_settings_fields:
        if field in settings_fields:
            print(f"  OK: Campo '{field}' detectado.")
        else:
            print(f"  ERROR: Campo '{field}' NO detectado.")
            all_ok = False

    if all_ok:
        print("\n>>> INTEGRIDAD DE ESQUEMA VERIFICADA: TODOS LOS CAMPOS PRESENTES.")
    else:
        print("\n>>> FALLO DE INTEGRIDAD: FALTAN CAMPOS.")

if __name__ == "__main__":
    check_integrity()
