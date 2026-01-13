# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/translation_room/services.py
import logging
import pypdf
import docx
from google import genai
from google.genai import types
from django.conf import settings
from orchestrator.models import AutomationSettings, ApiKey
from .models import TranslationLog

logger = logging.getLogger(__name__)

# Constante de Modelo vinculante
GEMINI_MODEL_NAME = "gemini-3-flash-preview"

class DocumentExtractionError(Exception):
    pass

class TranslationService:
    """
    Servicio refactorizado para Streaming y Multi-idioma (SDK v1).
    """

    @staticmethod
    def _get_api_key_string() -> str:
        """Obtiene la string de la clave API directamente."""
        try:
            config = AutomationSettings.load()
            if config.active_api_key and config.active_api_key.is_enabled and not config.active_api_key.is_quarantined:
                return config.active_api_key.key
        except Exception:
            pass
        
        fallback = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).first()
        if not fallback:
            raise Exception("No hay claves de API disponibles.")
        return fallback.key

    @classmethod
    def extract_text_from_file(cls, file_obj, file_extension: str) -> str:
        """Extrae texto plano de archivos."""
        try:
            text = ""
            file_extension = file_extension.lower()

            if file_extension == '.pdf':
                reader = pypdf.PdfReader(file_obj)
                for page in reader.pages:
                    extract = page.extract_text()
                    if extract: text += extract + "\n"
            
            elif file_extension in ['.docx', '.doc']:
                doc = docx.Document(file_obj)
                text = "\n".join([p.text for p in doc.paragraphs])
            
            elif file_extension == '.txt':
                text = file_obj.read().decode('utf-8')
            
            else:
                raise DocumentExtractionError(f"Formato no soportado: {file_extension}")

            return text.strip()
        except Exception as e:
            logger.error(f"Extraction error: {e}")
            raise DocumentExtractionError("Error leyendo el archivo.")

    @classmethod
    def stream_translation(cls, text: str, target_lang: str, user, source_lang: str = "Auto") -> any:
        """
        Generador que emite chunks de texto traducido en tiempo real (SDK v1).
        Registra la actividad en TranslationLog.
        """
        # Crear log inicial
        log_entry = TranslationLog.objects.create(
            user=user if user.is_authenticated else None,
            source_lang=source_lang,
            target_lang=target_lang,
            char_count=len(text)
        )
        
        try:
            api_key = cls._get_api_key_string()
            client = genai.Client(api_key=api_key)
            
            prompt = (
                f"Actúa como un traductor experto y simultáneo. "
                f"Origen: {source_lang}. Destino: {target_lang}. "
                f"Instrucción: Traduce el siguiente texto manteniendo el formato, tono y terminología académica. "
                f"NO expliques nada, solo traduce.\n\n"
                f"Texto:\n{text}"
            )
            
            config = types.GenerateContentConfig(
                temperature=0.3, 
                thinking_config=types.ThinkingConfig(include_thoughts=False)
            )

            response_stream = client.models.generate_content(
                model=GEMINI_MODEL_NAME,
                contents=prompt,
                config=config,
                stream=True
            )
            
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            # Captura de error en el log
            logger.error(f"Streaming error: {e}")
            log_entry.is_successful = False
            log_entry.error_message = str(e)
            log_entry.save()
            yield f"\n[Error de conexión con IA: {str(e)}]"
