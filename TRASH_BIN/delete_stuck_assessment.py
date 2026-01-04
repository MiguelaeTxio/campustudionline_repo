import os
import django
import sys

sys.path.append('/home/MiguelAeTxio/PROJECTS/CampuStudiOnline')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from assessment.models import Assessment

target_id = 158

try:
    assessment = Assessment.objects.get(id=target_id)
    print(f"Encontrada evaluación atascada: ID {assessment.id} - Estado: {assessment.status}")
    assessment.delete()
    print(f"Evaluación {target_id} eliminada correctamente de la base de datos.")
except Assessment.DoesNotExist:
    print(f"La evaluación {target_id} no existe (ya fue borrada).")
except Exception as e:
    print(f"Error al borrar: {e}")
