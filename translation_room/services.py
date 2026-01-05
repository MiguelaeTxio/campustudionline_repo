# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/translation_room/services.py
import logging
import pypdf
import docx
import google.generativeai as genai
from django.conf import settings
from orchestrator.models import AutomationSettings, ApiKey

logger = logging.getLogger(__name__)

class DocumentExtractionError(Exception):
    pass

class TranslationService:
    """
    Servicio refactorizado para Streaming y Multi-idioma.
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
    def stream_translation(cls, text: str, target_lang: str, source_lang: str = "Auto") -> any:
        """
        Generador que emite chunks de texto traducido en tiempo real.
        """
        api_key = cls._get_api_key_string()
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        # Prompt optimizado para traducción directa
        prompt = (
            f"Actúa como un traductor experto y simultáneo. "
            f"Origen: {source_lang}. Destino: {target_lang}. "
            f"Instrucción: Traduce el siguiente texto manteniendo el formato, tono y terminología. "
            f"NO expliques nada, solo traduce.\n\n"
            f"Texto:\n{text}"
        )

        try:
            # Activamos stream=True para recibir paquetes parciales
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"\n[Error de conexión con IA: {str(e)}]"
