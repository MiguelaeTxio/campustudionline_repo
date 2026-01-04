import os
import django
import sys
import traceback

# Configurar Django
sys.path.append('/home/MiguelAeTxio/PROJECTS/CampuStudiOnline')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model
from universia.services import UniversiaService
from django.conf import settings

# Forzar depuración imprimiendo variables clave
print("--- UNIVERSIA DIAGNOSTICS ---")
try:
    from schedule.models import AcademicEvent
    print("[OK] Import Schedule models success.")
except Exception as e:
    print(f"[FAIL] Could not import Schedule models: {e}")

try:
    User = get_user_model()
    # Usar el primer superusuario o usuario disponible
    user = User.objects.filter(is_superuser=True).first() or User.objects.first()
    
    if not user:
        print("[FAIL] No users found in database.")
    else:
        print(f"[INFO] Testing with user: {user.username}")
        
        # Ejecución directa del servicio
        print("\n--- ATTEMPTING EXECUTION ---")
        try:
            # Quitamos el catch-all del service hackeando momentáneamente o simplemente ejecutamos y vemos si el print interno de logger salta?
            # El service actual tiene try-except Exception global que devuelve el string error.
            # NO veremos el traceback a menos que 'logger.error' escriba en stdout (que suele estar silenciado en django normal).
            # INTENTO: Llamamos al método interno si es posible o configuramos logger a stdout
            
            # Reconfiguramos logging para ver stderr
            import logging
            logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
            
            # Ejecutamos
            response = UniversiaService.process_user_message(user, "Test message diagnostics", attempt=1)
            print(f"\n[RESULT] Response received: {response}")
            
            if "Error del servicio" in str(response):
                print("\n[ANALYSIS] Service swallowed the error. Please check the STDERR output above for the logging.error traceback.")
                
                # Check for API Keys manual
                from orchestrator.models import ApiKey
                key_count = ApiKey.objects.filter(is_enabled=True).count()
                print(f"[CHECK] Active API Keys in DB: {key_count}")

        except Exception as e:
             traceback.print_exc()

except Exception:
    traceback.print_exc()
