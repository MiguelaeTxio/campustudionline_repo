# /home/MiguelAeTxio/CampuStudiOnline/core/services/gemini_service.py
import json
import logging
import re
import time
from typing import Tuple

import google.generativeai as genai
from google.api_core import exceptions
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from django.db import close_old_connections

# [REFACTORIZADO V6] El servicio ya no gestiona estado, solo ejecuta.
# Las importaciones de modelos de Django y la lógica de BBDD se eliminan.
from content_automation.models import PendingContentTask
from content_automation.models import ApiKey

logger = logging.getLogger(__name__)

# --- Configuration Constants ---
GEMINI_MODEL_NAME = "gemini-2.5-flash-lite"
PROACTIVE_DELAY_SECONDS = 2

# --- Custom Exceptions ---
class AIServiceCriticalError(Exception):
    """Lanzada para errores no recuperables que deben detener el proceso."""
    pass

# --- Helper Functions (Stateless Design) ---

def _execute_gemini_call(prompt: str, api_key: ApiKey, generation_config: dict, safety_settings: dict) -> genai.GenerativeModel.generate_content:
    """Configura el cliente ad-hoc y realiza la llamada."""
    genai.configure(api_key=api_key.key)
    
    model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    
    logger.info(f"Realizando llamada a la API con la clave '{api_key.name}'.")
    time.sleep(PROACTIVE_DELAY_SECONDS)
    
    return model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(**generation_config),
        safety_settings=safety_settings,
        request_options={"timeout": 600}
    )

def clean_json_response(raw_text: str) -> str:
    """
    [PUBLIC] Extrae un bloque de código JSON de una cadena de texto.
    """
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
    if match:
        return match.group(1)
    return raw_text.strip()

# --- Public Functions (Refactored with Internal Resilience) ---

def generate_text_content(prompt: str, api_key: ApiKey, task_id: str = None) -> Tuple[bool, str, str]:
    """
    [V6-Stateless] Genera texto usando la clave de API proporcionada.
    No contiene lógica de reintentos ni de rotación; propaga las excepciones de cuota
    hacia la capa superior (la tarea) para que esta decida cómo actuar.
    """
    close_old_connections()
    generation_config = {"temperature": 0.4, "max_output_tokens": 8192}
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    try:
        # [DIRECTRIZ ATÓMICA] Si se proporciona un ID de tarea, se escribe la clave
        # que se va a usar ANTES de la llamada a la API.
        if task_id:
            try:
                PendingContentTask.objects.filter(pk=task_id).update(api_key_used=api_key.name)
                logger.info(f"Registro atómico: Tarea {task_id} actualizada para usar la clave '{api_key.name}'.")
            except Exception as e:
                logger.error(f"Error CRÍTICO en el registro atómico para la tarea {task_id}: {e}", exc_info=True)

        response = _execute_gemini_call(prompt, api_key, generation_config, safety_settings)

        if not response.candidates:
            feedback = response.prompt_feedback
            reason = feedback.block_reason.name if feedback and hasattr(feedback, "block_reason") else "UNKNOWN"
            error_msg = f"Respuesta bloqueada por seguridad. Razón: {reason}."
            return False, error_msg, api_key.name

        return True, response.text.strip(), api_key.name

    except exceptions.ResourceExhausted as e:
        # [REFACTORIZADO V6] Propagar la excepción para que la tarea la maneje.
        logger.warning(f"Límite de cuota detectado con la clave '{api_key.name}'. Propagando excepción.")
        raise e

    except Exception as e:
        logger.critical(f"Error inesperado en generate_text_content: {e}", exc_info=True)
        raise AIServiceCriticalError(f"Error inesperado en la capa de servicio de IA: {e}") from e
