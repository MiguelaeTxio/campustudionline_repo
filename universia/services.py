import logging
import google.generativeai as genai
from google.api_core import exceptions
import json
import re
import datetime
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from .models import UniversiaSession, UniversiaMessage
from .ai_config import UNIVERSIA_ACADEMIC_PROMPT, UNIVERSIA_NAVIGATION_PROMPT, UNIVERSIA_AGENDA_SKILL
from orchestrator.models import AutomationSettings, ApiKey
from schedule.models import AcademicEvent

logger = logging.getLogger(__name__)

class UniversiaService:
    @staticmethod
    def get_or_create_session(user):
        """Obtiene la sesión activa o crea una nueva."""
        session = UniversiaSession.objects.filter(user=user, is_active=True).first()
        if not session:
            session = UniversiaSession.objects.create(user=user)
        return session

    @staticmethod
    def _get_api_key():
        try:
            config = AutomationSettings.load()
            if config.active_api_key and config.active_api_key.is_enabled and not config.active_api_key.is_quarantined:
                return config.active_api_key.key
        except Exception: pass
        fallback = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).first()
        if fallback: return fallback.key
        raise Exception("No hay claves de API disponibles.")

    @classmethod
    def process_user_message(cls, user, message_text, context_url=None, context_title='General', attempt=1):
        session = cls.get_or_create_session(user)
        
        # Limitar longitud de URL para integridad de DB
        safe_url = (context_url[:490] + '...') if context_url and len(context_url) > 500 else context_url

        # 1. Registro inicial
        UniversiaMessage.objects.create(session=session, role='user', content=message_text, context_url=safe_url)
        session.save() 

        client_action = None
        response_text = "Lo siento, no he podido procesar tu solicitud."

        try:
            # 2. Configuración Gemini
            api_key = cls._get_api_key()
            genai.configure(api_key=api_key)
            
            # Datos Temporales
            now = timezone.now()
            current_time_str = now.strftime("%Y-%m-%d %H:%M:%S (%A)")
            
            # Inyección limpia de Skill
            skill_fmt = UNIVERSIA_AGENDA_SKILL.format(current_time=current_time_str)

            if context_url and "/study-room/" in context_url:
                # Usamos replace para evitar colisiones con llaves del JSON de la skill
                base_prompt = UNIVERSIA_ACADEMIC_PROMPT.format(
                    content_title=context_title or "el material",
                    agenda_skill="{agenda_skill}"
                ).replace("{agenda_skill}", skill_fmt)
            else:
                base_prompt = UNIVERSIA_NAVIGATION_PROMPT.replace("{agenda_skill}", skill_fmt)

            model = genai.GenerativeModel('gemini-2.5-flash-lite', system_instruction=base_prompt)

            # 3. Reconstruir historial con formato SDK correcto [{'text': ...}]
            all_messages = session.messages.order_by('timestamp').all()
            chat_history = []
            for i in range(0, len(all_messages) - 1):
                msg = all_messages[i]
                if msg.role == 'user':
                    if i + 1 < len(all_messages) and all_messages[i+1].role == 'model':
                        chat_history.append({'role': 'user', 'parts': [{'text': msg.content}]})
                        chat_history.append({'role': 'model', 'parts': [{'text': all_messages[i+1].content}]})
            
            # 4. Llamada a la IA
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(message_text)
            
            # Validación de respuesta segura
            if response and response.candidates:
                response_text = response.text
            else:
                response_text = "Mi respuesta ha sido filtrada por motivos de seguridad o no se pudo generar."
            
            # 5. Skill Execution (Agenda)
            try:
                json_match = re.search(r"```json\s*(\{.*?\})\s*```", response_text, re.DOTALL) or re.search(r"(\{.*\})", response_text, re.DOTALL)
                if json_match and '"action": "create_event"' in json_match.group(1):
                    raw_json = json_match.group(1)
                    data = json.loads(raw_json)
                    params = data.get("params", {})
                    
                    if params.get("title") and params.get("start_time"):
                        st = params["start_time"]
                        et = params.get("end_time")
                        
                        if not et:
                            try:
                                dt_start = datetime.datetime.fromisoformat(st.replace('Z', '+00:00'))
                                if timezone.is_naive(dt_start): dt_start = timezone.make_aware(dt_start)
                                is_task = params.get("event_type") == 'DL' or "tarea" in str(params.get("description", "")).lower()
                                delta = timedelta(minutes=10) if is_task else timedelta(hours=1)
                                et = (dt_start + delta).strftime("%Y-%m-%d %H:%M:%S")
                            except: et = st

                        # Check colisiones
                        has_col = AcademicEvent.objects.filter(user=user, start_time__lt=et, end_time__gt=st).exists()
                        AcademicEvent.objects.create(user=user, title=params["title"], start_time=st, end_time=et, event_type=params.get("event_type", "PE"))

                        if has_col:
                            response_text = f"⚠️ He agendado '{params['title']}', pero detecto un conflicto con otros eventos. Abriendo tu agenda..."
                            client_action = {"type": "redirect", "url": "/schedule/"}
                        else:
                            response_text = f"✅ Evento '{params['title']}' añadido correctamente."
            except Exception as e:
                logger.warning(f"Skill Error: {e}")

        except exceptions.ResourceExhausted:
            if attempt < 3: return cls.process_user_message(user, message_text, context_url, context_title, attempt + 1)
            response_text = "IA saturada. Reintenta en un momento." 

        except Exception as e:
            logger.error(f"FATAL UniversIA Service: {e}", exc_info=True)
            response_text = "Error del servicio."

        # 6. Persistencia de respuesta
        UniversiaMessage.objects.create(session=session, role='model', content=response_text)
        
        return {'text': response_text, 'action': client_action}
