# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/core/services/gemini_service.py
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
GEMINI_MODEL_NAME = "gemini-2.5-flash-lite"
PROACTIVE_DELAY_SECONDS = 2

# --- Custom Exceptions ---
class AIServiceCriticalError(Exception):
    """Lanzada para errores no recuperables que deben detener el proceso."""
    pass

# --- Helper Functions (Stateless Design) ---

def _execute_gemini_call(contents, api_key: ApiKey, generation_config: dict, safety_settings: list, system_instruction: str = None) -> types.GenerateContentResponse:
    """
    Configura el cliente unificado (v1) y realiza la llamada.
    Habilitado para multimodalidad (Texto, Audio, Imagen).
    """
    client = genai.Client(api_key=api_key.key)
    
    logger.info(f"Llamada Multimodal con clave '{api_key.name}' usando '{GEMINI_MODEL_NAME}'.")
    time.sleep(PROACTIVE_DELAY_SECONDS)
    
    # Combinar configuración base con la dinámica (ej: response_mime_type)
    # [CORRECCIÓN SDK v1] system_instruction se integra en el config
    config_params = {
        "max_output_tokens": generation_config.get("max_output_tokens", 8192),
        "safety_settings": safety_settings,
        "system_instruction": system_instruction,
    }
    if "response_mime_type" in generation_config:
        config_params["response_mime_type"] = generation_config["response_mime_type"]
    if "speech_config" in generation_config:
        config_params["speech_config"] = generation_config["speech_config"]
    if "response_schema" in generation_config:
        config_params["response_schema"] = generation_config["response_schema"]

    config = types.GenerateContentConfig(**config_params)

    return client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=contents,
        config=config
    )

def clean_json_response(raw_text: str) -> str:
    """
    [PUBLIC] Extrae un bloque de código JSON y blinda secuencias LaTeX (escapes inválidos).
    """
    # 1. Extracción del bloque JSON
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL | re.IGNORECASE)
    if match:
        text = match.group(1)
    else:
        start = raw_text.find('{')
        end = raw_text.rfind('}')
        if start != -1 and end != -1 and end > start:
            text = raw_text[start : end + 1]
        else:
            text = raw_text.strip()
            
    # 2. BLINDAJE LATEX/BACKSLASH (Anti-JSONDecodeError)
    # Buscamos barras invertidas que NO sean escapes JSON válidos y las duplicamos.
    # Secuencias válidas: \" \\ \/ \b \f \n \r \t \u
    # El regex busca una \ seguida de algo que NO está en la lista permitida.
    text = re.sub(r'\\(?![bfnrtu"/\\ ])', r'\\\\', text)
    
    return text

# --- Public Functions ---

def generate_text_content(prompt: str, api_key: ApiKey, task_id: str = None, system_instruction: str = None, response_schema: dict = None) -> Tuple[bool, str, str, dict]:
    usage_metadata = {"input_tokens": 0, "output_tokens": 0}
    """
    [V7-Stateless-SDKv1] Genera texto usando Gemini 3 Flash Preview.
    """
    close_old_connections()
    
    # Configuración base (Sin temperatura forzada para Gemini 3)
    generation_config = {"max_output_tokens": 8192}
    
    if response_schema:
        generation_config["response_mime_type"] = "application/json"
        generation_config["response_schema"] = response_schema
        
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

        response = _execute_gemini_call(prompt, api_key, generation_config, safety_settings, system_instruction=system_instruction)
        if hasattr(response, "usage_metadata"):
            usage_metadata["input_tokens"] = response.usage_metadata.prompt_token_count
            usage_metadata["output_tokens"] = response.usage_metadata.candidates_token_count

        if not response.candidates:
            msg = "Respuesta bloqueada o vacía (SDK v1 - Sin candidatos)."
            return False, msg, api_key.name, usage_metadata

        candidate = response.candidates[0]
        # Finish Reason en SDK v1
        finish_reason = str(candidate.finish_reason)
        
        if "RECITATION" in finish_reason:
             return False, "RECITATION_ERROR: Bloqueo por derechos de autor (Recitación).", api_key.name, usage_metadata

        if not response.text:
             return False, "Error: El modelo no generó texto visible.", api_key.name, usage_metadata

        return True, response.text.strip(), api_key.name, usage_metadata

    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str.upper():
            logger.warning(f"Límite de cuota detectado con la clave '{api_key.name}'. Propagando excepción.")
            raise AIServiceCriticalError(f"QUOTA_EXCEEDED: {error_str}") 
            
        logger.critical(f"Error inesperado en generate_text_content (SDK v1): {e}", exc_info=True)
        raise AIServiceCriticalError(f"Error inesperado en la capa de servicio de IA: {e}") from e

