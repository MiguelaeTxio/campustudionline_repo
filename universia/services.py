import logging
import google.generativeai as genai
from google.api_core import exceptions
from django.conf import settings
from django.utils import timezone
from .models import UniversiaSession, UniversiaMessage
from .ai_config import UNIVERSIA_ACADEMIC_PROMPT, UNIVERSIA_NAVIGATION_PROMPT
from orchestrator.models import AutomationSettings, ApiKey

logger = logging.getLogger(__name__)

class UniversiaService:
    @staticmethod
    def get_or_create_session(user):
        """Obtiene la sesión activa del usuario o crea una nueva."""
        session = UniversiaSession.objects.filter(user=user, is_active=True).first()
        if not session:
            session = UniversiaSession.objects.create(user=user)
        return session

    @staticmethod
    def _get_api_key():
        """Obtiene una clave API válida de la rotación del orquestador."""
        try:
            config = AutomationSettings.load()
            if config.active_api_key and config.active_api_key.is_enabled and not config.active_api_key.is_quarantined:
                return config.active_api_key.key
        except Exception:
            pass
        
        fallback_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).first()
        if fallback_key:
            return fallback_key.key
        
        raise Exception("No hay claves de API disponibles.")

    @classmethod
    def process_user_message(cls, user, message_text, context_url=None, context_title='General', attempt=1):
        """Procesa el mensaje discriminando contexto y asegurando sincronía."""
        session = cls.get_or_create_session(user)
        
        # 1. Guardar mensaje de usuario
        UniversiaMessage.objects.create(
            session=session,
            role=UniversiaMessage.ROLE_USER,
            content=message_text,
            context_url=context_url
        )
        session.save() 

        # 2. Configuración Contextual (Hito V29)
        try:
            api_key = cls._get_api_key()
            genai.configure(api_key=api_key)
            
            is_study_room = context_url and "/study-room/" in context_url
            if is_study_room:
                prompt = UNIVERSIA_ACADEMIC_PROMPT.format(content_title=context_title or "el material actual")
            else:
                prompt = UNIVERSIA_NAVIGATION_PROMPT

            model = genai.GenerativeModel('gemini-2.5-flash-lite', system_instruction=prompt)

            # 3. Reconstruir historial sincronizado (Evita dobles respuestas por fallos previos)
            all_messages = session.messages.order_by('timestamp').all()
            chat_history = []
            
            # Solo incluimos pares completos (User + Model) anteriores al mensaje actual
            # El mensaje actual es el último de la QuerySet
            for i in range(0, len(all_messages) - 1):
                msg = all_messages[i]
                
                if msg.role == UniversiaMessage.ROLE_USER:
                    # Verificar si este mensaje de usuario tiene una respuesta inmediata del modelo
                    if i + 1 < len(all_messages) and all_messages[i+1].role == UniversiaMessage.ROLE_MODEL:
                        chat_history.append({'role': 'user', 'parts': [msg.content]})
                        chat_history.append({'role': 'model', 'parts': [all_messages[i+1].content]})
            
            # 4. Generar respuesta
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(message_text)
            response_text = response.text
            
            # 5. Guardar respuesta
            UniversiaMessage.objects.create(
                session=session,
                role=UniversiaMessage.ROLE_MODEL,
                content=response_text
            )
            return response_text

        except exceptions.ResourceExhausted:
            # Lógica de Resiliencia Activa (Hito V29)
            try:
                # Cuarentena de la clave fallida
                api_key_str = cls._get_api_key()
                ApiKey.objects.filter(key=api_key_str).update(is_quarantined=True)
                logger.warning(f"Clave agotada detectada. Reintentando con otra... (Intento {attempt})")
            except Exception:
                pass
            
            # Si nos quedan intentos, probamos con la siguiente clave de forma transparente
            if attempt < 3:
                return cls.process_user_message(user, message_text, context_url, context_title, attempt + 1)
            
            return "UniversIA se encuentra realizando labores de mantenimiento técnico momentáneo. Por favor, inténtalo de nuevo en unos minutos." 

        except Exception as e:
            logger.error(f"Error en UniversIA Service: {e}", exc_info=True)
            return "UniversIA está experimentando una alta carga de trabajo. Por favor, refresca la página o inténtalo en unos instantes."
