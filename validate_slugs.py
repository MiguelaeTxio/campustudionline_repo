import os
import django
import uuid
from django.utils.text import slugify
from contents.models import ContentMaterial

def run_test():
    print("--- INICIANDO PRUEBA DE INTEGRIDAD DE SLUGS ---")
    
    # Usar un identificador único para evitar colisiones con datos reales previos
    unique_id = uuid.uuid4().hex[:6]
    base_title = f"Test Slug Collision {unique_id}"
    print(f"Título base para la prueba: '{base_title}'")
    
    created_objects = []
    iterations = 5
    
    print(f"Intentando crear {iterations} contenidos con el mismo título...")
    
    for i in range(iterations):
        try:
            content = ContentMaterial.objects.create(
                title=base_title,
                markdown_content=f"Contenido de prueba {i}",
                is_public=False
            )
            created_objects.append(content)
            print(f"  [OK] Creado objeto {i+1} | ID: {content.id} | Slug: '{content.slug}'")
        except Exception as e:
            print(f"  [ERROR] Fallo al crear objeto {i+1}: {e}")

    # Verificación de resultados
    print("\n--- VERIFICACIÓN DE RESULTADOS ---")
    
    expected_base_slug = slugify(base_title)
    slugs_found = [obj.slug for obj in created_objects]
    
    duplicates = len(slugs_found) != len(set(slugs_found))
    
    if duplicates:
        print("❌ FALLO CRÍTICO: Se han detectado slugs duplicados.")
    else:
        print("✅ ÉXITO: Todos los slugs generados son únicos.")

    # Comprobar patrón
    valid_pattern = True
    for idx, slug in enumerate(slugs_found):
        if idx == 0:
            if slug != expected_base_slug:
                print(f"  ⚠️ Aviso: El primer slug '{slug}' no coincide con el esperado '{expected_base_slug}' (posible colisión previa).")
        else:
            if not slug.startswith(expected_base_slug):
                print(f"  ❌ Error: El slug '{slug}' no sigue el patrón esperado.")
                valid_pattern = False
    
    if valid_pattern:
        print("✅ Patrón de generación de slugs correcto.")

    # Limpieza
    print("\n--- LIMPIEZA ---")
    count = 0
    for obj in created_objects:
        obj.delete()
        count += 1
    print(f"Eliminados {count} objetos de prueba.")

# Ejecución incondicional para shell de Django
run_test()
