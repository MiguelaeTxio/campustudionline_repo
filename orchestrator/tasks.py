# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/tasks.py
import logging
import traceback
import os
import json
import dirtyjson
import time
import re
import wave
import io
from datetime import datetime, timedelta
import pytz

from celery import shared_task
from celery.exceptions import MaxRetriesExceededError, Retry
from django import db
from django.db import transaction, OperationalError, InterfaceError
from django.db.models import Count, Q, F
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from google.api_core.exceptions import ResourceExhausted, DeadlineExceeded

from .models import AutomationSettings, ApiKey, PendingContentTask, GeneratedContentChunk, ContentRequest
from academic_structure.models import Subject
from users.models import CustomUser
from contents.services.navigation_builder import refresh_user_navigation
from contents.models import (
    ContentMaterial,
    FreeContentMasterCategory,
    FreeContentSubCategory,
)
from core.services.gemini_service import generate_text_content, generate_audio_content, generate_multimodal_item_content, clean_json_response, AIServiceCriticalError
from core.services.gemini_schemas import ImageItemContentSchema
from media_library.services import search as search_media_images, verify_and_store as verify_media_resource, WikimediaSearchError

from core.services.prompt_generators import (
    generate_course_metadata_prompt,
    generate_master_schema_prompt,
    generate_atomic_content_prompt
)
from messaging.push_utils import send_notification_to_user
from core.utils import send_unified_notification

# --- NUEVAS IMPORTACIONES HITO 6 ---
from assessment_v2.models.main import Exam, ExamSection, ExamItem
from assessment_v2.services.engine.factory import ExamFactory
from assessment_v2.services.engine.logic import AcademicDeductor
from assessment_v2.services.tracking import TrackingService

logger = logging.getLogger(__name__)
User = get_user_model()

QUARANTINE_MAILBOX_FILE = os.path.join(settings.BASE_DIR, "quarantine_requests.log")

# ==============================================================================
# SECCIÓN 1: FUNCIONES AUXILIARES DEL ORQUESTADOR (PRESERVADAS)
# ==============================================================================

def _log_structured_event(message: str, level: str = "INFO", details: dict = None):
    try:
        settings_obj = AutomationSettings.load()
        log_entry = {
            "timestamp": timezone.now().isoformat(),
            "level": level,
            "message": message,
            "details": details or {}
        }
        settings_obj.event_log.insert(0, log_entry)
        settings_obj.event_log = settings_obj.event_log[:100]
        settings_obj.save(update_fields=['event_log'])
    except Exception as e:
        logger.error(f"Error en event_log: {e}")

def _send_admin_notification(title, body):
    try:
        admins = CustomUser.objects.filter(is_superuser=True, is_active=True)
        if not admins.exists(): return
        email_subject = f"[CampuStudiOnline Automation] {title}"
        recipient_list = [admin.email for admin in admins]
        context = {'title': title, 'message_body': body, 'dashboard_url': 'https://www.campustudionline.com/admin/'}
        html_message = render_to_string('orchestrator/email/admin_notification.html', context)
        send_mail(subject=email_subject, message=body, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=recipient_list, fail_silently=True, html_message=html_message)
    except Exception as e:
        logger.error(f"Error notificación admin: {e}")

def _process_quarantine_requests():
    if not os.path.exists(QUARANTINE_MAILBOX_FILE): return
    try:
        with open(QUARANTINE_MAILBOX_FILE, "r") as f:
            key_ids = set(line.strip() for line in f if line.strip().isdigit())
        if not key_ids:
            os.remove(QUARANTINE_MAILBOX_FILE)
            return
        with transaction.atomic():
            ApiKey.objects.filter(id__in=key_ids).update(is_quarantined=True)
        os.remove(QUARANTINE_MAILBOX_FILE)
    except Exception as e:
        logger.error(f"Error procesando buzón: {e}")


def _request_quarantine_via_mailbox(api_key):
    """Solicita cuarentena persistente escribiendo en el buzón (thread-safe)."""
    try:
        with open(QUARANTINE_MAILBOX_FILE, "a") as f:
            f.write(f"{api_key.id}\n")
    except Exception as e:
        logger.error(f"Error solicitando cuarentena: {e}")

def _check_and_perform_daily_reset():
    try:
        automation_settings = AutomationSettings.load()
        madrid_tz = pytz.timezone('Europe/Madrid')
        now_madrid = timezone.now().astimezone(madrid_tz)
        if automation_settings.last_quarantine_reset_date >= now_madrid.date(): return
        if now_madrid.time() >= automation_settings.quarantine_reset_time:
            ApiKey.objects.filter(is_quarantined=True).update(is_quarantined=False)
            automation_settings.last_quarantine_reset_date = now_madrid.date()
            automation_settings.save(update_fields=["last_quarantine_reset_date"])
    except Exception as e:
        logger.error(f"Error reset diario: {e}")

def _purge_zombie_tasks():
    try:
        automation_settings = AutomationSettings.load()
        threshold = timezone.now() - timedelta(hours=automation_settings.zombie_task_threshold_hours)
        PendingContentTask.objects.exclude(status__in=[PendingContentTask.StatusChoices.PROCESSING, PendingContentTask.StatusChoices.COMPLETED]).filter(updated_at__lt=threshold).delete()
    except Exception as e:
        logger.error(f"Error purga zombies: {e}")


# [HITO 38 punto 6] FUSION SEGURA DE media_assets
# ------------------------------------------------------------------
# Defecto documentado en el anexo de H38: `db_item.content['media_assets']
# = [audio_url]` (linea original ~1416) SOBRESCRIBE la lista entera en
# lugar de anadir. Era inocuo mientras no existian imagenes reales; el
# punto 3 las introdujo, y el propio codigo nuevo del punto 3 tenia el
# MISMO patron de sobrescritura en la asignacion de imagen. Hoy audio
# (SD_LIST, arquitectura de idiomas) e imagen (W-CLIN-SCAN/W-ART-IDENT,
# salud/humanidades) nunca coinciden en el mismo item -- pertenecen a
# arquetipos distintos -- asi que el fallo no se ha disparado nunca en
# produccion, pero el patron es fragil por diseno en los dos sitios, no
# solo en el original, y se corrige en ambos con el mismo criterio.
#
# Los audios se detectan por extension .mp3, el mismo criterio que ya
# usan las plantillas de examen (exam_take.html: "not '.mp3' in asset").
def _set_media_asset(content, url, tipo):
    """
    Replace only the entry of the given kind ('audio' or 'imagen') in
    content['media_assets'], preserving any entry of the other kind.
    ---
    Reemplaza solo la entrada del tipo indicado ('audio' o 'imagen') en
    content['media_assets'], preservando cualquier entrada del otro
    tipo. Nunca sobrescribe la lista entera.
    """
    existentes = list(content.get('media_assets') or [])
    if tipo == 'audio':
        conservados = [a for a in existentes if not str(a).lower().endswith('.mp3')]
    else:
        conservados = [a for a in existentes if str(a).lower().endswith('.mp3')]
    content['media_assets'] = conservados + [url]


# [HITO 6] AUDIO GENERATION HELPER / FUNCIÓN AUXILIAR PARA GENERAR AUDIO
# [HITO 38 punto 3+] Prompts por tipo de ejercicio, cada uno alineado con
# la fuente de certificacion real del widget (V06DOC_WIDGETS/V06DOC_BLOCKS)
# en lugar de una redaccion generica que no encaja con ambos dominios.
_CONTEXTOS_IMAGEN_ITEM = {
    'W-CLIN-SCAN': (
        "pidiendo al alumno su interpretacion clinica o tecnica "
        "(hallazgos, semiologia, diagnostico diferencial segun corresponda)"
    ),
    'W-ART-IDENT': (
        "pidiendo al alumno que identifique la obra (autor, titulo, "
        "cronologia, tecnica y soporte, localizacion, estilo/periodo/escuela) "
        "y que redacte despues su analisis en los tres niveles Panofsky "
        "(pre-iconografico, iconografico, iconologico), conforme a la "
        "metodologia certificada del Departamento de Historia del Arte UGR "
        "(V06DOC_BLOCKS, motor EV-ICON-ART)"
    ),
}


