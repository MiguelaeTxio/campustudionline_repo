import os
import sys
import django

# Setup Django
sys.path.append('/home/MiguelAeTxio/PROJECTS/CampuStudiOnline')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model
from universia.services import UniversiaService

User = get_user_model()
user = User.objects.filter(is_superuser=True).first() or User.objects.first()

print(f"--- TESTING FULL SERVICE FOR USER: {user.username} ---")

# Forzamos la ejecución SIN el try/except del servicio para ver el crash real
# O capturamos y usamos traceback
import traceback

try:
    # Llamada al servicio real
    result = UniversiaService.process_user_message(user, "Hola UniversIA", context_url="/")
    print(f"Resultado: {result}")
    
    if result.get('text') == "Error del servicio.":
        print("\n[DETECTADO] El servicio devolvió el error genérico. Vamos a buscar la causa real en el código...")
        # Intentamos una operación de base de datos manual idéntica a la del servicio
        from universia.models import UniversiaSession, UniversiaMessage
        session = UniversiaService.get_or_create_session(user)
        print("[OK] Sesión obtenida.")
        
        print("Intentando guardar mensaje de prueba con context_url...")
        msg = UniversiaMessage.objects.create(
            session=session,
            role='user',
            content='Test',
            context_url='/'
        )
        print("[OK] Mensaje guardado exitosamente.")
        
except Exception:
    print("\n--- CRASH REAL DETECTADO ---")
    traceback.print_exc()

