# /home/MiguelAeTxio/CampuStudiOnline/check_models.py
import os
import google.generativeai as genai
import dotenv

# Cargar las variables de entorno desde el archivo .env
dotenv.load_dotenv()

print("Iniciando script de diagnóstico de modelos de Gemini...")

try:
    # Configurar la API key desde la variable de entorno
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("No se pudo encontrar la variable de entorno GEMINI_API_KEY.")

    genai.configure(api_key=api_key)
    print("API de Gemini configurada con éxito.")

    print("\nModelos disponibles que soportan 'generateContent':")
    print("--------------------------------------------------")

    count = 0
    # Iterar sobre todos los modelos y filtrar los que necesitamos
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(f"- {m.name}")
            count += 1

    if count == 0:
        print("No se encontraron modelos compatibles con 'generateContent'.")
    else:
        print(f"\nTotal de modelos compatibles encontrados: {count}")

except Exception as e:
    print(f"\n[ERROR] Ocurrió un error durante la ejecución: {e}")

print("\nScript de diagnóstico finalizado.")
