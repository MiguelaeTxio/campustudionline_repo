import os

print("--- DIAGNÓSTICO DE VARIABLE DE ENTORNO ---")
redis_url = os.environ.get("REDIS_URL")

if redis_url:
    print(f"La URL de Redis detectada es: {redis_url}")
    if redis_url.endswith('/1') or '/1?' in redis_url:
        print("\nERROR CRÍTICO: La URL de REDIS sigue apuntando a la DB /1.")
        print("Solución: Debe eliminar o modificar la variable de entorno REDIS_URL")
        print("en la sección 'Variables de Entorno' de la aplicación web en PythonAnywhere.")
    else:
        print("\nINFO: La URL es correcta (DB 0). El fallo es de caché en el proceso web.")
else:
    print("\nADVERTENCIA: La variable REDIS_URL no está definida en el entorno actual.")
    print("El fallo es de inicialización del proceso web. Debe forzar el reload de Gunicorn.")

