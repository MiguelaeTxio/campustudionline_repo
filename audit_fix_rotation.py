import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from orchestrator.models import ApiKey, AutomationSettings
import inspect

def audit():
    print("--- ESTADO DE LAS CLAVES EN DB ---")
    for k in ApiKey.objects.all():
        status = "ACTIVA" if k.is_enabled and not k.is_quarantined else "BLOQUEADA/CUARENTENA"
        print(f"ID: {k.id} | Name: {k.name} | Status: {status} | Failures: {k.consecutive_failures}")

    print("\n--- INSPECCIÓN DE MÉTODOS DE ApiKey ---")
    methods = [m[0] for m in inspect.getmembers(ApiKey, predicate=inspect.isfunction)]
    print(f"Métodos disponibles en ApiKey: {methods}")

if __name__ == "__main__":
    audit()
