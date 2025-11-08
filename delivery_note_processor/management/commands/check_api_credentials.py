# /home/MiguelAeTxio/CampuStudiOnline/delivery_note_processor/management/commands/check_api_credentials.py
import os
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

class Command(BaseCommand):
    help = 'Verifica la configuración y conexión con las APIs de Google (Vision y Gemini).'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("--- Iniciando Verificación de APIs de Google ---"))

        # --- Test 1: Google Cloud Vision API (Autenticación implícita) ---
        self.stdout.write("\n[1/2] Verificando Google Cloud Vision API...")
        vision_credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if not vision_credentials_path:
            self.stderr.write(self.style.ERROR("FALLO: La variable de entorno GOOGLE_APPLICATION_CREDENTIALS no está definida."))
            self.stdout.write(self.style.WARNING("       La API de Vision no funcionará."))
        else:
            if not os.path.exists(vision_credentials_path):
                self.stderr.write(self.style.ERROR(f"FALLO: El archivo de credenciales no se encuentra en la ruta: {vision_credentials_path}"))
            else:
                try:
                    # La única forma real de probar es haciendo una llamada mínima.
                    # El simple hecho de importar el cliente no es suficiente.
                    from google.cloud import vision
                    client = vision.ImageAnnotatorClient()
                    # Esta llamada fallará si las credenciales son inválidas o la API no está habilitada.
                    client.annotate_image({'image': {'content': b''}})
                    self.stdout.write(self.style.SUCCESS("ÉXITO: Las credenciales de Vision API parecen ser válidas y la librería se comunica."))
                except google_exceptions.PermissionDenied as e:
                    self.stderr.write(self.style.ERROR(f"FALLO DE PERMISO: {e}"))
                    self.stderr.write(self.style.WARNING("       Asegúrate de que la API 'Cloud Vision API' esté habilitada en tu proyecto de Google Cloud."))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"FALLO INESPERADO al probar Vision API: {e}"))

        # --- Test 2: Google Gemini API (API Key) ---
        self.stdout.write("\n[2/2] Verificando Google Gemini API...")
        gemini_api_key = os.environ.get('GEMINI_API_KEY')
        if not gemini_api_key:
            self.stderr.write(self.style.ERROR("FALLO: La variable de entorno GEMINI_API_KEY no está definida."))
        else:
            try:
                genai.configure(api_key=gemini_api_key)
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                # Hacemos una llamada mínima para verificar la clave.
                model.generate_content("test", generation_config=genai.types.GenerationConfig(max_output_tokens=1))
                self.stdout.write(self.style.SUCCESS("ÉXITO: La API Key de Gemini es válida y se puede comunicar con el modelo."))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"FALLO al probar Gemini API: {e}"))
                self.stderr.write(self.style.WARNING("       Verifica que la API Key es correcta y que la API 'Generative Language API' está habilitada."))

        self.stdout.write(self.style.SUCCESS("\n--- Verificación Finalizada ---"))
