# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/content_automation/tasks.py
import logging
import json
import time
import re
import os
import traceback
from datetime import datetime
import pytz
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django import db
from django.db import transaction
from django.db.models import Count, Q
from django.urls import reverse
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from google.api_core.exceptions import ResourceExhausted
from django.db import IntegrityError

from .models import PendingContentTask, GeneratedContentChunk, ContentRequest
from orchestrator.models import ApiKey
from contents.models import (
    ContentMaterial,
    KnowledgeArea,
    Discipline,
    MainCategory,
    Topic,
    FreeContentMasterCategory,
    FreeContentSubCategory,
)
from academic_structure.models import Subject
from users.models import CustomUser
from core.services.gemini_service import generate_text_content, clean_json_response
from core.services.prompt_generators import (
    generate_course_metadata_prompt,
    generate_master_schema_prompt,
    generate_atomic_content_prompt,
)
from messaging.push_utils import send_notification_to_user

logger = logging.getLogger(__name__)

QUARANTINE_MAILBOX_FILE = "/home/MiguelAeTxio/SWAP/quarantine_requests.log"


def _request_quarantine_via_mailbox(api_key: ApiKey):
    try:
        with open(QUARANTINE_MAILBOX_FILE, "a") as f:
            f.write(f"{api_key.id}\n")
        logger.warning(f"BUZÓN: Solicitud de cuarentena enviada para la clave '{api_key.name}' (ID: {api_key.id}).")
    except Exception as e:
        logger.critical(f"FALLO CRÍTICO DE ARQUITECTURA: No se pudo escribir en el buzón de cuarentena '{QUARANTINE_MAILBOX_FILE}': {e}", exc_info=True)


def log_task_event(
    task_id: str, message: str, is_error: bool = False, payload: dict = None
):
    try:
        log_dir = os.path.join(settings.BASE_DIR, "logs", "content_automation")
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, f"task_{task_id}.log")
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "message": message,
            "level": "ERROR" if is_error else "INFO",
        }
        if payload:
            try:
                log_entry["payload"] = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)
            except TypeError:
                log_entry["payload"] = f"Error al serializar payload: {str(payload)}"
        log_line = f"[{log_entry['timestamp']}] [{log_entry['level']}] {log_entry['message']}"
        if "payload" in log_entry:
            log_line += f"\n--- PAYLOAD ---\n{log_entry['payload']}\n-----------------\n"
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
    except Exception as e:
        logger.error(f"Error CRÍTICO al escribir en el archivo de log para la tarea {task_id}: {e}", exc_info=True)


def _parse_master_schema(markdown_text: str) -> list:
    headings = re.findall(r"^(##+)\s(.*)", markdown_text, re.MULTILINE)
    return [(len(hashes), title.strip()) for hashes, title in headings]


def _parse_markdown_with_separator(raw_text: str) -> tuple[str, str]:
    separator = "---FUENTES---"
    if separator in raw_text:
        parts = raw_text.split(separator, 1)
        content = parts[0].strip()
        sources = parts[1].strip() if len(parts) > 1 else ""
        return content, sources
    else:
        logger.warning("El separador '---FUENTES---' no se encontró en la respuesta de la IA. Se tratará toda la respuesta como contenido.")
        return raw_text.strip(), ""


