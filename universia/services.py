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
    def _get_api_key_object():
        """Obtiene el objeto ApiKey activo o el primer fallback disponible."""
        try:
            config = AutomationSettings.load()
            if config.active_api_key and config.active_api_key.is_enabled and not config.active_api_key.is_quarantined:
                return config.active_api_key
        except Exception: pass
        
        fallback = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).order_by('consecutive_failures').first()
        if fallback:
            return fallback
        raise Exception("No hay claves de API disponibles o todas están en cuarentena.")

    @classmethod
    def process_user_message(cls, user, message_text, context_url=None, context_title='General', attempt=1):
        session = cls.get_or_create_session(user)
        
        # Limitar longitud de URL para integridad de DB
        safe_url = (context_url[:490] + '...') if context_url and len(context_url) > 500 else context_url

        # 1. Registro inicial del mensaje de usuario
        UniversiaMessage.objects.create(session=session, role='user', content=message_text, context_url=safe_url)
        session.save() 

        client_action = None
        response_text = "Lo siento, no he podido procesar tu solicitud."

        try:
            # 2. Configuración Gemini
            api_key_obj = cls._get_api_key_object()
            api_key = api_key_obj.key
            genai.configure(api_key=api_key)
            
            # Datos Temporales
            now = timezone.localtime(timezone.now())
            current_time_str = now.strftime("%Y-%m-%d %H:%M:%S (%A)")
            
            # Inyección limpia de Skill
            skill_fmt = UNIVERSIA_AGENDA_SKILL.format(current_time=current_time_str + " (Europe/Madrid Time)")

            if context_url and "/study-room/" in context_url:
                base_prompt = UNIVERSIA_ACADEMIC_PROMPT.format(
                    content_title=context_title or "el material",
                    agenda_skill="{agenda_skill}"
                ).replace("{agenda_skill}", skill_fmt)
            else:
                base_prompt = UNIVERSIA_NAVIGATION_PROMPT.replace("{agenda_skill}", skill_fmt)

            # [Hito 36] Inyección de contexto: Sala de Traducción
            base_prompt += "\n\n[SISTEMA - ACTUALIZACIÓN]\nEstá disponible la nueva 'Sala de Traducción'. Si el usuario pide traducir documentos o textos largos, indícale que puede hacerlo en: /traducciones/. Es una herramienta especializada que soporta PDF y Word."
            
            model = genai.GenerativeModel('gemini-2.5-flash-lite', system_instruction=base_prompt)

            # 3. Reconstrucción ROBUSTA del historial
            # Evita errores de API si la BD tiene mensajes desordenados o impares
            all_messages = session.messages.order_by('timestamp').all()
            chat_history = []
            
            current_pair = []
            for msg in all_messages:
                # IMPORTANTE: Ignorar el mensaje actual que acabamos de guardar arriba
                # para no duplicarlo, ya que send_message lo añade implícitamente.
                if msg.content == message_text and msg.role == 'user' and msg == all_messages[len(all_messages)-1]:
                    continue

                if msg.role == 'user':
                    current_pair = [{'role': 'user', 'parts': [{'text': msg.content}]}]
                elif msg.role == 'model' and current_pair:
                    # Solo añadimos respuesta si hay una pregunta pendiente (cierra el par)
                    current_pair.append({'role': 'model', 'parts': [{'text': msg.content}]})
                    chat_history.extend(current_pair)
                    current_pair = [] # Reset para el siguiente par
            
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
                        # Mapeo de tipos de evento (max_length=2)
                        type_map = {
                            'class': 'CL', 'exam': 'EX', 'practice': 'PR', 
                            'tutorial': 'TU', 'study': 'ST', 'deadline': 'DL', 
                            'task': 'DL', 'reminder': 'PE', 'event': 'PE'
                        }
                        raw_type = str(params.get("event_type", "PE")).lower()
                        event_type_code = type_map.get(raw_type, 'PE')

                        import pytz
                        local_tz = pytz.timezone(settings.TIME_ZONE)
                        
                        def parse_to_local(dt_str):
                            # Intentar parsear y forzar la zona horaria local del proyecto
                            dt = datetime.datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
                            if timezone.is_aware(dt):
                                dt = timezone.make_naive(dt)
                            return local_tz.localize(dt)

                        try:
                            raw_st = params["start_time"]
                            # Si la IA envía solo HH:MM:SS, le concatenamos la fecha de hoy
                            if len(raw_st) <= 8 and ":" in raw_st:
                                raw_st = f"{timezone.localtime(timezone.now()).strftime('%Y-%m-%d')} {raw_st}"
                            st_dt = parse_to_local(raw_st)
                            st = st_dt
                            
                            if params.get("end_time"):
                                et = parse_to_local(params["end_time"])
                            else:
                                delta = timedelta(minutes=10) if event_type_code == 'DL' else timedelta(hours=1)
                                et = st_dt + delta
                        except Exception as e:
                            logger.error(f"Error parseando fechas de UniversIA: {e}")
                            st = timezone.now()
                            et = st + timedelta(hours=1)

                        has_col = AcademicEvent.objects.filter(user=user, start_time__lt=et, end_time__gt=st, is_all_day=False).exists()
                        AcademicEvent.objects.create(
                            user=user, 
                            title=params["title"][:190],
                            description=params.get("description", ""),
                            start_time=st, 
                            end_time=et, 
                            event_type=event_type_code
                        )

                        if has_col:
                            response_text = f"⚠️ He agendado '**{params['title']}**', pero detecto un conflicto de horario en tu agenda. He preparado un enlace abajo para que lo compruebes."
                            client_action = {"type": "redirect", "url": "/schedule/"}
                        else:
                            response_text = f"✅ ¡Hecho! He añadido '**{params['title']}**' a tu agenda correctamente."
            except Exception as e:
                logger.error(f"Skill Execution Error: {e}", exc_info=True)
                # OBLIGATORIO: Si la creación falla, el mensaje de éxito de la IA es MENTIRA.
                # Sobreescribimos para evitar el falso positivo.
                response_text = f"⚠️ He intentado agendar el evento, pero ha ocurrido un error técnico: {str(e)}. ¿Podrías intentar indicarme la fecha y hora de forma más precisa?" 


        except exceptions.ResourceExhausted:
            # Lógica de Rotación y Cuarentena (Hito 24)
            try:
                api_key_obj.consecutive_failures += 1
                config = AutomationSettings.load()
                if api_key_obj.consecutive_failures >= config.max_consecutive_api_errors:
                    api_key_obj.is_quarantined = True
                    logger.warning(f"Clave {api_key_obj.name} puesta en CUARENTENA.")
                api_key_obj.save()
            except Exception as re_err:
                logger.error(f"Error actualizando estado de clave: {re_err}")

            if attempt < 5: # Aumentamos reintentos para dar margen a la rotación
                logger.info(f"Reintentando con nueva clave (Intento {attempt + 1})...")
                return cls.process_user_message(user, message_text, context_url, context_title, attempt + 1)
            
            response_text = "IA saturada (Límite de cuota alcanzado en todas las claves). Reintenta en unos minutos." 

        except Exception as e:
            logger.error(f"FATAL UniversIA Service: {e}", exc_info=True)
            # MEJORA: Visibilidad de errores para administradores en el frontend
            if user.is_staff or user.is_superuser:
                response_text = f"⚠️ **DEBUG ERROR (Admin Only):**\n\n`{str(e)}`"
            else:
                response_text = "Lo siento, ha ocurrido un error interno en el servicio. Por favor, inténtalo de nuevo más tarde."

        # 6. Persistencia de respuesta
        UniversiaMessage.objects.create(session=session, role='model', content=response_text)
        
        return {'text': response_text, 'action': client_action}