def _generate_item_image_content(search_query, api_key, task_id=None, excluir_ids=None, widget_id='W-CLIN-SCAN'):
    """
    [HITO 38 punto 3] Retrieve and verify a real image FIRST, then ask
    Gemini to write the item's stem/keywords about that specific image.
    ---
    [HITO 38 punto 3] Recupera y verifica una imagen real PRIMERO, y
    solo despues le pide a Gemini que redacte el stem/keywords del
    item sobre esa imagen concreta. Es la inversion del flujo que da
    nombre al punto 3: si se pidiera la imagen para una pregunta ya
    escrita, se podria acabar con una radiografia patologica
    ilustrando una pregunta sobre anatomia normal.

    Devuelve un dict {'stem', 'keywords', 'media_url', 'attribution'}
    en exito, o None si no se pudo recuperar ninguna imagen verificada
    o la generacion fallo. Nunca lanza excepcion por un fallo esperable
    (busqueda vacia, imagen rota, cuota agotada): este paso es un
    posprocesado que no debe tumbar el resto de la generacion del
    examen si el catalogo de imagenes falla.

    excluir_ids permite no repetir un recurso ya asignado a otro item
    de la misma seccion: sin esto, dos items con la misma consulta de
    busqueda podrian terminar mostrando la misma imagen.

    widget_id selecciona el marco pedagogico del prompt (ver
    _CONTEXTOS_IMAGEN_ITEM). Ampliado en S027 para cubrir tambien
    W-ART-IDENT (SUB-HUM-ART-HIST), verificado contra V06DOC_WIDGETS.md
    y V06DOC_BLOCKS.md: el widget certificado usa UNA sola obra por
    item, no varias -- la instruccion original de humanities.py que
    pedia 3 imagenes era un defecto respecto a la propia especificacion
    UGR del proyecto, no una necesidad real.
    """
    excluir_ids = excluir_ids or set()
    try:
        resultados = search_media_images(search_query, limit=5)
    except WikimediaSearchError as e:
        logger.warning(f"Busqueda de imagen fallida para '{search_query}': {e}")
        return None

    recurso = None
    for candidato in resultados:
        candidato_recurso, creado = verify_media_resource(candidato, search_query=search_query)
        if candidato_recurso is not None and candidato_recurso.id not in excluir_ids:
            recurso = candidato_recurso
            break
    if recurso is None:
        logger.warning(f"Ningun resultado verificable/nuevo para '{search_query}' (0/{len(resultados)}).")
        return None

    marco_pedagogico = _CONTEXTOS_IMAGEN_ITEM.get(
        widget_id, _CONTEXTOS_IMAGEN_ITEM['W-CLIN-SCAN']
    )
    prompt = (
        f"Consulta academica original: \"{search_query}\".\n"
        f"Se adjunta una imagen real, ya verificada, recuperada de un catalogo "
        f"licenciado para ilustrar esta consulta. Redacta el enunciado (stem) "
        f"describiendo lo que se observa en ESTA imagen concreta, {marco_pedagogico}. "
        f"No inventes ningun dato que no se pueda deducir de la imagen. "
        f"No menciones ninguna URL: la imagen ya esta incluida y se mostrara "
        f"directamente al alumno."
    )
    try:
        recurso.file.open('rb')
        imagen_bytes = recurso.file.read()
        success, resp, _, _ = generate_multimodal_item_content(
            image_bytes=imagen_bytes,
            image_mime_type=recurso.content_type or "image/jpeg",
            prompt=prompt,
            api_key=api_key,
            response_schema=ImageItemContentSchema,
            task_id=task_id,
        )
    except AIServiceCriticalError as e:
        logger.warning(f"Generacion multimodal fallida para '{search_query}': {e}")
        return None
    finally:
        recurso.file.close()

    if not success:
        logger.warning(f"Generacion multimodal sin exito para '{search_query}': {resp}")
        return None

    try:
        parsed = json.loads(clean_json_response(resp))
        stem = str(parsed["stem"]).strip()
        keywords = list(parsed.get("keywords", []))
    except Exception as e:
        logger.warning(f"JSON de generacion multimodal ilegible para '{search_query}': {e}")
        return None
    if not stem:
        return None

    atribucion = recurso.attribution_text or recurso.author or ""
    return {
        "stem": stem,
        "keywords": keywords,
        "media_url": recurso.file.url,
        "attribution": atribucion,
        "license_code": recurso.license.code,
        "license_url": recurso.license_url or recurso.license.url,
        "source_page_url": recurso.source_page_url,
        "resource_id": recurso.id,
    }


def _generate_item_audio(item_id, text, api_key):
    """
    Converts item text to speech and saves to media/assessment/audio/.
    ---
    Convierte el texto del ítem en voz y lo guarda en media/assessment/audio/.
    [FIX S028] generate_audio_content devuelve PCM crudo (mono, 16-bit,
    24kHz -- formato documentado por Google para sus modelos TTS), no un
    MP3 valido. Guardarlo tal cual con extension .mp3 producia un archivo
    que el navegador no podia decodificar (se reproducia silencio, aunque
    el reproductor mostrara movimiento). Se envuelve en un contenedor WAV
    real con el modulo estandar `wave`, igual que el ejemplo oficial de
    Google, y se guarda como .wav.
    """
    try:
        success, audio_bytes, _ = generate_audio_content(text, api_key)
        if success and audio_bytes:
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                wf.writeframes(audio_bytes)
            wav_bytes = wav_buffer.getvalue()

            filename = f"assessment/audio/item_{item_id}.wav"
            if default_storage.exists(filename):
                default_storage.delete(filename)
            path = default_storage.save(filename, ContentFile(wav_bytes))
            return default_storage.url(path)
    except Exception as e:
        logger.error(f"Error generando audio para ítem {item_id}: {e}")
    return None
# ==============================================================================
# SECCIÓN 2: GENERACIÓN DE CONTENIDO (RESTAURADO V24.13)
# ==============================================================================

# --- Newline sentinel / Centinela de salto de linea (S026) ---
# Gemini, called with response_mime_type=application/json and a strict
# response_schema, returns string values with NO newline escapes at all.
# Verified on 2026-07-29 against gemini-2.5-flash: the raw response
# text, before any parsing, arrives as
#   '{"j":"...solicitado.```    INICIOPrograma    DECLARAR..."}'
# with the indentation intact and the line break simply absent. The
# project code is not at fault: clean_json_response, dirtyjson and
# response.text.strip() were each tested in isolation and all three
# preserve newlines. The loss happens at the API boundary, in
# constrained decoding.
#
# The model is therefore instructed to emit an explicit token, restored
# here on the way into the database. Restoring at persistence time and
# not at render time keeps the templates dumb, as com-standards
# requires. The mechanism is additive: if the model omits the token the
# text is stored exactly as it is today, so there is no regression.
# ---
# Gemini, invocado con response_mime_type=application/json y un
# response_schema estricto, devuelve las cadenas SIN ningun escape de
# salto de linea. Verificado el 2026-07-29 contra gemini-2.5-flash: el
# texto crudo de la respuesta, antes de parsear nada, llega como
#   '{"j":"...solicitado.```    INICIOPrograma    DECLARAR..."}'
# con la indentacion intacta y el salto sencillamente ausente. El
# codigo del proyecto no tiene la culpa: clean_json_response, dirtyjson
# y response.text.strip() se probaron por separado y los tres preservan
# los saltos. La perdida ocurre en la frontera con la API, en la
# decodificacion restringida.
#
# Por eso se instruye al modelo para que emita un token explicito, que
# se restituye aqui al entrar en la base de datos. Restituir en la
# persistencia y no en el renderizado mantiene tontas las plantillas,
# como exige com-standards. El mecanismo es aditivo: si el modelo omite
# el token, el texto se guarda igual que hoy, sin regresion.
NEWLINE_SENTINEL = "<<NL>>"

NEWLINE_DIRECTIVE = (
    "\n\n--- DIRECTIVA DE SALTOS DE LINEA (OBLIGATORIA) ---\n"
    "El transporte JSON descarta los saltos de linea reales. En "
    "CUALQUIER campo de texto que generes, escribe cada salto de "
    "linea como el token literal " + NEWLINE_SENTINEL + ", sin "
    "espacios alrededor.\n"
    "Ejemplo de valla de codigo markdown:\n"
    "```pseudocode" + NEWLINE_SENTINEL + "funcion f(n):"
    + NEWLINE_SENTINEL + "  retornar n" + NEWLINE_SENTINEL + "```\n"
    "Ejemplo de lista numerada:\n"
    "1. Primer paso" + NEWLINE_SENTINEL + "2. Segundo paso\n"
    "No uses " + NEWLINE_SENTINEL + " para ninguna otra cosa. Si un "
    "texto no necesita saltos de linea, no incluyas ninguno."
)


def _restore_newlines(node):
    """
    Recursively replace the newline sentinel with real newlines across
    the whole parsed AI payload: item content, grading logic and
    section stimulus alike. Returns plain dict/list containers, which
    is safe because dirtyjson's AttributedDict and AttributedList
    subclass them and the downstream code only uses .get() and
    iteration.
    ---
    Sustituye recursivamente el centinela por saltos de linea reales
    en todo el arbol devuelto por la IA: contenido del item, logica de
    calificacion y estimulo de seccion por igual. Devuelve contenedores
    dict/list planos, lo cual es seguro porque AttributedDict y
    AttributedList de dirtyjson heredan de ellos y el codigo posterior
    solo usa .get() e iteracion.
    """
    if isinstance(node, str):
        return node.replace(NEWLINE_SENTINEL, "\n")
    if isinstance(node, dict):
        return {k: _restore_newlines(v) for k, v in node.items()}
    if isinstance(node, list):
        return [_restore_newlines(v) for v in node]
    return node


