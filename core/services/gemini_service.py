# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/core/services/gemini_service.py
import json
import logging
import re
import time
from typing import Tuple

from google import genai
from google.genai import types
from google.genai.errors import APIError
from django.db import close_old_connections

# [REFACTORIZADO HITO 37] SDK Unificado Google Gen AI (v1)
# Soporte oficial para Gemini 3.1 Pro Preview.
from orchestrator.models import ApiKey, PendingContentTask

logger = logging.getLogger(__name__)

# --- Configuration Constants ---
# Modelo activo certificado — Directriz Técnica Vinculante CampuStudiOnline
GEMINI_MODEL_NAME = "gemini-2.5-flash"
# Delay entre llamadas: 0 por defecto (sin delay proactivo forzado).
# El control de cuota lo gestiona _safe_generate_content mediante rotación de claves.
PROACTIVE_DELAY_SECONDS = 0

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
    if "response_modalities" in generation_config:
        config_params["response_modalities"] = generation_config["response_modalities"]

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
    """
    [V7-Stateless-SDKv1] Generates text content using the active Gemini model.
    Supports Structured Outputs via response_schema (Pydantic or JSON Schema).
    Returns a tuple: (success, text_or_error, api_key_name, usage_metadata).
    ---
    Genera contenido de texto usando el modelo Gemini activo.
    Soporta Structured Outputs mediante response_schema (Pydantic o JSON Schema).
    Devuelve una tupla: (exito, texto_o_error, nombre_clave, metadatos_uso).
    """
    usage_metadata = {"input_tokens": 0, "output_tokens": 0}
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

    except APIError as e:
        error_str = str(e).upper()
        if e.code == 429 or "429" in error_str or "QUOTA" in error_str or "RESOURCE" in error_str:
            logger.warning(f"Límite de cuota (429) detectado con la clave '{api_key.name}'. Propagando excepción.")
            raise AIServiceCriticalError(f"QUOTA_EXCEEDED: {e}")
        elif e.code == 503 or "503" in error_str or "OVERLOAD" in error_str:
            raise AIServiceCriticalError(f"SERVER_OVERLOAD: {e}")
        else:
            raise AIServiceCriticalError(f"API_ERROR_{e.code}: {e}")
    except Exception as e:
        error_str = str(e).upper()
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "QUOTA" in error_str:
            logger.warning(f"Límite de cuota detectado con la clave '{api_key.name}'. Propagando excepción.")
            raise AIServiceCriticalError(f"QUOTA_EXCEEDED: {e}") 
            
        logger.critical(f"Error inesperado en generate_text_content (SDK v1): {e}", exc_info=True)
        raise AIServiceCriticalError(f"Error inesperado en la capa de servicio de IA: {e}") from e

