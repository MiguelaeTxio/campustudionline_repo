import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from orchestrator.models import ApiKey, AutomationSettings

def audit():
    print("--- ESTADO ACTUAL DE CLAVES ---")
    keys = ApiKey.objects.all()
    for k in keys:
        print(f"Key: {k.name} | Enabled: {k.is_enabled} | Quarantined: {k.is_quarantined} | Failures: {k.consecutive_failures}")
    
    config = AutomationSettings.load()
    active = config.active_api_key.name if config.active_api_key else "None"
    print(f"\nConfiguración global - Clave Activa: {active}")

if __name__ == "__main__":
    audit()