def _safe_generate_content(prompt, system_instruction=None, response_schema=None, logger_callback=None):
    """
    [HITO 37 RESTORED] Wrapper de Rotación en Caliente (Hot-Swap).
    Gestiona Errores 429/Cuota, Strikes y Rotación de Keys transparente.
    """
    while True:
        # 1. Sincronización
        automation_settings = AutomationSettings.load()
        api_key = automation_settings.active_api_key
        
        # 2. Validación de Clave Activa
        if not api_key or not api_key.is_enabled or api_key.is_quarantined:
                api_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).order_by('id').first()
                if api_key:
                    automation_settings.active_api_key = api_key
                    automation_settings.save(update_fields=['active_api_key'])
                else:
                    if logger_callback: logger_callback("SIN CLAVES DISPONIBLES. Esperando 5m...", level="ERROR")
                    time.sleep(300)
                    continue

        if logger_callback: logger_callback(f"Llamando a API... (Clave: {api_key.name})")
        
        try:
            # Llamada original
            success, text, key_name, usage = generate_text_content(
                prompt, 
                system_instruction=system_instruction,
                api_key=api_key,
                response_schema=response_schema
            )
        except Exception as e:
            success = False
            text = str(e)
            usage = {}
        
        if success:
            # Limpiar strikes si hubo éxito
            if api_key.consecutive_failures > 0:
                api_key.consecutive_failures = 0
                api_key.save(update_fields=['consecutive_failures'])
            return True, text, api_key.name, usage
        
        else:
            # 3. Gestión de Errores Estándar
            error_str = str(text)
            error_str_upper = error_str.upper()
            is_quota = "429" in error_str_upper or "RESOURCE" in error_str_upper or "QUOTA" in error_str_upper
            
            if is_quota:
                api_key.refresh_from_db()
                api_key.consecutive_failures += 1
                api_key.save(update_fields=["consecutive_failures"])
                
                # ROTACIÓN INMEDIATA (Hot-Swap)

                
                next_k = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).exclude(id=api_key.id).order_by('id').first()

                
                if next_k:

                
                    automation_settings.active_api_key = next_k

                
                    automation_settings.save(update_fields=['active_api_key'])

                
                    if logger_callback: logger_callback(f"ROTACIÓN INMEDIATA (429): Clave {next_k.name}")

                
                else:

                
                    if logger_callback: logger_callback("POOL AGOTADO (429). Esperando 60s...", level="ERROR")

                
                    time.sleep(60)

                
                

                
                if api_key.consecutive_failures >= 4:

                
                    api_key.is_quarantined = True

                
                    api_key.save(update_fields=["is_quarantined"])

                
                    _request_quarantine_via_mailbox(api_key)

                
                    if logger_callback: logger_callback(f"CUARENTENA: Clave {api_key.name} agotó strikes.", level="ERROR")
                continue 
            else:
                # Error no relacionado con cuota (ej: 500, overload), devolvemos el error.
                return False, text, api_key.name, {}

def deep_validate_json_structure(expected, received, path="root"):
    """
    Validación estricta recursiva del esqueleto JSON frente a la salida de la IA.
    Garantiza que la IA actúe solo como máquina de relleno, sin alterar estructura.
    """
    if isinstance(expected, dict):
        if not isinstance(received, dict):
            raise ValueError(f"[{path}] Se esperaba un objeto/diccionario, se recibió {type(received).__name__}")
        for k, v in expected.items():
            if k not in received:
                raise ValueError(f"[{path}] Falta la clave obligatoria: '{k}'")
            deep_validate_json_structure(v, received[k], f"{path}.{k}")
    elif isinstance(expected, list):
        if not isinstance(received, list):
            raise ValueError(f"[{path}] Se esperaba un array/lista, se recibió {type(received).__name__}")
        # No verificamos longitud de lista, la IA rellena los marcadores.

def log_task_event(task_id: str, message: str, is_error: bool = False, payload: dict = None):
    try:
        entry = {"timestamp": datetime.utcnow().isoformat() + "Z", "level": "ERROR" if is_error else "INFO", "message": message}
        if payload: entry["payload"] = str(payload)[:2000]
        with transaction.atomic():
            task = PendingContentTask.objects.select_for_update().get(id=task_id)
            if task.task_log is None: task.task_log = []
            task.task_log.append(entry)
            task.updated_at = timezone.now()
            task.save(update_fields=['task_log', 'updated_at'])
    except Exception as e:
        logger.error(f"Error log_task_event: {e}")

def _parse_master_schema(markdown_text: str) -> list:
    return [(len(hashes), title.strip()) for hashes, title in re.findall(r"^(##+)\s(.*)", markdown_text, re.MULTILINE)]

def _parse_markdown_with_separator(raw_text: str) -> tuple[str, str]:
    sep = r"(?i:^[-*_#]*\s*(?:FUENTES|BIBLIOGRAF[ÍI]A|REFERENCIAS)\s*[-*_#]*$)"
    parts = list(re.finditer(sep, raw_text, re.MULTILINE))
    if parts:
        return raw_text[:parts[-1].start()].strip(), raw_text[parts[-1].end():].strip()
    return raw_text.strip(), ""

def _assemble_final_markdown_from_chunks(course_title: str, metadata: dict, master_schema: str, chunks: list[GeneratedContentChunk]) -> str:
    classification = metadata.get("clasificacion_intelectual", {})
    yaml_header =["---", f'titulo: "{course_title}"', f'descripcion_corta: "{metadata.get("descripcion_corta", "")}"', f'categoria_general: "{classification.get("categoria_general", "Desconocida")}"', f'subcategoria: "{classification.get("subcategoria", "Desconocida")}"', f'palabras_clave: {json.dumps(classification.get("palabras_clave", []))}', "---"]
    parsed_schema = _parse_master_schema(master_schema)
    fuentes_title = "Fuentes y Bibliografía"
    fuentes_slug = slugify(fuentes_title)
    parsed_schema.append((2, fuentes_title))
    toc_entries =[]
    for level, title in parsed_schema:
        slug = slugify(title)
        indent = "    " * (level - 2)
        toc_entries.append(f"{indent}*[{title}](#{slug})")
    introduction =[f"# {course_title}", f"{metadata.get('descripcion_corta', 'Descripción no disponible.')}", '<a id="tabla-de-contenidos"></a>', "## Tabla de Contenidos", "\n".join(toc_entries)]
    content_body =[]
    original_parsed_schema = _parse_master_schema(master_schema)
    chunk_map = {slugify(original_parsed_schema[chunk.order - 1][1]): chunk for chunk in chunks}
    for level, title in original_parsed_schema:
        slug = slugify(title)
        chunk = chunk_map.get(slug)
        content_text = chunk.content if chunk else f"### Error\n\nEl contenido para la sección '{title}' no pudo ser localizado."
        heading_hashes = "#" * level
        content_body.append(f'<a id="{slug}"></a>')
        content_body.append(f"{heading_hashes} {title}")
        content_body.append(content_text)
        if level == 2:
            content_body.append("\n[⬆️ Volver al índice](#tabla-de-contenidos)")
    all_sources_text =[chunk.ai_sources for chunk in chunks if chunk.ai_sources]
    if all_sources_text:
        unique_references = set()
        for source_block in all_sources_text:
            for line in source_block.split('\n'):
                cleaned_line = line.strip()
                if cleaned_line:
                    unique_references.add(cleaned_line)
        sorted_references = sorted(list(unique_references))
        formatted_bibliography = "\n".join(f"- {ref}" for ref in sorted_references)
        bibliography_section =[f'<a id="{fuentes_slug}"></a>', f"## {fuentes_title}", formatted_bibliography, "\n[⬆️ Volver al índice](#tabla-de-contenidos)"]
        content_body.extend(bibliography_section)
    final_parts = yaml_header + introduction + content_body
    return "\n\n".join(final_parts)

def _get_or_create_free_categories_from_classification(classification_data: dict, course_title: str) -> tuple:
    master_name = classification_data.get("categoria_general")
    sub_name = classification_data.get("subcategoria")
    if not master_name:
        logger.warning(f"No se encontró 'categoria_general' en la clasificación para '{course_title}'. No se puede clasificar.")
        return None, None
    master_category, _ = FreeContentMasterCategory.objects.get_or_create(name=master_name)
    sub_category = None
    if sub_name:
        sub_category, _ = FreeContentSubCategory.objects.get_or_create(master_category=master_category, name=sub_name)
    return master_category, sub_category

def _send_completion_notifications(new_content: ContentMaterial):
    try:
        first_subject = new_content.subject.first()
        if not first_subject: return
        content_request = ContentRequest.objects.filter(subject=first_subject).first()
        if not content_request: return
        requesters = content_request.requesters.all()
        if not requesters: return
        content_url = new_content.get_absolute_url()
        full_url = f"https://{settings.ALLOWED_HOSTS[0]}{content_url}"
        push_title = "¡Contenido Disponible!"
        push_body = f"El material de estudio para '{new_content.title}' ya está disponible."
        email_subject = f"[CampuStudiOnline] El contenido para '{new_content.title}' está listo"
        email_body_text = (f"¡Hola!\n\nNos complace informarte que el material de estudio para la asignatura '{new_content.title}' que solicitaste ha sido generado y ya está disponible en la plataforma.\n\n"
                           f"Puedes acceder a él directamente a través del siguiente enlace:\n{full_url}\n\n"
                           f"Gracias por tu paciencia y por ayudarnos a mejorar CampuStudiOnline.\n\n"
                           f"Atentamente,\nEl equipo de CampuStudiOnline")
        context = {'content_title': new_content.title, 'content_url': full_url}
        html_message = render_to_string('orchestrator/email/content_completion.html', context)
        for user in requesters:
            send_notification_to_user(user, push_title, push_body, url=content_url)
            send_mail(subject=email_subject, message=email_body_text, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[user.email], fail_silently=True, html_message=html_message)
        content_request.status = ContentRequest.StatusChoices.FULFILLED
        content_request.save(update_fields=["status"])
    except Exception as e:
        logger.error(f"Error notifications: {e}")

