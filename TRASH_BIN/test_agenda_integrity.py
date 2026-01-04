import os
import sys
import django
import traceback

sys.path.append('/home/MiguelAeTxio/PROJECTS/CampuStudiOnline')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model
from schedule.models import AcademicEvent
from django.utils import timezone

User = get_user_model()
user = User.objects.filter(is_active=True).first()

print(f"--- INICIANDO TEST DE INTEGRIDAD DE AGENDA ---")
print(f"Usuario: {user.username}")

try:
    # Intentamos crear el evento exactamente como lo hace UniversIA
    # Esto disparará cualquier signal de post_save
    event = AcademicEvent.objects.create(
        user=user,
        title="Test de Señales UniversIA",
        start_time=timezone.now(),
        end_time=timezone.now() + timezone.timedelta(minutes=30),
        event_type='PE',
        description="Prueba técnica de integridad"
    )
    print("[OK] Evento creado sin errores. Los signals parecen estar sanos.")
    # Limpiamos
    event.delete()
except Exception:
    print("\n[!!!] CRASH DETECTADO AL CREAR EVENTO:")
    traceback.print_exc()
