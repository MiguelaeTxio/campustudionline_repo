import logging
import google.generativeai as genai
from django.conf import settings
from django.utils import timezone
from .models import UniversiaSession, UniversiaMessage
from .ai_config import UNIVERSIA_SYSTEM_PROMPT_TEMPLATE
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
        """
        Obtiene una clave API válida.
        Prioriza la clave activa global, luego busca cualquier clave habilitada.
        """
        try:
            config = AutomationSettings.load()
            if config.active_api_key and config.active_api_key.is_enabled and not config.active_api_key.is_quarantined:
                return config.active_api_key.key
        except Exception:
            pass # Si falla la carga de configuración, intentamos fallback directo
        
        # Fallback
        fallback_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).first()
        if fallback_key:
            return fallback_key.key
        
        raise Exception("No hay claves de API disponibles para UniversIA.")

    @classmethod
    def process_user_message(cls, user, message_text, context_url=None, context_title='General'):
        """
        Procesa un mensaje de usuario:
        1. Guarda el mensaje del usuario.
        2. Reconstruye el historial.
        3. Llama a Gemini.
        4. Guarda y devuelve la respuesta.
        """
        session = cls.get_or_create_session(user)
        
        # 1. Guardar mensaje de usuario
        UniversiaMessage.objects.create(
            session=session,
            role=UniversiaMessage.ROLE_USER,
            content=message_text,
            context_url=context_url
        )
        
        # Actualizar timestamp de sesión
        session.save() 

        # 2. Configurar Gemini
        try:
            api_key = cls._get_api_key()
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash-lite', system_instruction=UNIVERSIA_SYSTEM_PROMPT_TEMPLATE)

            # 3. Reconstruir historial
            history_objects = session.messages.order_by('timestamp').all()
            
            chat_history = []
            for msg in history_objects:
                role = 'user' if msg.role == UniversiaMessage.ROLE_USER else 'model'
                
                # Excluir el último mensaje (el actual) para usarlo en send_message
                if msg == history_objects.last() and msg.role == UniversiaMessage.ROLE_USER:
                    continue
                    
                chat_history.append({'role': role, 'parts': [msg.content]})

            # 4. Generar respuesta
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(message_text)
            response_text = response.text
            
            # 5. Guardar respuesta del modelo
            UniversiaMessage.objects.create(
                session=session,
                role=UniversiaMessage.ROLE_MODEL,
                content=response_text
            )
            return response_text

        except Exception as e:
            logger.error(f"Error en UniversIA Service: {e}", exc_info=True)
            error_msg = "Lo siento, he tenido un problema técnico momentáneo. ¿Podrías repetirlo?"
            # Opcional: Guardar el error como mensaje del sistema o dejar que el usuario reintente
            return error_msg