def _send_exam_failure_notification(exam):
    """
    Notifies the user via Email and Push about a fatal generation error.
    Notifica al usuario vía Email y Push sobre un error fatal de generación.
    Ref: V06DOC_LOGIC_MAPPING Section 3 (Incidencia 27).
    """
    try:
        from django.utils.translation import gettext as _
        subject = _("[CampuStudiOnline] Error en la generación de tu evaluación")
        body_text = _(
            f"Hola,\n\nLamentamos informarte que el servicio de generación de exámenes no está disponible temporalmente "
            f"para la asignatura '{exam.content_copy.original_content.title}'.\n\n"
            "Por favor, inténtalo de nuevo más tarde. No se ha realizado ningún cargo en tu cuota semanal.\n\n"
            "Disculpa las molestias.\nEl equipo de CampuStudiOnline"
        )
        
        context = {
            'course_title': exam.content_copy.original_content.title,
            'dashboard_url': f"https://{settings.ALLOWED_HOSTS[0]}/"
        }
        html_message = render_to_string('orchestrator/email/exam_failure.html', context)

        send_mail(
            subject=subject,
            message=body_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[exam.user.email],
            fail_silently=True,
            html_message=html_message
        )
        
        send_unified_notification(
            exam.user, 
            _("Servicio no disponible"), 
            _("No se pudo generar el examen. Por favor, inténtelo de nuevo más tarde."), 
            reverse('assessment_v2:dashboard')
        )
    except Exception as e:
        logger.error(f"Error en _send_exam_failure_notification: {e}")


def _get_next_subject_queryset(settings_obj):
    base_queryset = Subject.objects.filter(content_materials__isnull=True)
    active_task_subject_names = PendingContentTask.objects.exclude(status__in=[PendingContentTask.StatusChoices.COMPLETED, PendingContentTask.StatusChoices.FAILED_FATAL]).values_list('subject__name', flat=True).distinct()
    query = base_queryset.exclude(name__in=active_task_subject_names)
    if settings_obj.seed_branch: query = query.filter(academic_year__degree__branch=settings_obj.seed_branch)
    if settings_obj.seed_degree: query = query.filter(academic_year__degree=settings_obj.seed_degree)
    return query

# ==============================================================================
# SECCIÓN 3: TAREAS CELERY - CONTENIDO (PRESERVADA)
# ==============================================================================

def _advance_seed_filters_if_needed(automation_settings):
    if not any([automation_settings.seed_branch, automation_settings.seed_degree, automation_settings.seed_year]):
        return False
    from academic_structure.models import Subject
    from .models import PendingContentTask
    base_queryset = Subject.objects.filter(content_materials__isnull=True)
    active_task_subject_names = PendingContentTask.objects.exclude(status__in=[PendingContentTask.StatusChoices.COMPLETED, PendingContentTask.StatusChoices.FAILED_FATAL]).values_list('subject__name', flat=True).distinct()
    query = base_queryset.exclude(name__in=active_task_subject_names)
    if automation_settings.seed_branch: query = query.filter(academic_year__degree__branch=automation_settings.seed_branch)
    if automation_settings.seed_degree: query = query.filter(academic_year__degree=automation_settings.seed_degree)
    
    if not query.exists():
        if automation_settings.seed_year:
            automation_settings.seed_year = ""
            automation_settings.save(update_fields=['seed_year'])
            return True
        if automation_settings.seed_degree:
            automation_settings.seed_degree = None
            automation_settings.save(update_fields=['seed_degree'])
            return True
        if automation_settings.seed_branch:
            automation_settings.seed_branch = None
            automation_settings.save(update_fields=['seed_branch'])
            return True
    return False

@shared_task(bind=True)
def global_orchestrator_task(self):
    try:
        db.close_old_connections()
        # [HOTFIX] DEBOUNCE: Evitar ejecuciones superpuestas
        try:
            settings_check = AutomationSettings.load()
            if settings_check.last_run_timestamp:
                delta = timezone.now() - settings_check.last_run_timestamp
                if delta.total_seconds() < 45:
                    logger.warning(f'ORCHESTRATOR DEBOUNCE: Ejecución omitida (Delta: {delta.total_seconds():.1f}s < 45s).')
                    return
        except Exception:
            pass

        _purge_zombie_tasks()
        _process_quarantine_requests()
        _check_and_perform_daily_reset()
        
        automation_settings = AutomationSettings.load()
        if not automation_settings.is_running:
            status_msg = "DETENIDO: Interruptor maestro desactivado."
            if automation_settings.last_run_status != status_msg:
                _log_structured_event(status_msg, "INFO")
                automation_settings.last_run_status = status_msg
                automation_settings.save(update_fields=['last_run_status'])
            return
            
        active_key = automation_settings.active_api_key
        if active_key:
            active_key.refresh_from_db()
            
        if not active_key or not active_key.is_enabled or active_key.is_quarantined:
            _log_structured_event("SINCRO: Clave activa no es válida. Buscando reemplazo.", "INFO")
            next_available_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).order_by('id').first()
            if next_available_key:
                automation_settings.active_api_key = next_available_key
                automation_settings.save(update_fields=['active_api_key'])
                _log_structured_event(f"SINCRO EXITOSA: Nueva clave activa es '{next_available_key.name}'.", "INFO")
            else:
                status_msg = "HIBERNANDO (POOL AGOTADO): No hay claves disponibles."
                if automation_settings.last_run_status != status_msg:
                    _log_structured_event(status_msg, "WARNING")
                    automation_settings.last_run_status = status_msg
                    automation_settings.save(update_fields=['last_run_status'])
                return
        
        automation_settings.refresh_from_db()

        # Rescate de Tareas de Contenido Zombies/Fallidas
        zombie_threshold = timezone.now() - timedelta(minutes=5)
        zombie_content_tasks = PendingContentTask.objects.filter(
            status__in=[PendingContentTask.StatusChoices.PROCESSING, PendingContentTask.StatusChoices.PENDING], 
            updated_at__lt=zombie_threshold
        )
        for task in zombie_content_tasks:
            _log_structured_event(f"VIGILANTE: Tarea '{task.id}' ZOMBIE rescatada.", "WARNING")
            task.status = PendingContentTask.StatusChoices.FAILED_RETRYABLE
            task.save(update_fields=["status"])
            
        task_to_rescue = PendingContentTask.objects.filter(
            status__in=[PendingContentTask.StatusChoices.FAILED_RETRYABLE, PendingContentTask.StatusChoices.FAILED_QUOTA]
        ).order_by('created_at').first()
        
        if task_to_rescue:
            _log_structured_event(f"RESCATE: Re-encolando la tarea de contenido {task_to_rescue.id}.", "INFO")
            sc = task_to_rescue.structured_content or {}
            if sc.get("consecutive_quota_errors", 0) > 0:
                sc["consecutive_quota_errors"] = 0
                task_to_rescue.structured_content = sc
            task_to_rescue.status = PendingContentTask.StatusChoices.PENDING
            task_to_rescue.save(update_fields=["status", "structured_content"])
            generate_full_course_task.delay(str(task_to_rescue.id))
            
            automation_settings.last_run_status = f"AUTO-RECUPERACIÓN: Tarea re-encolada."
            automation_settings.last_run_timestamp = timezone.now()
            automation_settings.save(update_fields=['last_run_status', 'last_run_timestamp'])
            return

                # PRIORIDAD 0: Evaluaciones/Exámenes (HITO 6 - MÁXIMA PRIORIDAD)
        pending_exam = Exam.objects.filter(status='PENDING').order_by('created_at').first()
        if pending_exam:
            _log_structured_event(f"PRIORIDAD 0 (EXAM): Procesando examen {pending_exam.uuid}.", "INFO")
            
            # Marcamos actividad para evitar condiciones de carrera
            pending_exam.updated_at = timezone.now()
            pending_exam.save(update_fields=['updated_at'])
            
            generate_exam_task.delay(str(pending_exam.uuid))
            
            status_msg = f"TAREA LANZADA (EXAM): '{pending_exam.uuid}'."
            automation_settings.last_run_status = status_msg
            automation_settings.last_run_timestamp = timezone.now()
            automation_settings.save(update_fields=['last_run_status', 'last_run_timestamp'])
            return

        # PRIORIDAD 1: Solicitudes de Usuarios (ContentRequest)
        approved_request = ContentRequest.objects.filter(status=ContentRequest.StatusChoices.APPROVED).order_by('created_at').first()
        if approved_request and approved_request.subject.content_materials.count() == 0:
            subject_to_process = approved_request.subject
            with transaction.atomic():
                req = ContentRequest.objects.select_for_update().get(id=approved_request.id)
                req.status = ContentRequest.StatusChoices.IN_PROGRESS
                req.save(update_fields=["status"])
            
            admin_user = CustomUser.objects.filter(is_superuser=True, is_active=True).order_by('pk').first()
            new_task = PendingContentTask.objects.create(
                subject=subject_to_process, 
                assigned_to=admin_user, 
                task_origin=PendingContentTask.TaskOrigin.APPROVED_REQUEST
            )
            generate_full_course_task.delay(str(new_task.id))
            
            status_msg = f"TAREA LANZADA (REQUEST): '{subject_to_process.name}'."
            _log_structured_event(status_msg, "INFO")
            automation_settings.last_run_status = status_msg
            automation_settings.last_run_timestamp = timezone.now()
            automation_settings.save(update_fields=['last_run_status', 'last_run_timestamp'])
            return

        if PendingContentTask.objects.filter(status__in=[PendingContentTask.StatusChoices.PROCESSING, PendingContentTask.StatusChoices.PENDING]).exists():
            status_msg = "EN ESPERA: Hay tareas de contenido activas."
            if automation_settings.last_run_status != status_msg:
                automation_settings.last_run_status = status_msg
                automation_settings.save(update_fields=['last_run_status'])
            return

        # CONTROL DE GENERACIÓN MASIVA
        if not automation_settings.is_mass_generation_enabled:
            status_msg = "AHORRO DE ENERGÍA: Generación masiva desactivada. A la espera de solicitudes manuales."
            if automation_settings.last_run_status != status_msg:
                _log_structured_event(status_msg, "INFO")
                automation_settings.last_run_status = status_msg
                automation_settings.save(update_fields=['last_run_status'])
            return

        # PRIORIDAD 2: Generación Masiva (Mass Generation)
        while True:
            subject_qs = _get_next_subject_queryset(automation_settings)
            subject_to_process = subject_qs.order_by('?').first()
            if subject_to_process:
                admin_user = CustomUser.objects.filter(is_superuser=True, is_active=True).order_by('pk').first()
                new_task = PendingContentTask.objects.create(
                    subject=subject_to_process, 
                    assigned_to=admin_user, 
                    task_origin=PendingContentTask.TaskOrigin.MASS_GENERATION
                )
                generate_full_course_task.delay(str(new_task.id))
                
                status_msg = f"TAREA LANZADA (MASS-GEN): '{subject_to_process.name}'."
                _log_structured_event(status_msg, "INFO")
                automation_settings.last_run_status = status_msg
                automation_settings.last_run_timestamp = timezone.now()
                automation_settings.save(update_fields=['last_run_status', 'last_run_timestamp'])
                break
            else:
                if _advance_seed_filters_if_needed(automation_settings):
                    continue
                else:
                    final_message = "SIN TRABAJO: No quedan más asignaturas para procesar."
                    if automation_settings.last_run_status != final_message:
                        _log_structured_event(final_message, "INFO")
                        automation_settings.last_run_status = final_message
                        automation_settings.save(update_fields=['last_run_status'])
                    break

    except Exception as e:
        logger.critical(f"Error orquestador: {e}", exc_info=True)