def _assemble_final_markdown_from_chunks(
    course_title: str,
    metadata: dict,
    master_schema: str,
    chunks: list[GeneratedContentChunk],
) -> str:
    classification = metadata.get("clasificacion_intelectual", {})
    yaml_header = [
        "---",
        f'titulo: "{course_title}"',
        f"descripcion_corta: \"{metadata.get('descripcion_corta', '')}\"",
        f"categoria_general: \"{classification.get('categoria_general', 'Desconocida')}\"",
        f"subcategoria: \"{classification.get('subcategoria', 'Desconocida')}\"",
        f"palabras_clave: {json.dumps(classification.get('palabras_clave', []))}",
        "---",
    ]
    parsed_schema = _parse_master_schema(master_schema)
    fuentes_title = "Fuentes y Bibliografía"
    fuentes_slug = slugify(fuentes_title)
    parsed_schema.append((2, fuentes_title))
    toc_entries = []
    for level, title in parsed_schema:
        slug = slugify(title)
        indent = "    " * (level - 2)
        toc_entries.append(f"{indent}*   [{title}](#{slug})")
    introduction = [
        f"# {course_title}",
        f"{metadata.get('descripcion_corta', 'Descripción no disponible.')}",
        '<a id="tabla-de-contenidos"></a>',
        "## Tabla de Contenidos",
        "\n".join(toc_entries),
    ]
    content_body = []
    original_parsed_schema = _parse_master_schema(master_schema)
    chunk_map = {slugify(original_parsed_schema[chunk.order - 1][1]): chunk for chunk in chunks}
    for level, title in original_parsed_schema:
        slug = slugify(title)
        chunk = chunk_map.get(slug)
        content = chunk.content if chunk else f"### Error\n\nEl contenido para la sección '{title}' no pudo ser localizado."
        heading_hashes = "#" * level
        content_body.append(f'<a id="{slug}"></a>')
        content_body.append(f"{heading_hashes} {title}")
        content_body.append(content)
        if level == 2:
            content_body.append("\n[⬆️ Volver al índice](#tabla-de-contenidos)")
    all_sources_text = [chunk.ai_sources for chunk in chunks if chunk.ai_sources]
    if all_sources_text:
        unique_references = set()
        for source_block in all_sources_text:
            for line in source_block.split('\n'):
                cleaned_line = line.strip()
                if cleaned_line:
                    unique_references.add(cleaned_line)
        sorted_references = sorted(list(unique_references))
        formatted_bibliography = "\n".join(f"- {ref}" for ref in sorted_references)
        bibliography_section = [
            f'<a id="{fuentes_slug}"></a>',
            f"## {fuentes_title}",
            formatted_bibliography,
            "\n[⬆️ Volver al índice](#tabla-de-contenidos)"
        ]
        content_body.extend(bibliography_section)
    final_parts = yaml_header + introduction + content_body
    return "\n\n".join(final_parts)


def _get_or_create_academic_topic_for_subject(subject: Subject) -> Topic:
    try:
        academic_year = subject.academic_year
        degree = academic_year.degree
        branch = degree.branch
        area, _ = KnowledgeArea.objects.get_or_create(name=branch.name, defaults={'slug': slugify(branch.name)})
        discipline, _ = Discipline.objects.get_or_create(knowledge_area=area, name=degree.name, defaults={'slug': slugify(f"{area.name}-{degree.name}")})
        main_category_name = f"{academic_year.year}º Curso"
        main_category, _ = MainCategory.objects.get_or_create(discipline=discipline, name=main_category_name, defaults={'slug': slugify(f"{discipline.name}-{main_category_name}")})
        topic, _ = Topic.objects.get_or_create(main_category=main_category, name=subject.name, defaults={'slug': slugify(f"{main_category.name}-{subject.name}")})
        return topic
    except Exception as e:
        logger.error(f"Error CRÍTICO al crear la jerarquía académica para la asignatura '{subject.name}': {e}", exc_info=True)
        return None


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
        if not first_subject:
            return
        content_request = ContentRequest.objects.filter(subject=first_subject).first()
        if not content_request:
            return
        requesters = content_request.requesters.all()
        if not requesters:
            return
        logger.info(f"Enviando notificaciones de finalización para '{new_content.title}' a {requesters.count()} usuarios.")
        content_url = new_content.get_absolute_url()
        full_url = f"https://{settings.ALLOWED_HOSTS[0]}{content_url}"
        push_title = "¡Contenido Disponible!"
        push_body = f"El material de estudio para '{new_content.title}' que solicitaste ya está disponible."
        email_subject = f"[CampuStudiOnline] El contenido para '{new_content.title}' está listo"
        email_body_text = (f"¡Hola!\n\nNos complace informarte que el material de estudio para la asignatura '{new_content.title}' que solicitaste ha sido generado y ya está disponible en la plataforma.\n\n"
                           f"Puedes acceder a él directamente a través del siguiente enlace:\n{full_url}\n\n"
                           f"Gracias por tu paciencia y por ayudarnos a mejorar CampuStudiOnline.\n\n"
                           f"Atentamente,\nEl equipo de CampuStudiOnline")
        for user in requesters:
            send_notification_to_user(user, push_title, push_body, url=content_url)
            send_mail(subject=email_subject, message=email_body_text, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[user.email], fail_silently=False)
        content_request.status = ContentRequest.StatusChoices.FULFILLED
        content_request.save(update_fields=["status"])
        logger.info(f"La solicitud de contenido para '{first_subject.name}' ha sido marcada como 'Satisfecha'.")
    except Exception as e:
        logger.error(f"Error al enviar notificaciones de finalización para el contenido {new_content.id}: {e}", exc_info=True)


class ContentGenerationError(Exception):
    pass