def generate_audio_content(prompt: str, api_key: ApiKey) -> Tuple[bool, bytes, str]:
    """
    [HITO 6] Genera un archivo de audio (MPEG) nativamente usando Gemini 2.5.
    """
    close_old_connections()
    generation_config = {
        "response_mime_type": "audio/mpeg",
    }
    
    # Reutilizamos los safety_settings definidos en generate_text_content (simplificado para el parche)
    safety_settings = [types.SafetySetting(category=c, threshold="BLOCK_NONE") 
                       for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", 
                                 "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]

    try:
        response = _execute_gemini_call(prompt, api_key, generation_config, safety_settings)
        # En generación de audio, el contenido viene en las partes de la respuesta
        if response.data:
            return True, response.data, api_key.name
        
        # Fallback para algunas versiones del SDK que lo devuelven en partes
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.inline_data:
                    return True, part.inline_data.data, api_key.name
                    
        return False, b"", api_key.name
    except Exception as e:
        logger.error(f"Fallo en generación de audio nativo: {e}")
        return False, b"", api_key.name

def generate_multimodal_correction(prompt: str, audio_path: str, api_key: ApiKey) -> Tuple[bool, str, str]:
    """
    [HITO 6] Envía texto y un archivo de audio para evaluación.
    """
    close_old_connections()
    try:
        with open(audio_path, "rb") as f:
            audio_data = f.read()
        
        # Construcción de mensaje multimodal (SDK v1)
        contents = [
            types.Part.from_bytes(data=audio_data, mime_type="audio/webm"), # O el formato que use el navegador
            types.Part.from_text(text=prompt)
        ]
        
        generation_config = {"max_output_tokens": 2048}
        safety_settings = [types.SafetySetting(category=c, threshold="BLOCK_NONE") 
                           for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", 
                                     "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]

        response = _execute_gemini_call(contents, api_key, generation_config, safety_settings)
        return True, response.text.strip(), api_key.name
    except Exception as e:
        logger.error(f"Error en corrección multimodal: {e}")
        return False, str(e), api_key.name

def classify_subject_identity(subject_name: str, branch_name: str, degree_name: str, api_key: ApiKey) -> Tuple[bool, dict, str]:
    """
    [HITO 6] Classifies a subject using AI to resolve semantic ambiguity (Hybrid Protocol).
    ---
    [HITO 6] Clasifica una asignatura usando la IA para resolver ambigüedad semántica (Protocolo Híbrido).
    """
    from .gemini_schemas import ACADEMIC_CLASSIFICATION_SCHEMA
    
    close_old_connections()
    
    prompt = (
        f"Clasifica la siguiente asignatura según la taxonomía de la plataforma:\n"
        f"- Asignatura: {subject_name}\n"
        f"- Rama: {branch_name}\n"
        f"- Grado: {degree_name}\n"
    )
    
    # [BLINDAJE HITO 6] Instrucción dictatorial con reglas de decisión de V06DOC_SUBARCHETYPES
    system_instruction = """Eres un experto en taxonomía académica universitaria. Tu misión es clasificar la asignatura 
en el sub_archetype_id exacto siguiendo estas reglas de decisión:

1. ARCH_LANG (Lenguas):
   - SUB-LIN-MINOR: Si es un idioma de iniciación, nivel básico o explícitamente indica 'Minor'.
   - SUB-LIN-INSTR: Si es formación lingüística general (B1, B2, C1, C2) sin especialización técnica.
   - SUB-LIN-TRA-TECH / SUB-LIN-PROF: Solo si el curso trata sobre la técnica de traducción profesional.
   - SUB-LIN-PHILO: Si el enfoque es gramática histórica, fonética o evolución lingüística.

2. ARCH_SCI (Ciencias Puras):
   - Clasifica aquí Biología (BIO), Química (CHEM), Física (PHYS), Geología (GEOL), Ambientales (ENV) y Datos (DATA).

3. ARCH_HEALTH (Salud):
   - Usa los prefijos SUB-SAN-* para Medicina, Enfermería, Vet, etc.

Para ARCH_LANG, detecta el idioma objetivo y genera 'localized_sections' traducido fielmente. 
Para el resto, devuelve las secciones en Castellano."""

    generation_config = {
        "response_mime_type": "application/json",
        "response_schema": ACADEMIC_CLASSIFICATION_SCHEMA,
    }
    
    safety_settings = [types.SafetySetting(category=c, threshold="BLOCK_NONE") 
                       for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", 
                                 "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]

    try:
        response = _execute_gemini_call(prompt, api_key, generation_config, safety_settings, system_instruction=system_instruction)
        
        if not response.text:
            return False, {}, api_key.name
            
        data = json.loads(clean_json_response(response.text))
        return True, data, api_key.name
    except Exception as e:
        logger.error(f"Error en clasificación por IA: {e}")
        return False, {}, api_key.name
