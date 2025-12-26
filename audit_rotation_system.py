import os
import django
import inspect
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from orchestrator.models import ApiKey, AutomationSettings

def audit():
    print("--- ESTADO DE LAS CLAVES EN BASE DE DATOS ---")
    keys = ApiKey.objects.all()
    if not keys.exists():
        print("No se encontraron registros en ApiKey.")
    for k in keys:
        status = "HABILITADA" if k.is_enabled else "DESHABILITADA"
        quarantine = "SÍ" if k.is_quarantined else "NO"
        print(f"ID: {k.id} | Name: {k.name} | Status: {status} | Quarantined: {quarantine} | Failures: {k.consecutive_failures}")

    print("\n--- INSPECCIÓN DE MÉTODOS DE ApiKey (Lógica de Rotación) ---")
    # Buscamos métodos que contengan 'quarantine', 'fail' o 'rotation'
    methods = [m[0] for m in inspect.getmembers(ApiKey, predicate=inspect.isfunction)]
    print(f"Métodos en ApiKey: {methods}")

if __name__ == "__main__":
    audit()
