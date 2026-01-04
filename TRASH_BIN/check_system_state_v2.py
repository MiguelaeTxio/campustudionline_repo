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
    print(f"ID: {t.id} | Asignatura: {t.subject} | Estado: {t.status}")
    print(f"   > Material Generado: {t.content_material}")
    # Imprimir las últimas 3 líneas del log para ver pistas
    if t.task_log:
        print("   > Últimos logs:")
        for entry in t.task_log[-3:]:
            print(f"     - {entry}")
    else:
        print("   > Log interno VACÍO")

print("\n--- EVALUACIONES (Assessment) ---")
assessments = Assessment.objects.all().order_by('-created_at')[:5]
if not assessments:
    print("No hay evaluaciones recientes.")
for a in assessments:
    # CORRECCIÓN: Usar a.content en lugar de a.content_material
    print(f"ID: {a.id} | Estado: {a.status} | Material Origen: {a.content.title if a.content else 'N/A'}")
    print(f"   > Error Registrado: {a.last_error}")

print("\n--- CONTENIDO REAL (ContentMaterial) ---")
contents = ContentMaterial.objects.all().order_by('-created_at')[:5]
if not contents:
    print("No hay contenido reciente.")
for c in contents:
    print(f"ID: {c.id} | Título: {c.title} | Público: {c.is_public}")
