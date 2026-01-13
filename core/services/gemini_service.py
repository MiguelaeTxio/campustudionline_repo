import json
import logging
import re
import time
from typing import Tuple

from google import genai
from google.genai import types
from django.db import close_old_connections

# [REFACTORIZADO HITO 37] SDK Unificado Google Gen AI (v1)
# Soporte oficial para Gemini 3 Flash Preview.
from orchestrator.models import ApiKey, PendingContentTask

logger = logging.getLogger(__name__)

# --- Configuration Constants ---
# ID Oficial Preview para API
GEMINI_MODEL_NAME = "gemini-3-flash-preview"
PROACTIVE_DELAY_SECONDS = 2

# --- Custom Exceptions ---
class AIServiceCriticalError(Exception):
    """Lanzada para errores no recuperables que deben detener el proceso."""
    pass

# --- Helper Functions (Stateless Design) ---

def _execute_gemini_call(prompt: str, api_key: ApiKey, generation_config: dict, safety_settings: list) -> types.GenerateContentResponse:
    """
    Configura el cliente unificado (v1) y realiza la llamada.
    """
    client = genai.Client(api_key=api_key.key)
    
    logger.info(f"Realizando llamada a la API (SDK v1) con la clave '{api_key.name}' usando '{GEMINI_MODEL_NAME}'.")
    time.sleep(PROACTIVE_DELAY_SECONDS)
    
    # Configuración de generación tipada (SDK v1)
    # [GEMINI 3 SPECIFIC]: Temperatura default (1.0) requerida para razonamiento óptimo.
    config = types.GenerateContentConfig(
        max_output_tokens=generation_config.get("max_output_tokens", 8192),
        safety_settings=safety_settings,
        thinking_config=types.ThinkingConfig(include_thoughts=True)
    )

    return client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=prompt,
        config=config
    )

def clean_json_response(raw_text: str) -> str:
    """
    [PUBLIC] Extrae un bloque de código JSON de una cadena de texto.
    """
    # Usa el modulo 're' importado globalmente
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    
    start = raw_text.find('{')
    end = raw_text.rfind('}')
    
    if start != -1 and end != -1 and end > start:
        return raw_text[start : end + 1]
        
    return raw_text.strip()

# --- Public Functions ---

def generate_text_content(prompt: str, api_key: ApiKey, task_id: str = None) -> Tuple[bool, str, str]:
    """
    [V7-Stateless-SDKv1] Genera texto usando Gemini 3 Flash Preview.
    """
    close_old_connections()
    
    # Configuración base (Sin temperatura forzada para Gemini 3)
    generation_config = {"max_output_tokens": 8192}
    
    # Safety Settings (SDK v1 Format)
    safety_settings = [
        types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="BLOCK_NONE"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH",
            threshold="BLOCK_NONE"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold="BLOCK_NONE"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold="BLOCK_NONE"
        ),
    ]

    try:
        if task_id:
            try:
                PendingContentTask.objects.filter(pk=task_id).update(api_key_used=api_key.name)
                logger.info(f"Registro atómico: Tarea {task_id} actualizada para usar la clave '{api_key.name}'.")
            except Exception as e:
                logger.error(f"Error CRÍTICO en el registro atómico para la tarea {task_id}: {e}", exc_info=True)

        response = _execute_gemini_call(prompt, api_key, generation_config, safety_settings)

        if not response.candidates:
            msg = "Respuesta bloqueada o vacía (SDK v1 - Sin candidatos)."
            return False, msg, api_key.name

        candidate = response.candidates[0]
        # Finish Reason en SDK v1
        finish_reason = str(candidate.finish_reason)
        
        if "RECITATION" in finish_reason:
             return False, "RECITATION_ERROR: Bloqueo por derechos de autor (Recitación).", api_key.name

        if not response.text:
             return False, "Error: El modelo no generó texto visible.", api_key.name

        return True, response.text.strip(), api_key.name

    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str.upper():
            logger.warning(f"Límite de cuota detectado con la clave '{api_key.name}'. Propagando excepción.")
            raise AIServiceCriticalError(f"QUOTA_EXCEEDED: {error_str}") 
            
        logger.critical(f"Error inesperado en generate_text_content (SDK v1): {e}", exc_info=True)
        raise AIServiceCriticalError(f"Error inesperado en la capa de servicio de IA: {e}") from e