@shared_task(bind=True, time_limit=21600, acks_late=True, rate_limit='12/m')
def generate_full_course_task(self, task_id: str):
    db.close_old_connections()
    logger.info(f"[V20 REFACTOR] Iniciando Tarea {task_id}, Intento: {self.request.retries + 1}")
    task = None
    api_key = None
    try:
        time.sleep(10)
        from orchestrator.models import AutomationSettings
        automation_settings = AutomationSettings.load()
        api_key = automation_settings.active_api_key
        if not api_key or not api_key.is_enabled or api_key.is_quarantined:
            log_task_event(task_id, f"ESTADO DEL SISTEMA: La clave activa ('{api_key.name if api_key else 'N/A'}') no está disponible. Reintentando en 15 minutos.", is_error=True)
            raise self.retry(countdown=900)
        task = PendingContentTask.objects.select_related('subject__academic_year__degree__branch__university', 'subject__content_hash_family').get(id=task_id)
        if task.subject and task.subject.content_hash_family:
            family = task.subject.content_hash_family
            log_task_event(task_id, f"GUARDIÁN: Verificando Familia de Contenido (Hash: {family.hash[:12]}...) para la asignatura '{task.subject.name}'.")
            if family.content_material:
                existing_material = family.content_material
                log_task_event(task_id, f"GUARDIÁN: La familia ya tiene material existente (ID: {existing_material.id}). Vinculando esta asignatura y finalizando.")
                with transaction.atomic():
                    existing_material.subject.add(task.subject)
                    task_to_complete = PendingContentTask.objects.select_for_update().get(id=task_id)
                    task_to_complete.status = PendingContentTask.StatusChoices.COMPLETED
                    task_to_complete.content_material = existing_material
                    task_to_complete.notes = "Tarea completada por el Guardián de Familia. Se encontró y vinculó contenido preexistente a través de la familia."
                    task_to_complete.save(update_fields=["status", "content_material", "notes", "updated_at"])
                log_task_event(task_id, "GUARDIÁN: Vínculo asegurado y tarea marcada como completada. Ejecución finalizada.")
                return
        if not task.log_file_path:
            log_dir = os.path.join(settings.BASE_DIR, "logs", "content_automation")
            os.makedirs(log_dir, exist_ok=True)
            task.log_file_path = os.path.join(log_dir, f"task_{task_id}.log")
            task.save(update_fields=["log_file_path"])
        log_task_event(task_id, f"Usando clave de API activa: '{api_key.name}'.")
        if task.status in [PendingContentTask.StatusChoices.PENDING, PendingContentTask.StatusChoices.FAILED_RETRYABLE, PendingContentTask.StatusChoices.FAILED_QUOTA]:
            task.status = PendingContentTask.StatusChoices.PROCESSING
            task.save(update_fields=["status"])
            log_task_event(task_id, "Tarea iniciada. Estado cambiado a 'Procesando'.")
        if task.status == PendingContentTask.StatusChoices.PAUSED:
            logger.info(f"Tarea {task_id} está en PAUSA. Re-encolando para futura comprobación.")
            self.retry(countdown=600)
            return
        if not task.structured_content or "master_schema" not in task.structured_content:
            log_task_event(task_id, "Fase de Inicialización: No se encontró plan de trabajo. Generándolo ahora.")
            manual_classification = task.structured_content.get('manual_classification')
            course_title = task.course_title or (task.subject.name if task.subject else "Curso sin título")
            if task.subject:
                topic_description = task.subject.name
                degree = task.subject.academic_year.degree
                academic_context = (f"- Universidad: {degree.branch.university.name}\n- Rama: {degree.branch.name}\n- Titulación: {degree.name} ({degree.get_degree_type_display()})")
                learning_objectives = json.dumps(task.subject.learning_objectives, ensure_ascii=False) if task.subject.learning_objectives else ""
                syllabus = json.dumps(task.subject.course_content_outline, ensure_ascii=False) if task.subject.course_content_outline else ""
            else:
                topic_description = task.prompt_text
                academic_context = ""
                learning_objectives = ""
                syllabus = ""
            metadata_prompt_base = generate_course_metadata_prompt(topic_description, academic_context)
            metadata_prompt = (f"{metadata_prompt_base}\n\n" "IMPORTANTE: Devuelve la respuesta exclusivamente como un bloque de código JSON " "dentro de un bloque ```json ... ```. No incluyas ningún otro texto fuera de este bloque.")
            success, response_text, _ = generate_text_content(metadata_prompt, api_key=api_key, task_id=task_id)
            if not success:
                raise ResourceExhausted(f"Fallo crítico en inicialización al generar metdatos: {response_text}")
            cleaned_json_str = clean_json_response(response_text)
            metadata = json.loads(cleaned_json_str)
            classification_data = metadata.get("clasificacion_intelectual", {})
            if not all(classification_data.get(key) for key in ["categoria_general", "subcategoria", "palabras_clave"]):
                raise ContentGenerationError("Clasificación intelectual inválida o incompleta por parte de la IA.")
            schema_prompt = generate_master_schema_prompt(topic_description, academic_context, learning_objectives, syllabus)
            success, schema_or_error, _ = generate_text_content(schema_prompt, api_key=api_key, task_id=task_id)
            if not success:
                raise ResourceExhausted(f"Fallo crítico en inicialización al generar esquema: {schema_or_error}")
            master_schema_md = schema_or_error
            section_count = len(_parse_master_schema(master_schema_md))
            task.section_count = section_count
            new_structured_content = {"metadata": metadata, "master_schema": master_schema_md, "academic_context": academic_context}
            if manual_classification:
                new_structured_content['manual_classification'] = manual_classification
                log_task_event(task_id, "Clasificación manual del usuario preservada durante la inicialización.")
            task.structured_content = new_structured_content
            task.save(update_fields=["structured_content", "section_count"])
            log_task_event(task_id, f"Plan de trabajo generado y guardado. Secciones: {section_count}.")
        task.refresh_from_db()
        parsed_schema = _parse_master_schema(task.structured_content["master_schema"])
        for index, (_, title) in enumerate(parsed_schema):
            db.close_old_connections()
            order = index + 1
            if GeneratedContentChunk.objects.filter(task=task, order=order).exists():
                continue
            task.refresh_from_db(fields=["status"])
            if task.status == PendingContentTask.StatusChoices.PAUSED:
                log_task_event(task_id, "Tarea pausada por un administrador. Guardando progreso y saliendo.")
                self.retry(countdown=600)
                return
            academic_context = task.structured_content.get("academic_context", "")
            initial_prompt = generate_atomic_content_prompt(course_title=task.course_title or task.subject.name, section_title=title, master_schema=task.structured_content["master_schema"], academic_context=academic_context)
            log_task_event(task_id, f'Procesando sección {order}/{len(parsed_schema)}: "{title}"')
            log_task_event(task_id, "Enviando prompt atómico a la API.", payload={"prompt": initial_prompt})
            success, content_or_error, _ = generate_text_content(initial_prompt, api_key=api_key, task_id=task_id)
            if not success:
                 raise ResourceExhausted(f"Fallo en la generación de la sección: {content_or_error}")
            content_text, sources_text = _parse_markdown_with_separator(content_or_error)
            GeneratedContentChunk.objects.create(task=task, order=order, content=content_text, ai_sources=sources_text)
            log_task_event(task_id, f"Fragmento {order}/{len(parsed_schema)} guardado.")
            time.sleep(2)
        task.refresh_from_db()
        if task.content_chunks.count() == len(parsed_schema):
            log_task_event(task_id, "Ensamblaje final.")
            final_course_title = task.subject.name if task.subject else task.course_title
            final_markdown = _assemble_final_markdown_from_chunks(final_course_title, task.structured_content["metadata"], task.structured_content["master_schema"], list(task.content_chunks.all()))
            log_task_event(task_id, "Iniciando fase de clasificación de contenido.")
            manual_classification = task.structured_content.get('manual_classification')
            if task.subject:
                log_task_event(task_id, "Clasificación para contenido académico iniciada (Lógica Corregida).")
                target_topic = _get_or_create_academic_topic_for_subject(task.subject)
                if not target_topic:
                    raise ContentGenerationError(f"No se pudo crear la jerarquía académica para la asignatura {task.subject.name}")
                log_task_event(task_id, f"Clasificación jerárquica académica creada/verificada. Tema final: '{target_topic.name}'.")
                master_category, sub_category = None, None
            elif manual_classification:
                log_task_event(task_id, "Clasificación MANUAL para contenido libre iniciada.")
                master_category = FreeContentMasterCategory.objects.get(id=manual_classification['master_category_id'])
                sub_category = None
                if manual_classification.get('sub_category_id'):
                    sub_category = FreeContentSubCategory.objects.get(id=manual_classification['sub_category_id'])
                target_topic = None
            else:
                raise ContentGenerationError("Estado de tarea anómalo: Contenido libre sin clasificación manual.")
            with transaction.atomic():
                task_final = PendingContentTask.objects.select_for_update().get(id=task_id)
                is_free = task_final.subject is None
                new_content = ContentMaterial.objects.create(title=final_course_title, short_description=task_final.structured_content["metadata"].get("descripcion_corta", ""), markdown_content=final_markdown, topic=target_topic, master_category=master_category, sub_category=sub_category, creator=task_final.assigned_to, is_free_content=is_free)
                if not is_free:
                    family = task_final.subject.content_hash_family
                    if family:
                        log_task_event(task_id, f"Vinculando nuevo contenido a la Familia Hash {family.hash[:12]}...")
                        family.content_material = new_content
                        family.save(update_fields=['content_material'])
                        all_subjects_in_family = family.subjects.all()
                        count = all_subjects_in_family.count()
                        new_content.subject.add(*all_subjects_in_family)
                        log_task_event(task_id, f"VINCULACIÓN POR FAMILIA: Contenido vinculado a la familia y a sus {count} asignatura(s) miembro.")
                    else:
                        log_task_event(task_id, f"ADVERTENCIA: La asignatura '{task_final.subject.name}' no tiene familia. Vinculando solo a esta asignatura.", "WARNING")
                        new_content.subject.add(task_final.subject)
                else:
                    log_task_event(task_id, "Contenido libre creado, no se vincula a ninguna asignatura académica.")
                task_final.content_material = new_content
                task_final.status = PendingContentTask.StatusChoices.COMPLETED
                task_final.save(update_fields=["status", "content_material"])
            _send_completion_notifications(new_content)
        else:
            raise ContentGenerationError("Proceso incompleto, no se generaron todas las secciones.")
    except ResourceExhausted as e:
        if task and api_key:
            error_str = str(e)
            if "PROHIBITED_CONTENT" in error_str:
                log_task_event(task.id, "FALLO FATAL: Contenido bloqueado por la política de seguridad de la API.", is_error=True, payload={"api_key": api_key.name, "error": error_str})
                task.status = PendingContentTask.StatusChoices.FAILED_FATAL
                task.last_error = traceback.format_exc()
                task.notes = ("La generación fue bloqueada por la API de Gemini debido a 'PROHIBITED_CONTENT'. " "Esto es un fallo irrecuperable y requiere intervención manual para analizar el prompt.")
                task.save(update_fields=["status", "last_error", "notes"])
                from orchestrator.tasks import _send_admin_notification
                _send_admin_notification("Tarea Fallida por Contenido Prohibido", f"La tarea para '{task}' ha fallado permanentemente debido a contenido prohibido.")
                return
            max_retries = 2
            if self.request.retries >= max_retries:
                log_task_event(task.id, f"Máximo de reintentos ({self.request.retries + 1}) alcanzado por error de cuota. Solicitando cuarentena vía buzón.", is_error=True)
                _request_quarantine_via_mailbox(api_key)
                task.status = PendingContentTask.StatusChoices.FAILED_QUOTA
                task.last_error = f"Clave '{api_key.name}' solicitada para cuarentena tras {self.request.retries + 1} fallos. El bucle principal se encargará de rotar y re-encolar.\n{traceback.format_exc()}"
                task.save(update_fields=["status", "last_error"])
            else:
                log_task_event(task.id, f"Error de cuota API (Intento {self.request.retries + 1}/{max_retries + 1}).", is_error=True, payload={"api_key": api_key.name, "error": error_str})
                raise self.retry(exc=e, countdown=60, max_retries=max_retries)
    except Exception as e:
        if task:
            error_traceback = traceback.format_exc()
            logger.critical(f"TRACEBACK CAPTURADO PARA TAREA {task.id}:\n{error_traceback}")
            log_task_event(task.id, f"Error en la tarea: {str(e)}", is_error=True)
            try:
                task.status = PendingContentTask.StatusChoices.FAILED_RETRYABLE
                task.last_error = error_traceback
                task.save(update_fields=["status", "last_error"])
                self.retry(exc=e)
            except self.MaxRetriesExceededError:
                logger.critical(f"Máximo de reintentos alcanzado para la tarea {task.id}. Marcando como FATAL.")
                task.status = PendingContentTask.StatusChoices.FAILED_FATAL
                task.notes = f"Falló permanentemente. Error final: {str(e)}"
                task.last_error = error_traceback
                task.save(update_fields=["status", "notes", "last_error"])
                from orchestrator.tasks import _send_admin_notification
                _send_admin_notification("Tarea Fallida Permanentemente", f"La tarea para '{task}' ha fallado tras múltiples reintentos.")
        else:
            logger.critical(f"Error irrecuperable en tarea con ID {task_id} donde 'task' es None: {e}", exc_info=True)
    finally:
        db.close_old_connections()