@shared_task(bind=True, time_limit=21600, acks_late=True, rate_limit='12/m')
def generate_full_course_task(self, task_id):
    db.close_old_connections()
    logger.info(f"[V24.14 503-AWARE] Iniciando Tarea {task_id}.")
    task = None
    api_key = None
    try:
        # --- BLOQUE DE INICIALIZACIÓN Y FUSIBLE ---
        time.sleep(2)
        automation_settings = AutomationSettings.load()
        api_key = automation_settings.active_api_key
        
        if not api_key or not api_key.is_enabled or api_key.is_quarantined:
             next_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).order_by('id').first()
             if next_key:
                 automation_settings.active_api_key = next_key
                 automation_settings.save(update_fields=['active_api_key'])
                 api_key = next_key
             else:
                 log_task_event(task_id, "HIBERNACIÓN: No hay claves disponibles al inicio.", is_error=True)
                 time.sleep(60)
                 raise self.retry(countdown=900)

        task = PendingContentTask.objects.select_related('subject__academic_year__degree__branch__university', 'subject__content_hash_family').get(id=task_id)
        
        if task.status == PendingContentTask.StatusChoices.FAILED_FATAL:
            logger.warning(f"DRENAJE: Tarea {task_id} ya es FATAL. Omitiendo ejecución para vaciar cola.")
            return

        PendingContentTask.objects.filter(id=task_id).update(global_actuation_count=F('global_actuation_count') + 1)
        task.refresh_from_db(fields=['global_actuation_count'])
        
        limit_actuations = automation_settings.max_task_actuations
        if task.global_actuation_count > limit_actuations:
            msg = f"FUSIBLE FUNDIDO: {task.global_actuation_count}/{limit_actuations}."
            log_task_event(task_id, msg, is_error=True)
            task.status = PendingContentTask.StatusChoices.FAILED_FATAL
            task.notes = f"{task.notes} | {msg}"
            task.save(update_fields=["status", "notes"])
            return

        if not task.log_file_path:
            log_dir = os.path.join(settings.BASE_DIR, "logs", "content_automation")
            os.makedirs(log_dir, exist_ok=True)
            task.log_file_path = os.path.join(log_dir, f"task_{task_id}.log")
            task.save(update_fields=["log_file_path"])

        if task.status in[PendingContentTask.StatusChoices.PENDING, PendingContentTask.StatusChoices.FAILED_RETRYABLE, PendingContentTask.StatusChoices.FAILED_QUOTA]:
            task.status = PendingContentTask.StatusChoices.PROCESSING
            task.save(update_fields=["status"])
            log_task_event(task_id, "Tarea iniciada (Status -> PROCESSING).")

        # --- FASE 1: GENERACIÓN DE PLAN ---
        if not task.structured_content or "master_schema" not in task.structured_content:
            log_task_event(task_id, "Generando Plan de Trabajo...")
            
            while True: 
                task.refresh_from_db(fields=["status"])
                if task.status == PendingContentTask.StatusChoices.PAUSED:
                    log_task_event(task_id, "PAUSA ADMIN DETECTADA.")
                    self.retry(countdown=600)
                    return

                automation_settings = AutomationSettings.load()
                api_key = automation_settings.active_api_key
                if not api_key or not api_key.is_enabled or api_key.is_quarantined:
                     api_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).order_by('id').first()
                     if api_key:
                         automation_settings.active_api_key = api_key
                         automation_settings.save(update_fields=['active_api_key'])
                     else:
                         log_task_event(task_id, "SIN CLAVES (INIT). Esperando...", is_error=True)
                         time.sleep(300)
                         continue

                course_title = task.course_title or (task.subject.name if task.subject else "Curso sin título")
                if task.subject:
                    topic_description = task.subject.name
                    degree = task.subject.academic_year.degree
                    academic_context = f"- Universidad: {degree.branch.university.name}\n- Rama: {degree.branch.name}\n- Titulación: {degree.name}"
                    learning_objectives = json.dumps(task.subject.learning_objectives, ensure_ascii=False) if task.subject.learning_objectives else ""
                    syllabus = json.dumps(task.subject.course_content_outline, ensure_ascii=False) if task.subject.course_content_outline else ""
                else:
                    topic_description = task.prompt_text
                    academic_context = ""
                    learning_objectives = ""
                    syllabus = ""
                    
                metadata_prompt = generate_course_metadata_prompt(topic_description, academic_context) + "\n\nJSON Only."
                
                try:
                    success, response_text, _, _ = generate_text_content(metadata_prompt, api_key=api_key, task_id=task_id)
                except Exception as ex:
                    success = False
                    response_text = str(ex)

                if not success:
                    error_str = str(response_text)
                    error_str_upper = error_str.upper()
                    is_quota = "429" in error_str_upper or "RESOURCE" in error_str_upper or "QUOTA" in error_str_upper
                    is_server_overload = "503" in error_str_upper or "UNAVAILABLE" in error_str_upper or "OVERLOAD" in error_str_upper
                    
                    if is_server_overload:
                        log_task_event(task_id, f"GOOGLE OVERLOAD (503). Esperando 45s antes de reintentar con {api_key.name}...", is_error=True)
                        time.sleep(45)
                        # NO rotamos, NO sumamos strike. Simplemente reintentamos el bucle.
                        continue

                    if is_quota:
                        api_key.refresh_from_db()
                        api_key.consecutive_failures += 1
                        api_key.save(update_fields=["consecutive_failures"])
                        # ROTACIÓN INMEDIATA (Hot-Swap)

                        next_k = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).exclude(id=api_key.id).order_by('id').first()

                        if next_k:

                            automation_settings.active_api_key = next_k

                            automation_settings.save(update_fields=['active_api_key'])

                            log_task_event(task_id, f"ROTACIÓN INMEDIATA (429): Nueva clave {next_k.name}.")

                        else:

                            log_task_event(task_id, "POOL AGOTADO (429). Esperando 60s...", is_error=True)

                            time.sleep(60)

                        

                        if api_key.consecutive_failures >= 4:

                            api_key.is_quarantined = True

                            api_key.save(update_fields=["is_quarantined"])

                            _request_quarantine_via_mailbox(api_key)

                            log_task_event(task_id, f"CUARENTENA: Clave {api_key.name} agotó strikes.", is_error=True)
                        continue 
                    else:
                        log_task_event(task_id, f"ERROR INIT NO-CUOTA: {error_str}. Reintentando en 30s...", is_error=True)
                        time.sleep(30)
                        continue

                cleaned_json_str = clean_json_response(response_text)
                metadata = json.loads(cleaned_json_str)
                
                schema_prompt = generate_master_schema_prompt(topic_description, academic_context, learning_objectives, syllabus)
                
                try:
                    success, schema_or_error, _, _ = generate_text_content(schema_prompt, api_key=api_key, task_id=task_id)
                except Exception as ex:
                    success = False
                    schema_or_error = str(ex)
                
                if not success:
                    error_str = str(schema_or_error)
                    error_str_upper = error_str.upper()
                    is_quota = "429" in error_str_upper or "RESOURCE" in error_str_upper or "QUOTA" in error_str_upper
                    is_server_overload = "503" in error_str_upper or "UNAVAILABLE" in error_str_upper or "OVERLOAD" in error_str_upper

                    if is_server_overload:
                        log_task_event(task_id, f"GOOGLE OVERLOAD (503) en ESQUEMA. Esperando 45s...", is_error=True)
                        time.sleep(45)
                        continue

                    if is_quota:
                        api_key.refresh_from_db()
                        api_key.consecutive_failures += 1
                        api_key.save(update_fields=["consecutive_failures"])
                        if api_key.consecutive_failures >= 4:
                            api_key.is_quarantined = True
                            api_key.save(update_fields=["is_quarantined"])
                            _request_quarantine_via_mailbox(api_key)
                            next_k = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).exclude(id=api_key.id).first()
                            if next_k:
                                automation_settings.active_api_key = next_k
                                automation_settings.save(update_fields=['active_api_key'])
                                log_task_event(task_id, f"ROTACIÓN (INIT): Nueva clave {next_k.name}.")
                            else:
                                time.sleep(60)
                        else:
                            log_task_event(task_id, f"STRIKE INIT {api_key.consecutive_failures}/4. Esperando 60s...", is_error=True)
                            time.sleep(60)
                        continue 
                    else:
                        log_task_event(task_id, f"ERROR INIT ESQUEMA NO-CUOTA: {error_str}. Reintentando en 30s...", is_error=True)
                        time.sleep(30)
                        continue
                
                if api_key.consecutive_failures > 0:
                    api_key.consecutive_failures = 0
                    api_key.save(update_fields=['consecutive_failures'])

                master_schema_md = schema_or_error
                section_count = len(_parse_master_schema(master_schema_md))
                
                new_structured_content = {"metadata": metadata, "master_schema": master_schema_md, "academic_context": academic_context}
                if task.structured_content and task.structured_content.get('manual_classification'):
                    new_structured_content['manual_classification'] = task.structured_content['manual_classification']
                    
                task.section_count = section_count
                task.structured_content = new_structured_content
                task.save(update_fields=["structured_content", "section_count"])
                log_task_event(task_id, f"Plan generado: {section_count} secciones.")
                break 

        # --- FASE 2: GENERACIÓN DE CHUNKS ---
        task.refresh_from_db()
        parsed_schema = _parse_master_schema(task.structured_content["master_schema"])
        
        for index, (_, title) in enumerate(parsed_schema):
            db.close_old_connections()
            order = index + 1
            
            if GeneratedContentChunk.objects.filter(task=task, order=order).exists():
                continue

            while True:
                task.refresh_from_db(fields=["status"])
                if task.status == PendingContentTask.StatusChoices.PAUSED:
                    log_task_event(task_id, "PAUSA ADMIN DETECTADA.")
                    self.retry(countdown=600)
                    return

                automation_settings = AutomationSettings.load()
                api_key = automation_settings.active_api_key
                
                if not api_key or not api_key.is_enabled or api_key.is_quarantined:
                     api_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).order_by('id').first()
                     if api_key:
                         automation_settings.active_api_key = api_key
                         automation_settings.save(update_fields=['active_api_key'])
                     else:
                         log_task_event(task_id, "SIN CLAVES. Esperando...", is_error=True)
                         time.sleep(300)
                         continue

                academic_context = task.structured_content.get("academic_context", "")
                initial_prompt = generate_atomic_content_prompt(
                    course_title=task.course_title or task.subject.name, 
                    section_title=title, 
                    master_schema=task.structured_content["master_schema"], 
                    academic_context=academic_context
                )
                
                log_task_event(task_id, f'Generando {order}/{len(parsed_schema)}: "{title}" (Key: {api_key.name})')

                try:
                    success, content_or_error, _, _ = generate_text_content(initial_prompt, api_key=api_key, task_id=task_id)
                except Exception as ex:
                    success = False
                    content_or_error = str(ex)

                if success:
                    content_text, sources_text = _parse_markdown_with_separator(content_or_error)
                    GeneratedContentChunk.objects.create(task=task, order=order, content=content_text, ai_sources=sources_text)
                    log_task_event(task_id, f"Sección {order} guardada OK.")
                    
                    if api_key.consecutive_failures > 0:
                        log_task_event(task_id, f"CLAVE RECUPERADA: {api_key.name} (Reset contador).")
                        api_key.consecutive_failures = 0
                        api_key.save(update_fields=['consecutive_failures'])
                    
                    time.sleep(5)
                    break 

                else:
                    error_str = str(content_or_error)
                    error_str_upper = error_str.upper()
                    is_quota = "429" in error_str_upper or "RESOURCE" in error_str_upper or "QUOTA" in error_str_upper
                    is_server_overload = "503" in error_str_upper or "UNAVAILABLE" in error_str_upper or "OVERLOAD" in error_str_upper

                    if is_server_overload:
                        log_task_event(task_id, f"GOOGLE OVERLOAD (503). Esperando 45s antes de reintentar con {api_key.name}...", is_error=True)
                        time.sleep(45)
                        # NO rotamos, NO sumamos strike.
                        continue

                    if is_quota:
                        api_key.refresh_from_db()
                        api_key.consecutive_failures += 1
                        api_key.save(update_fields=["consecutive_failures"])
                        fails = api_key.consecutive_failures

                        # ROTACIÓN INMEDIATA CHUNK

                        next_k = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).exclude(id=api_key.id).order_by('id').first()

                        if next_k:

                            automation_settings.active_api_key = next_k

                            automation_settings.save(update_fields=['active_api_key'])

                            log_task_event(task_id, f"ROTACIÓN INMEDIATA CHUNK (429): Nueva clave {next_k.name}.")

                        else:

                            log_task_event(task_id, "POOL AGOTADO CHUNK (429). Esperando 60s...", is_error=True)

                            time.sleep(60)

                        

                        if fails >= 4:

                            api_key.is_quarantined = True

                            api_key.save(update_fields=["is_quarantined"])

                            _request_quarantine_via_mailbox(api_key)

                            log_task_event(task_id, f"CUARENTENA CHUNK: Clave {api_key.name} agotada.", is_error=True)
                    else:
                        log_task_event(task_id, f"ERROR CHUNK NO-CUOTA: {error_str}. Reintentando en 30s.", is_error=True)
                        time.sleep(30)

        # --- FINALIZACIÓN ---
        task.refresh_from_db()
        if task.content_chunks.count() >= len(parsed_schema):
            log_task_event(task_id, "Ensamblando curso final...")
            final_course_title = task.subject.name if task.subject else task.course_title
            final_markdown = _assemble_final_markdown_from_chunks(final_course_title, task.structured_content["metadata"], task.structured_content["master_schema"], list(task.content_chunks.all()))
            
            master_category, sub_category = None, None
            manual = task.structured_content.get('manual_classification')
            if task.subject: pass 
            elif manual:
                try:
                    master_category = FreeContentMasterCategory.objects.get(id=manual['master_category_id'])
                    if manual.get('sub_category_id'): sub_category = FreeContentSubCategory.objects.get(id=manual['sub_category_id'])
                except: pass
            
            with transaction.atomic():
                task_final = PendingContentTask.objects.select_for_update().get(id=task_id)
                is_free = task_final.subject is None
                if task_final.content_material:
                    nm = task_final.content_material
                    nm.markdown_content = final_markdown
                    nm.save()
                else:
                    nm = ContentMaterial.objects.create(title=final_course_title, short_description=task_final.structured_content["metadata"].get("descripcion_corta", ""), markdown_content=final_markdown, master_category=master_category, sub_category=sub_category, creator=task_final.assigned_to, is_free_content=is_free, is_public=True)
                if not is_free and task_final.subject:
                     fam = task_final.subject.content_hash_family
                     if fam: 
                         fam.content_material = nm
                         fam.save()
                         nm.subject.add(*fam.subjects.all())
                     else:
                         nm.subject.add(task_final.subject)
                task_final.content_material = nm
                task_final.status = PendingContentTask.StatusChoices.COMPLETED
                task_final.save(update_fields=["status", "content_material"])
            _send_completion_notifications(nm)
            log_task_event(task_id, "TAREA COMPLETADA EXITOSAMENTE.")

    except Exception as e:
        err_str = str(e)
        is_transient = isinstance(e, (TimeoutError, ConnectionError, OSError, OperationalError, InterfaceError)) or "Resource" in err_str or "429" in err_str or "Quota" in err_str
        
        if is_transient:
             log_task_event(task_id, f"Error Transitorio Global (Escape): {err_str}. Reintentando...", is_error=True)
             raise self.retry(exc=e, countdown=300)
        else:
             log_task_event(task_id, f"ERROR FATAL DE CÓDIGO: {err_str}", is_error=True)
             if task:
                 task.status = PendingContentTask.StatusChoices.FAILED_FATAL
                 task.last_error = traceback.format_exc()
                 task.save(update_fields=["status", "last_error"])

    finally:
        db.close_old_connections()

