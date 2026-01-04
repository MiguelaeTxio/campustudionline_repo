import os
import django
from django.utils import timezone
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from schedule.models import AcademicEvent
from django.conf import settings

def audit():
    print(f"--- CONFIGURACIÓN DE TIEMPO ---")
    print(f"TIME_ZONE: {settings.TIME_ZONE}")
    print(f"USE_TZ: {settings.USE_TZ}")
    print(f"Hora actual (timezone.now()): {timezone.now()}")
    print(f"Hora actual (datetime.now()): {datetime.datetime.now()}")

    print("\n--- ÚLTIMOS EVENTOS CREADOS ---")
    events = AcademicEvent.objects.order_by('-created_at')[:5]
    for e in events:
        print(f"ID: {e.id} | Titulo: {e.title} | Start: {e.start_time} | End: {e.end_time} | Created: {e.created_at}")

if __name__ == "__main__":
    audit()
