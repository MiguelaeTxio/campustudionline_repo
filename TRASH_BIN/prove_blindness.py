import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from assessment.models import Assessment
from contents.models import ContentCopy

# 1. BUSCAR EL CASO REAL (Cálculo I)
copy = ContentCopy.objects.filter(
    user__username="CampuStudiOnline", 
    original_content__title__icontains="Cálculo I"
).first()

if not copy:
    print("No se encontró la copia de Cálculo I para CampuStudiOnline")
    exit()

print(f"\n--- ANÁLISIS FORENSE: {copy.original_content.title} ---")

# 2. LA VERDAD (Base de Datos)
latest = Assessment.objects.filter(content_copy=copy).order_by('-created_at').first()
if not latest:
    print("La BD dice: No hay evaluaciones.")
    exit()

print(f"1. REALIDAD (Base de Datos):")
print(f"   Estado Actual: [{latest.status}]")
print(f"   ID: {latest.id}")

# 3. EL FILTRO ACTUAL (La lógica ciega de file10.py)
visible_statuses = [
    'PENDING', 'PROCESSING', 'COMPLETED', 
    'AWAITING_CORRECTION', 'CORRECTING', 'RESULTS_AVAILABLE'
]
# NOTA: GENERATION_FAILED_QUOTA no está aquí. CANCELLED no está aquí.

is_visible = latest.status in visible_statuses

print(f"\n2. LÓGICA DE LA SIDEBAR:")
print(f"   ¿Está '{latest.status}' en la lista permitida? -> {is_visible}")

if not is_visible:
    print("\n>>> CONCLUSIÓN: El Builder IGNORA esta evaluación.")
    print(">>> RESULTADO VISUAL: Icono desaparecido (Inconsistencia probada).")
else:
    print("\n>>> CONCLUSIÓN: El Builder debería verla. El problema está en otro lado.")