def generate_audio_content(prompt: str, api_key: ApiKey) -> Tuple[bool, bytes, str]:
    """
    [HITO 6] Genera un archivo de audio (MPEG) nativamente usando Gemini 3.1 Pro Preview.
    """
    close_old_connections()
    generation_config = {
        "response_modalities": ["AUDIO"],
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

def generate_multimodal_item_content(image_bytes: bytes, image_mime_type: str, prompt: str, api_key: ApiKey, system_instruction: str = None, response_schema: dict = None, task_id: str = None) -> Tuple[bool, str, str, dict]:
    """
    [HITO 38] Generate item content (stem/keywords) from a real, already
    verified image, instead of asking the model to invent a URL.
    ---
    [HITO 38] Genera contenido de ítem (stem/keywords) a partir de una
    imagen real ya verificada, en lugar de pedirle al modelo que invente
    una URL. Inversión del flujo de generación (H38 punto 3): la imagen
    se recupera y verifica primero, y el enunciado se redacta después,
    sobre esa imagen concreta — así se evita el defecto raiz de H38, una
    radiografia patologica ilustrando una pregunta sobre anatomia normal.

    Misma forma de retorno que generate_text_content: (exito,
    texto_o_error, nombre_clave, metadatos_uso). No lanza excepcion por
    fallos de red o de cuota: los devuelve como fallo controlado, porque
    este servicio se llama en un paso de posprocesado que no debe tumbar
    la generacion del resto del examen.
    """
    usage_metadata = {"input_tokens": 0, "output_tokens": 0}
    close_old_connections()

    generation_config = {"max_output_tokens": 4096}
    if response_schema:
        generation_config["response_mime_type"] = "application/json"
        generation_config["response_schema"] = response_schema

    safety_settings = [
        types.SafetySetting(category=c, threshold="BLOCK_NONE")
        for c in [
            "HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT",
        ]
    ]

    contents = [
        types.Part.from_bytes(data=image_bytes, mime_type=image_mime_type),
        types.Part.from_text(text=prompt),
    ]

    try:
        if task_id:
            try:
                PendingContentTask.objects.filter(pk=task_id).update(api_key_used=api_key.name)
            except Exception as e:
                logger.error(f"Error en registro atómico (multimodal item) para tarea {task_id}: {e}", exc_info=True)

        response = _execute_gemini_call(contents, api_key, generation_config, safety_settings, system_instruction=system_instruction)
        if hasattr(response, "usage_metadata"):
            usage_metadata["input_tokens"] = response.usage_metadata.prompt_token_count
            usage_metadata["output_tokens"] = response.usage_metadata.candidates_token_count

        if not response.candidates:
            return False, "Respuesta bloqueada o vacía (multimodal item).", api_key.name, usage_metadata

        candidate = response.candidates[0]
        finish_reason = str(candidate.finish_reason)
        if "RECITATION" in finish_reason:
            return False, "RECITATION_ERROR: Bloqueo por derechos de autor (Recitación).", api_key.name, usage_metadata
        if not response.text:
            return False, "Error: El modelo no generó texto visible (multimodal item).", api_key.name, usage_metadata

        return True, response.text.strip(), api_key.name, usage_metadata

    except APIError as e:
        error_str = str(e).upper()
        if e.code == 429 or "429" in error_str or "QUOTA" in error_str or "RESOURCE" in error_str:
            raise AIServiceCriticalError(f"QUOTA_EXCEEDED: {e}")
        elif e.code == 503 or "503" in error_str or "OVERLOAD" in error_str:
            raise AIServiceCriticalError(f"SERVER_OVERLOAD: {e}")
        else:
            raise AIServiceCriticalError(f"API_ERROR_{e.code}: {e}")
    except Exception as e:
        error_str = str(e).upper()
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "QUOTA" in error_str:
            raise AIServiceCriticalError(f"QUOTA_EXCEEDED: {e}")
        logger.critical(f"Error inesperado en generate_multimodal_item_content: {e}", exc_info=True)
        raise AIServiceCriticalError(f"Error inesperado en generación multimodal de ítem: {e}") from e


def classify_subject_identity(subject_name: str, branch_name: str, degree_name: str, api_key: ApiKey) -> Tuple[bool, dict, str]:
    """
    [HITO 6] Classifies a subject using AI to resolve semantic ambiguity (Hybrid Protocol).
    ---
    [HITO 6] Clasifica una asignatura usando la IA para resolver ambigüedad semántica (Protocolo Híbrido).
    """
    from .gemini_schemas import AcademicClassificationSchema
    
    close_old_connections()
    
    prompt = (
        f"Clasifica la siguiente asignatura según la taxonomía de la plataforma:\n"
        f"- Asignatura: {subject_name}\n"
        f"- Rama: {branch_name}\n"
        f"- Grado: {degree_name}\n"
    )
    
    # [HITO 6 v5.9] Instrucción dictatorial con árbol de decisión completo — 87 IDs certificados
    # Ref: V06DOC_SUBARCHETYPES v5.9, V06DOC_LOGIC_MAPPING
    system_instruction = (
        "Eres un experto en taxonomía académica universitaria española. "
        "Tu única misión es clasificar la asignatura recibida en el sub_archetype_id exacto "
        "de entre los 87 IDs certificados de V06DOC_SUBARCHETYPES v5.9.\n\n"
        "ÁRBOL DE DECISIÓN OBLIGATORIO:\n\n"
        "1. ARCH_LANG (Lenguas Extranjeras):\n"
        "   - SUB-LIN-INSTR: Formación lingüística instrumental (B1/B2/C1/C2, CertAcles, CLM-UGR). "
        "Sin especialización técnica ni literaria.\n"
        "   - SUB-LIN-MINOR: Idioma de iniciación, nivel elemental, asignatura 'Minor' o complemento transversal.\n"
        "   - SUB-LIN-PHILO: Lingüística histórica, gramática diacrónica, fonética histórica, evolución de la lengua.\n"
        "   - SUB-LIN-ECDO: Edición crítica, crítica textual, ecdótica, corrección editorial, edición científica.\n"
        "   - SUB-LIN-NORM: Normativa del español, ortografía académica, El español actual, usos normativos.\n"
        "   - SUB-LIN-TRA-TECH: Traducción especializada técnico-científica, traducción jurídica o económica B-A.\n"
        "   - SUB-LIN-TRA-LIT: Traducción literaria, literatura y traducción, traducción creativa.\n\n"
        "2. ARCH_HUM (Artes y Humanidades):\n"
        "   - SUB-HUM-HIST: Historia (Medieval, Moderna, Contemporánea, Universal, de España).\n"
        "   - SUB-HUM-PHIL: Filosofía, Ética, Metafísica, Lógica, Historia de la Filosofía.\n"
        "   - SUB-HUM-ART-HIST: Historia del Arte, Iconografía, Patrimonio, Museología.\n"
        "   - SUB-HUM-ART-CREA: Bellas Artes, Diseño, Escultura, Pintura, Grabado.\n"
        "   - SUB-HUM-MUS: Musicología, Historia de la Música, Armonía, Análisis Musical.\n"
        "   - SUB-HUM-ANTH: Antropología Social y Cultural, Etnografía, Etnología.\n\n"
        "3. ARCH_HEALTH (Ciencias de la Salud):\n"
        "   - SUB-SAN-MED-CLIN: Medicina clínica, semiología, diagnóstico diferencial, patología.\n"
        "   - SUB-SAN-MED-BASIC: Anatomía, Histología, Embriología (ciencias básicas médicas).\n"
        "   - SUB-SAN-MED-FISIO-GEN: Fisiología general, SNA, homeostasis, cardiovascular, respiratoria.\n"
        "   - SUB-SAN-MED-FISIO-NEURO: Fisiología neurológica, neurofisiología, neurociencia.\n"
        "   - SUB-SAN-CUID: Enfermería, cuidados NANDA/NIC/NOC, técnicas enfermeras.\n"
        "   - SUB-SAN-ODON: Odontología, estomatología, prótesis dental, endodoncia.\n"
        "   - SUB-SAN-FISIO: Fisioterapia, rehabilitación, terapia manual, anatomía palpatoria.\n"
        "   - SUB-SAN-BIOQUIM: Bioquímica, metabolismo, enzimología (Farmacia UGR).\n"
        "   - SUB-SAN-FARM: Farmacología I y II, farmacoterapia, farmacocinética.\n"
        "   - SUB-SAN-PSY-DIAG: Psicopatología, diagnóstico DSM-5/CIE-11, psicología clínica.\n"
        "   - SUB-SAN-PSY-EVAL: Evaluación psicológica, tests psicométricos, psicodiagnóstico.\n"
        "   - SUB-SAN-PSY-MET: Métodos y diseños de investigación (Psicología).\n"
        "   - SUB-SAN-PSY-STAT: Estadística aplicada a la Psicología, análisis de datos.\n"
        "   - SUB-SAN-VET-CLIN: Veterinaria clínica, medicina de animales, diagnóstico veterinario.\n"
        "   - SUB-SAN-VET-CIR: Cirugía veterinaria, anestesia veterinaria.\n"
        "   - SUB-SAN-NUT-DIET: Dietética, nutrición clínica, diseño de dietas.\n"
        "   - SUB-SAN-NUT-BROM: Bromatología, composición de alimentos, calidad alimentaria.\n"
        "   - SUB-SAN-NUT-SPUB: Salud pública alimentaria, epidemiología nutricional, comedores.\n\n"
        "4. ARCH_SOC (Ciencias Sociales y Jurídicas):\n"
        "   - SUB-SOC-LAW-PROC-CIV: Derecho procesal civil, proceso declarativo, ejecución.\n"
        "   - SUB-SOC-LAW-PROC-PEN: Derecho procesal penal, instrucción, juicio oral.\n"
        "   - SUB-SOC-LAW-DICT-CIV: Derecho civil (personas, familia, obligaciones, contratos, reales).\n"
        "   - SUB-SOC-LAW-DICT-PEN: Derecho penal (parte general, parte especial, tipos, penas).\n"
        "   - SUB-SOC-ECON-QUAN-STAT: Estadística, métodos cuantitativos, análisis de datos económicos.\n"
        "   - SUB-SOC-ECON-QUAN-ECON: Econometría, regresión, series temporales.\n"
        "   - SUB-SOC-ECON-MGMT-ACC: Contabilidad financiera, contabilidad de gestión, auditoría.\n"
        "   - SUB-SOC-ECON-MGMT-STR: Dirección estratégica, organización de empresas, management.\n"
        "   - SUB-SOC-ECON-MGMT-ECO: Microeconomía, macroeconomía, teoría económica.\n"
        "   - SUB-SOC-EDU-KIDS: Magisterio Infantil/Primaria, DUA, LOMLOE, didáctica de aula.\n"
        "   - SUB-SOC-EDU-SEC: Máster de Profesorado Secundaria (MAES), didáctica específica.\n"
        "   - SUB-SOC-COMM-JOUR: Periodismo, redacción periodística, géneros informativos.\n"
        "   - SUB-SOC-COMM-AV: Comunicación audiovisual, guion, producción, realización.\n"
        "   - SUB-SOC-GEOG-SIG: Sistemas de Información Geográfica, cartografía digital.\n"
        "   - SUB-SOC-GEOG-TER: Geografía humana, demografía, ordenación del territorio.\n"
        "   - SUB-SOC-GEOG-FIS: Geografía física, climatología, geomorfología.\n"
        "   - SUB-SOC-WORK-INT: Trabajo social, intervención individual y familiar.\n"
        "   - SUB-SOC-WORK-POL: Política social, estado de bienestar, servicios sociales.\n"
        "   - SUB-SOC-WORK-MED: Mediación social, ámbitos especializados (violencia, menores).\n\n"
        "5. ARCH_TECH (Ingeniería y Arquitectura):\n"
        "   - SUB-TEC-SOFT-ALG: Algoritmia, estructuras de datos, complejidad computacional.\n"
        "   - SUB-TEC-SOFT-DS: Diseño de software, patrones, arquitectura de sistemas.\n"
        "   - SUB-TEC-SOFT-SE: Ingeniería del software, requisitos, calidad, pruebas.\n"
        "   - SUB-TEC-CIVIL-STRUCT: Estructuras, resistencia de materiales, cálculo estructural.\n"
        "   - SUB-TEC-CIVIL-CONC: Hormigón armado, pretensado, EHE.\n"
        "   - SUB-TEC-CIVIL-STEEL: Estructuras metálicas, acero, perfiles.\n"
        "   - SUB-TEC-INDUS-THERMO: Termodinámica, motores térmicos, ciclos de potencia.\n"
        "   - SUB-TEC-INDUS-TMM: Teoría de máquinas y mecanismos, cinemática, dinámica.\n"
        "   - SUB-TEC-INDUS-DEM: Diseño y fabricación, metrología, expresión gráfica industrial.\n"
        "   - SUB-TEC-CHEM-BAL: Balances de materia y energía, operaciones unitarias.\n"
        "   - SUB-TEC-CHEM-REACT: Reactores químicos, cinética, ingeniería de procesos.\n"
        "   - SUB-TEC-PROJ-ARCH: Proyectos arquitectónicos, composición, programa funcional.\n"
        "   - SUB-TEC-PROJ-URB: Urbanismo, planeamiento, ordenación del territorio.\n"
        "   - SUB-TEC-CONS-TECH: Construcción, sistemas constructivos, detalle técnico.\n"
        "   - SUB-TEC-CONS-MAN: Gestión de obra, planificación, seguridad y salud laboral.\n"
        "   - SUB-TEC-PURE-ANAL: Análisis matemático, cálculo, ecuaciones diferenciales.\n"
        "   - SUB-TEC-PURE-ALGSTR: Álgebra estructural, topología, geometría diferencial.\n\n"
        "6. ARCH_SCI (Ciencias Puras y Experimentales):\n"
        "   - SUB-SCI-BIO-GEN: Biología molecular, genética, microbiología.\n"
        "   - SUB-SCI-BIO-ZOO: Zoología, botánica, sistemática.\n"
        "   - SUB-SCI-BIO-ECO: Ecología, medio ambiente, conservación.\n"
        "   - SUB-SCI-CHEM-ORG: Química orgánica pura, síntesis, reactividad.\n"
        "   - SUB-SCI-CHEM-INORG: Química inorgánica pura, coordinación, estado sólido.\n"
        "   - SUB-SCI-PHYS-EM: Electromagnetismo, óptica, física ondulatoria.\n"
        "   - SUB-SCI-PHYS-QM: Mecánica cuántica, física moderna, física nuclear.\n"
        "   - SUB-SCI-GEOL-MIN: Mineralogía, petrología, geoquímica.\n"
        "   - SUB-SCI-GEOL-STRAT: Estratigrafía, paleontología, geología histórica.\n"
        "   - SUB-SCI-GEOL-MAP: Cartografía geológica, tectónica, geología estructural.\n"
        "   - SUB-SCI-ENV-RES: Gestión de residuos, evaluación de impacto ambiental.\n"
        "   - SUB-SCI-ENV-CONT: Contaminación, toxicología ambiental, control de emisiones.\n"
        "   - SUB-SCI-DATA-STAT: Estadística computacional, inferencia, modelos probabilísticos.\n"
        "   - SUB-SCI-DATA-ML: Machine learning, aprendizaje automático, IA.\n"
        "   - SUB-SCI-DATA-BIG: Big data, ingeniería de datos, procesamiento distribuido.\n\n"
        "REGLAS ADICIONALES OBLIGATORIAS:\n"
        "- Para ARCH_LANG: detecta el idioma objetivo de la asignatura (ej: inglés → 'en', "
        "francés → 'fr', alemán → 'de', árabe → 'ar', japonés → 'ja', checo → 'cs') "
        "y genera localized_sections con títulos e instrucciones en ese idioma.\n"
        "- Para todos los demás arquetipos: target_language_code = 'es', localized_sections = {}.\n"
        "- PROHIBIDO devolver IDs pre-segregación obsoletos: SUB-LIN-CERT, SUB-LIN-PROF, "
        "SUB-LIN-LIT, SUB-SAN-LAB, SUB-SAN-PSY-CLIN, SUB-SAN-PSY-EXP, SUB-SAN-VET, "
        "SUB-SAN-NUT, SUB-SOC-LAW-PROC, SUB-SOC-LAW-DICT, SUB-SOC-ECON-QUAN, "
        "SUB-SOC-ECON-MGMT, SUB-SOC-WORK, SUB-SOC-GEOG, "
        "SUB-TEC-SOFT, SUB-TEC-CIVIL, SUB-TEC-INDUS, SUB-TEC-CHEM, SUB-TEC-PROJ, "
        "SUB-TEC-CONS, SUB-TEC-PURE, SUB-SCI-BIO, SUB-SCI-CHEM, SUB-SCI-PHYS, "
        "SUB-SCI-GEOL, SUB-SCI-ENV, SUB-SCI-DATA."
    )

    generation_config = {
        "response_mime_type": "application/json",
        "response_schema": AcademicClassificationSchema,
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
