import os
import django

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from contents.models import ContentMaterial

def fix_visibility():
    print("--- INICIO DE REPARACIÓN DE VISIBILIDAD ---")
    
    # Buscar contenido libre que NO es público
    targets = ContentMaterial.objects.filter(is_free_content=True, is_public=False)
    count = targets.count()
    
    if count == 0:
        print("✅ No se encontró contenido libre oculto. Todo está correcto.")
    else:
        print(f"⚠️  Se encontraron {count} materiales libres ocultos.")
        print("🔄 Aplicando corrección (is_public=True)...")
        
        # Actualización masiva
        updated = targets.update(is_public=True)
        
        print(f"✅ ¡ÉXITO! Se han hecho públicos {updated} materiales.")

    print("--- FIN ---")

if __name__ == '__main__':
    fix_visibility()
