import os
import django
import sys

sys.path.append('/home/MiguelAeTxio/PROJECTS/CampuStudiOnline')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from orchestrator.models import PendingContentTask, AutomationSettings
from assessment.models import Assessment
from contents.models import ContentMaterial

print("--- ESTADO DEL SISTEMA DE GENERACIÓN ---")
settings = AutomationSettings.load()
print(f"Automatización Global Activada: {settings.is_running}")
print(f"Clave API Activa: {settings.active_api_key}")

print("\n--- TAREAS DE CONTENIDO (PendingContentTask) ---")
tasks = PendingContentTask.objects.all().order_by('-created_at')[:5]
if not tasks:
    print("No hay tareas recientes.")
for t in tasks:
    print(f"ID: {t.id} | Asignatura: {t.subject} | Estado: {t.status} | Origen: {t.task_origin}")
    print(f"   > Material Generado: {t.content_material}")
    print(f"   > Log interno (última entrada): {t.task_log[-1] if t.task_log else 'VACÍO'}")

print("\n--- EVALUACIONES (Assessment) ---")
assessments = Assessment.objects.all().order_by('-created_at')[:5]
if not assessments:
    print("No hay evaluaciones recientes.")
for a in assessments:
    print(f"ID: {a.id} | Estado: {a.status} | Material Origen: {a.content_material}")

print("\n--- CONTENIDO REAL (ContentMaterial) ---")
contents = ContentMaterial.objects.all().order_by('-created_at')[:5]
for c in contents:
    print(f"ID: {c.id} | Título: {c.title} | Público: {c.is_public}")
