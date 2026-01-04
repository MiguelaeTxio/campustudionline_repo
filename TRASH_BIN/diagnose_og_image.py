import os
import sys
import django
from django.conf import settings

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from contents.utils import generate_share_image_bytes

def run_diagnosis():
    print("--- INICIANDO DIAGNÓSTICO DE GENERACIÓN DE IMAGEN OG ---")
    
    # 1. Verificación de Variables y Rutas Estáticas
    print(f"\n[1] Verificación de Entorno:")
    print(f"STATIC_ROOT configurado: {settings.STATIC_ROOT}")
    
    resources = [
        ("Fuente Regular", os.path.join(settings.STATIC_ROOT, "fonts/Roboto-Regular.ttf")),
        ("Fuente Bold", os.path.join(settings.STATIC_ROOT, "fonts/Roboto-Bold.ttf")),
        ("Logo SVG", os.path.join(settings.STATIC_ROOT, "images/favicon.svg")),
        ("Logo PNG", os.path.join(settings.STATIC_ROOT, "images/favicon-96x96.png")),
        ("Template Share Card", os.path.join(settings.BASE_DIR, "contents/templates/contents/share_card_template.html")),
    ]
    
    all_resources_exist = True
    for name, path in resources:
        exists = os.path.exists(path)
        status = "OK" if exists else "FALTA"
        print(f"  - {name}: {status} -> {path}")
        if not exists:
            all_resources_exist = False

    if not all_resources_exist:
        print("\nCRÍTICO: Faltan recursos estáticos necesarios. La generación fallará.")
    
    # 2. Prueba de Generación
    print(f"\n[2] Prueba de Ejecución de 'generate_share_image_bytes':")
    try:
        context = {
            "title": "Diagnóstico de OpenGraph",
            "author": "Sistema de Diagnóstico"
        }
        print("  - Llamando a la función...")
        png_bytes = generate_share_image_bytes(context)
        
        if png_bytes and len(png_bytes) > 0:
            print(f"  - ÉXITO: Imagen generada. Tamaño: {len(png_bytes)} bytes.")
            output_file = "diagnostic_share_image.png"
            with open(output_file, "wb") as f:
                f.write(png_bytes)
            print(f"  - Imagen guardada en: {os.path.abspath(output_file)}")
        else:
            print("  - FALLO: La función devolvió None o bytes vacíos.")
            
    except Exception as e:
        print(f"  - EXCEPCIÓN NO CONTROLADA: {e}")
        import traceback
        traceback.print_exc()

    print("\n--- DIAGNÓSTICO FINALIZADO ---")

if __name__ == "__main__":
    run_diagnosis()
