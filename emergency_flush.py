import os
import redis
import sys

def flush_redis():
    # Obtener la URL de Redis del entorno, con fallback a local para seguridad
    redis_url = os.environ.get("REDIS_URL")
    
    if not redis_url:
        print("ERROR: No se encontró la variable de entorno REDIS_URL.")
        sys.exit(1)

    # Ocultar credenciales para el log visual
    safe_url = redis_url.split('@')[-1] if '@' in redis_url else 'localhost'
    print(f"--- PROTOCOLO DE PURGADO DE REDIS ---")
    print(f"Objetivo: {safe_url}")
    
    try:
        # Conexión directa
        r = redis.from_url(redis_url)
        r.ping() # Verificar conexión
        
        # Diagnóstico previo
        keys_count = r.dbsize()
        print(f"Estado Actual: {keys_count} claves (tareas/resultados) en memoria.")
        
        if keys_count == 0:
            print("Diagnóstico: La cola ya está vacía. No se requiere acción.")
            return

        # Ejecución del purgado
        print("Ejecutando FLUSHDB (Borrado total de tareas)...")
        r.flushdb()
        
        # Verificación
        new_count = r.dbsize()
        if new_count == 0:
            print("RESULTADO: ÉXITO. La cola está completamente vacía.")
            print("El sistema de mensajería debería fluir instantáneamente ahora.")
        else:
            print(f"ALERTA: Quedan {new_count} claves. Algo ha fallado.")

    except redis.exceptions.AuthenticationError:
        print("ERROR: Fallo de autenticación con Redis.")
    except Exception as e:
        print(f"ERROR CRÍTICO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    flush_redis()
