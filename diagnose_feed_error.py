import os
import time
import django
from django.test import Client
from django.conf import settings

# Configuración
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Permitir testserver
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + ['testserver']

def check_feed():
    print("--- Iniciando diagnóstico del Feed ---")
    client = Client()
    start_time = time.time()
    
    try:
        # Simulamos la petición
        response = client.get('/contents/feed/meta-catalog/')
        duration = time.time() - start_time
        
        if response.status_code == 200:
            content_size = len(response.content)
            print(f"✅ ÉXITO: El feed se generó correctamente.")
            print(f"📊 Estadísticas:")
            print(f"   - Tiempo de generación: {duration:.2f} segundos")
            print(f"   - Tamaño del archivo: {content_size / 1024:.2f} KB")
            print(f"   - Ítems aproximados: {response.content.count(b'<item>')}")
            
            if duration > 10:
                print("⚠️  ADVERTENCIA: El feed tarda más de 10 segundos. Meta podría estar cortando la conexión por Timeout.")
        else:
            print(f"❌ ERROR: El servidor devolvió código {response.status_code}")
            # Si es 500, intentamos mostrar algo del error (aunque Client captura excepciones, a veces las oculta en el content)
            if response.status_code == 500:
                print("🔍 Contenido del error (primeros 500 caracteres):")
                print(response.content[:500].decode('utf-8', errors='ignore'))
                
    except Exception as e:
        print(f"❌ EXCEPCIÓN CRÍTICA: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_feed()