# ==============================================================================
# HITO 6: GENERACIÓN DE EXAMEN (SKELETON-FIRST ATÓMICO)
# ==============================================================================

@shared_task(bind=True, time_limit=1800, max_retries=3)
def generate_exam_task(self, exam_uuid, context_text=None, topic=None):
    db.close_old_connections()
    exam = None
    try:
        exam = Exam.objects.select_related('user', 'content_copy').get(uuid=exam_uuid)
        if self.request.retries == 0:
            exam.status = 'GENERATING'
            exam.event_log.append({"ts": timezone.now().isoformat(), "msg": f"Iniciando Skeleton-First (Examen: {str(exam.uuid)[:8]})"})
            exam.save(update_fields=['status', 'event_log'])

        material = exam.content_copy.original_content
        subject = material.subject.first()
        
        # PROTOCOLO DE RESILIENCIA (10 MIN RETRY)
        try:
            exam.event_log.append({"ts": timezone.now().isoformat(), "msg": "Iniciando clasificación de asignatura (IA)..."})
            exam.save(update_fields=['event_log'])
            metadata = AcademicDeductor.get_context_metadata(subject, context_title=material.title)
            exam.event_log.append({"ts": timezone.now().isoformat(), "msg": f"Clasificación completada. Archetype: {metadata.get('archetype_id', 'Unknown')}"})
            exam.save(update_fields=['event_log'])
        except AIServiceCriticalError as e:
            exam.event_log.append({"ts": timezone.now().isoformat(), "msg": "API Clasificación Fallida. Reintento 10min."})
            exam.save(update_fields=['event_log'])
            raise self.retry(exc=e, countdown=600)
        
        exam.archetype_id = metadata['archetype_id']
        exam.sub_archetype_id = metadata['sub_archetype_id']
        exam.itinerary_id = metadata['itinerary_id']
        exam.pedagogical_level = metadata['pedagogical_level']
        # [Strategy Delegation] Immersion mode logic moved to strategy
        exam.target_language_code = metadata.get('target_language_code', 'es')
        exam.localized_sections = metadata.get('localized_sections', {})
        
        strategy = ExamFactory.get_strategy(
            archetype_id=exam.archetype_id,
            sub_archetype_id=exam.sub_archetype_id,
            pedagogical_level=exam.pedagogical_level,
            itinerary_id=exam.itinerary_id,
            target_language_code=exam.target_language_code,
            localized_sections=exam.localized_sections
        )
        exam.immersion_mode = strategy.get_immersion_mode()
        exam.grading_params = strategy._get_grading_params()
        # [HITO 6 FIX] Discrepancia 1: Secuencialidad obligatoria para Lenguas
        if exam.archetype_id == 'ARCH_LANG':
            exam.is_sequential = True
        exam.save()

        # FASE ESTRUCTURAL (Skeleton-First Fijo)
        skeleton = strategy.get_exam_skeleton()
        with transaction.atomic():
            exam.sections.all().delete()
            sections_map = {}
            for idx, s_data in enumerate(skeleton):
                section = ExamSection.objects.create(
                    exam=exam, 
                    subdivision_id=s_data['subdivision_id'], 
                    title=s_data['title'],
                    instructions=s_data.get('instructions', ''), 
                    time_limit=s_data.get('time_limit', 0),
                    layout_mode=s_data.get('layout_mode', 'STANDARD'),
                    order=idx
                )
                # Indexar por orden (idx) y por subdivision_id.
                # El índice por orden evita colisiones cuando dos secciones
                # distintas tienen el mismo subdivision_id (ej: SUB-HUM-MUS).
                sections_map[idx] = section
                
                # Crear ítems vacíos con el esqueleto predefinido
                for i_idx, i_data in enumerate(s_data.get('items', [])):
                    ExamItem.objects.create(
                        section=section,
                        block_type=i_data.get('block_type', 'UNKNOWN'),
                        widget_id=i_data.get('widget_id', 'UNKNOWN'),
                        # [HITO 6] FIX: Inyección de parámetros técnicos de la Estrategia
                        level_requisite=i_data.get('level_requisite', 'MANDATORY'),
                        weight=i_data.get('weight', 1.00),
                        estimated_time=i_data.get('estimated_time', 0),
                        fail_logic=i_data.get('fail_logic', 'PENALTY'),
                        content={},
                        grading_logic={},
                        # [HITO 6] SKELETON-PROMPT BINDING: Persistir la instrucción de llenado
                        metadata={'task_instruction': i_data.get('task_instruction', '')},
                        order=i_idx
                    )
        
        # FASE DE LLENADO ATÓMICO (Bucle Iterativo por Sección)
        generated_titles = []
        usage_total = {"in": 0, "out": 0}
        # [HITO 38 punto 7 - correccion tras E2E real] El conjunto de
        # recursos ya usados debe vivir a nivel de EXAMEN, no de seccion.
        # Verificado en produccion el 2026-07-30: dos secciones distintas
        # (SD_ANAT_MACRO y SD_ANAT_RADIO) con la misma consulta de
        # busqueda (topic="Anatomia") terminaron mostrando la MISMA
        # imagen, porque el conjunto se reiniciaba en cada seccion y
        # ninguna de las dos veia lo que la otra ya habia usado.
        recursos_usados_examen = set()

        for s_idx, s_info in enumerate(skeleton):
            db_sec = sections_map.get(s_idx)
            if not db_sec: continue
            
            # [FIX 2026-07-27] db_items debe resolverse ANTES de construir
            # section_skeleton_json, que lo itera. La asignación vivía DESPUÉS de
            # ese uso, lo que producía UnboundLocalError en la primera sección de
            # todo examen. El fallo era inalcanzable mientras la llamada a la IA
            # reventaba antes por 'additionalProperties' en el response_schema;
            # aflora al corregir aquello (ff562bb). Se sube tambien la guarda de
            # resiliencia: no tiene sentido construir prompts para una seccion
            # que ya esta llena.
            db_items = list(db_sec.items.all().order_by('order'))
            if not db_items: continue
            
            # [HITO 6 BLINDAJE] Resiliencia Celery: Si el primer item ya tiene contenido, la sección está lista
            if db_items[0].content:
                for item in db_items:
                    generated_titles.append(str(item.content.get('stem', ''))[:30])
                continue
            
            # Inyección de immersion_mode y pedagogical_level ELIMINADA (Bugfix: TypeError)
            s_prompt = strategy.get_system_prompt() + NEWLINE_DIRECTIVE
            
            # Construir skeleton_json con los UUIDs reales de los ítems de esta sección
            # para que la IA los devuelva inmutables (SCHEMA-FIRST Protocol)
            section_skeleton_json = json.dumps([
                {
                    'item_id': str(item.uuid),
                    'block_type': item.block_type,
                    'widget_id': item.widget_id,
                    'task_instruction': item.metadata.get('task_instruction', '')
                }
                for item in db_items
            ], ensure_ascii=False)
            u_prompt = strategy.get_user_prompt(
                context_text=context_text, topic=topic or subject.name,
                subdivision_id=s_info['subdivision_id'],
                generated_item_titles=generated_titles,
                skeleton_json=section_skeleton_json
            )
            
            # [HITO 6] SKELETON-PROMPT BINDING: Inyectar la instrucción específica por ítem
            widgets_info_list = []
            for i, item in enumerate(db_items):
                instruction = item.metadata.get('task_instruction', 'Generar contenido académico estándar para este widget.')
                widgets_info_list.append(f"Item {item.uuid} [{item.widget_id}]: {instruction}")
            
            widgets_info = "\n".join(widgets_info_list)
            u_prompt_augmented = f"{u_prompt}\n\nINSTRUCCIONES DE LLENADO POR ÍTEM (OBLIGATORIO):\n{widgets_info}"

            # [HITO 6 BLINDAJE] Bucle de reintentos local (Atómico) para evitar consumir max_retries de Celery
            section_success = False
            local_retries = 0
            MAX_LOCAL_RETRIES = 3
            
            # [FIX LOGGING] Crear un callback de logging con contexto
            def contextual_logger(message, level="INFO"):
                context_msg = f"{message} (Examen: {str(exam.uuid)[:8]}, Sección: {s_info['subdivision_id']})"
                exam.event_log.append({"ts": timezone.now().isoformat(), "msg": context_msg, "level": level})
                exam.save(update_fields=['event_log'])

            while not section_success and local_retries < MAX_LOCAL_RETRIES:
                success, resp, key_name, usage = _safe_generate_content(
                    u_prompt_augmented,
                    system_instruction=s_prompt,
                    response_schema=strategy.get_output_schema(),
                    logger_callback=contextual_logger
                )
                
                if success:
                    try:
                        usage_total["in"] += usage.get("input_tokens", 0)
                        usage_total["out"] += usage.get("output_tokens", 0)
                        parsed_resp = _restore_newlines(
                            dirtyjson.loads(clean_json_response(resp))
                        )
                        items = parsed_resp.get("items", [])
                        
                        if "section_stimulus" in parsed_resp:
                            db_sec.section_stimulus = parsed_resp.get("section_stimulus", "")
                            db_sec.save(update_fields=["section_stimulus"])
                        
                        # [FIX] SKELETON-PROMPT BINDING: Mapeo estricto por UUID devuelto por la IA
                        db_items_map = {str(item.uuid): item for item in db_items}
                        for i_data in items:
                            ai_item_id = i_data.get('item_id')
                            db_item = db_items_map.get(str(ai_item_id))
                            
                            if db_item:
                                # [HITO 6 BLINDAJE] VALIDACIÓN ESTRICTA TRY-AND-FAIL (Deep Structure)
                                ai_content = i_data.get('content', {})
                                ai_grading = i_data.get('grading_logic', {})
                                
                                if db_item.content:
                                    deep_validate_json_structure(db_item.content, ai_content, "content")
                                if db_item.grading_logic:
                                    deep_validate_json_structure(db_item.grading_logic, ai_grading, "grading_logic")

                                db_item.content = ai_content
                                db_item.grading_logic = ai_grading
                                # [HITO 6 BLINDAJE] Preservar metadata original (TaskInstruction)
                                ai_metadata = i_data.get('metadata', {})
                                if 'task_instruction' in db_item.metadata:
                                    ai_metadata['task_instruction'] = db_item.metadata['task_instruction']
                                db_item.metadata = ai_metadata
                                # [HITO 6] AUDIO GENERATION TRIGGER (SD_LIST) / DISPARADOR DE AUDIO
                                if s_info['subdivision_id'] == 'SD_LIST':
                                    audio_text = db_sec.section_stimulus if db_sec.section_stimulus else db_item.content.get('stem', '')
                                    # [FIX 2026-07-27] 'automation_settings' vivia solo en el ambito de
                                    # _safe_generate_content, no en este: aqui era un NameError seguro.
                                    # Inalcanzable hasta ahora porque la generacion moria antes; se
                                    # habria disparado en el primer examen de idiomas con seccion SD_LIST.
                                    audio_url = _generate_item_audio(db_item.id, audio_text, AutomationSettings.load().active_api_key)
                                    if audio_url:
                                        _set_media_asset(db_item.content, audio_url, 'audio')
                                db_item.save(update_fields=["content", "grading_logic", "metadata"])
                                generated_titles.append(str(i_data.get('content', {}).get('stem', ''))[:30])

                        # [HITO 38 punto 3] INVERSION DEL FLUJO PARA ITEMS DE IMAGEN
                        # Se sustituye el contenido de los items de imagen POR
                        # SEPARADO de la llamada por lotes de arriba: primero
                        # se recupera y verifica una imagen real, y solo
                        # despues se le pide a Gemini que redacte el stem
                        # sobre esa imagen concreta. Paso aislado y con
                        # degradacion segura: si falla para un item, ese
                        # item conserva el contenido (con URL inventada) que
                        # ya escribio la llamada por lotes de arriba, y el
                        # resto de la seccion no se ve afectado. Cubre
                        # W-CLIN-SCAN (ILC-CONTEXT, salud/ciencia/tecnica) y,
                        # desde S027, W-ART-IDENT (EV-ICON-ART,
                        # SUB-HUM-ART-HIST) -- verificado contra
                        # V06DOC_WIDGETS.md y V06DOC_BLOCKS.md que el widget
                        # certificado por la UGR usa una unica obra por item.
                        WIDGETS_CON_IMAGEN_REAL = ('W-CLIN-SCAN', 'W-ART-IDENT')
                        for db_item in db_items:
                            if db_item.widget_id not in WIDGETS_CON_IMAGEN_REAL:
                                continue
                            try:
                                # [S027 - afinado tras observar convergencia
                                # entre generaciones distintas] Antes solo
                                # se usaba topic/subject.name, identico para
                                # TODOS los items del examen -- Wikimedia
                                # tiende a devolver el mismo mejor resultado
                                # para una consulta tan generica, asi que
                                # examenes distintos de la misma asignatura
                                # convergian en la misma imagen para el
                                # primer item. Se añade el titulo de la
                                # propia seccion (dato real ya disponible en
                                # db_sec, no inventado): "Anatomía
                                # Macroscópica — Nomenclatura" y "Anatomía
                                # Radiológica — Semiología" son consultas
                                # bien distintas aunque compartan asignatura.
                                base = (topic or subject.name or '').strip()
                                consulta = f"{db_sec.title} {base}".strip()
                                if not consulta:
                                    continue
                                resultado_imagen = _generate_item_image_content(
                                    consulta,
                                    AutomationSettings.load().active_api_key,
                                    task_id=None,
                                    excluir_ids=recursos_usados_examen,
                                    widget_id=db_item.widget_id,
                                )
                                if resultado_imagen is None:
                                    contextual_logger(
                                        f"H38: sin imagen verificable para item "
                                        f"{db_item.uuid} (consulta='{consulta}'); "
                                        f"conserva contenido de la llamada por lotes.",
                                        level="WARNING",
                                    )
                                    continue
                                recursos_usados_examen.add(resultado_imagen['resource_id'])
                                db_item.content['stem'] = resultado_imagen['stem']
                                _set_media_asset(db_item.content, resultado_imagen['media_url'], 'imagen')
                                db_item.content['media_attribution'] = {
                                    'text': resultado_imagen['attribution'],
                                    'license_code': resultado_imagen['license_code'],
                                    'license_url': resultado_imagen['license_url'],
                                    'source_page_url': resultado_imagen['source_page_url'],
                                }
                                db_item.grading_logic['keywords'] = resultado_imagen['keywords']
                                db_item.save(update_fields=["content", "grading_logic"])
                                contextual_logger(
                                    f"H38: item {db_item.uuid} actualizado con "
                                    f"imagen real verificada (recurso "
                                    f"{resultado_imagen['resource_id']})."
                                )
                            except Exception as img_err:
                                # Defensa en profundidad: aunque el diseño de
                                # _generate_item_image_content ya evita
                                # lanzar, cualquier fallo inesperado aqui
                                # NUNCA debe colarse en el except de la
                                # seccion (eso forzaria un reintento completo
                                # de la llamada por lotes, gastando cuota).
                                # El item conserva el contenido de la
                                # llamada por lotes.
                                contextual_logger(
                                    f"H38: excepcion inesperada procesando "
                                    f"imagen para item {db_item.uuid}: "
                                    f"{img_err}",
                                    level="ERROR",
                                )

                        section_success = True
                        time.sleep(5)
                    except Exception as parse_err:
                        local_retries += 1
                        error_msg = f"Error Parseo JSON (Intento {local_retries}/{MAX_LOCAL_RETRIES}): {parse_err}"
                        contextual_logger(error_msg, level="ERROR")
                        time.sleep(15)
                else:
                    local_retries += 1
                    error_msg = f"Fallo IA (Intento {local_retries}/{MAX_LOCAL_RETRIES}): {resp}"
                    contextual_logger(error_msg, level="ERROR")
                    time.sleep(15)
            
            # Si tras los reintentos locales falla, abortamos fatalmente el examen
            if not section_success:
                fatal_msg = f"ABORTO FATAL: La Sección no pudo generarse tras {MAX_LOCAL_RETRIES} intentos."
                contextual_logger(fatal_msg, level="CRITICAL")
                raise AIServiceCriticalError(fatal_msg)

        TrackingService.record_usage(exam.user, exam, "gemini-2.5-flash", usage_total["in"], usage_total["out"], "EXAM_GEN")
        exam.status = 'READY'
        exam.expiration_date = timezone.now() + timedelta(hours=24)
        exam.event_log.append({"ts": timezone.now().isoformat(), "msg": "Generación Completada. Caduca en 24h."})
        exam.save()

    except MaxRetriesExceededError:
        if exam:
            exam.status = 'ERROR'
            exam.error_log = "MaxRetriesExceeded: La IA falló repetidamente."
            exam.save(update_fields=['status', 'error_log'])
            
            # Notificación al Administrador (OBLIGATORIO)
            try:
                _send_admin_notification(f"FALLO CRÍTICO EXAMEN {exam.uuid}", f"El examen ha fallado tras agotar los reintentos de IA. Usuario: {exam.user.email}")
            except: pass

            # Notificación al Usuario (Incidencia 27)
            _send_exam_failure_notification(exam)
    except Exception as e:
        if isinstance(e, Retry): raise e
        if exam:
            exam.status = 'ERROR'
            exam.error_log = traceback.format_exc()
            exam.save()
            # Notificación al Usuario (Incidencia 27)
            _send_exam_failure_notification(exam)

