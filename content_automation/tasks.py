# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/content_automation/tasks.py
import logging
import json
import time
import re
import os
import traceback
from datetime import datetime, timedelta
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

from .models import PendingContentTask, GeneratedContentChunk, ContentRequest, AutomationSettings, ApiKey, FreeContentRequest
from contents.models import (
    ContentMaterial,
    KnowledgeArea,
    Discipline,
    MainCategory,
    Topic,
    FreeContentMasterCategory,
    FreeContentSubCategory,
)
from academic_structure.models import Subject, Degree, Branch
from users.models import CustomUser
# [REFACTORIZADO V6] El servicio de texto ahora requiere la clave como parámetro.
from core.services.gemini_service import generate_text_content, clean_json_response
from core.services.prompt_generators import (
    generate_course_metadata_prompt,
    generate_master_schema_prompt,
    generate_atomic_content_prompt,
)
from messaging.push_utils import send_notification_to_user

logger = logging.getLogger(__name__)

# ==============================================================================
# HELPERS
# ==============================================================================

def _check_and_perform_daily_reset():
    """
    [REFACTORIZADO V2] Lógica de reseteo de cuarentena integrada en el bucle principal.
    Se ejecuta una vez al día después de la hora configurada, usando una "banderita"
    de fecha y corrigiendo la zona horaria.
    """
    try:
        automation_settings = AutomationSettings.load()
        
        # OBTENER HORA LOCAL DE MADRID
        madrid_tz = pytz.timezone('Europe/Madrid')
        now_madrid = timezone.now().astimezone(madrid_tz)
        today = now_madrid.date()
        
        # Condición 1: Comprobar si ya se ha ejecutado el reseteo hoy.
        if automation_settings.last_quarantine_reset_date >= today:
            return

        # Condición 2: Si no se ha ejecutado hoy, comprobar si ya es la hora en Madrid.
        now_time = now_madrid.time()
        if now_time >= automation_settings.quarantine_reset_time:
            keys_to_reset = ApiKey.objects.filter(is_quarantined=True)
            count = keys_to_reset.count()
            
            if count > 0:
                keys_to_reset.update(is_quarantined=False)
                message = f"Se han liberado {count} claves API de la cuarentena."
                _log_structured_event(f"RESET DIARIO (INTEGRADO): {message}", "INFO")
                _send_admin_notification("Reseteo Diario de Claves API", message)

            # Actualizar la "banderita" para que no se vuelva a ejecutar hoy.
            automation_settings.last_quarantine_reset_date = today
            automation_settings.save(update_fields=["last_quarantine_reset_date"])

    except Exception as e:
        # Este es un punto crítico, si falla, debe ser logueado de forma muy visible.
        _log_structured_event(f"Error CRÍTICO en la lógica de reseteo diario integrado: {e}", "CRITICAL", {"traceback": traceback.format_exc()})
        logger.critical(f"Error CRÍTICO en _check_and_perform_daily_reset: {e}", exc_info=True)


def _log_structured_event(message: str, level: str = "INFO", details: dict = None):
    """
    [NUEVO] Escribe un evento estructurado en el JSONField de AutomationSettings.
    """
    try:
        settings = AutomationSettings.load()
        log_entry = {
            "timestamp": timezone.now().isoformat(),
            "level": level,
            "message": message,
            "details": details or {}
        }
        # Prepend to the list to show newest first
        settings.event_log.insert(0, log_entry)
        # Trim the log to keep it from growing indefinitely
        settings.event_log = settings.event_log[:100]
        settings.save(update_fields=['event_log'])
    except Exception as e:
        logger.error(f"CRITICAL: No se pudo escribir en el event_log estructurado: {e}", exc_info=True)


def _rotate_to_next_active_key(quarantined_key):
    """
    [V3] Pone en cuarentena la clave activa y rota a la siguiente disponible en la secuencia.
    Actualiza el estado global en AutomationSettings.
    """
    automation_settings = AutomationSettings.load()
    
    # 1. Poner la clave fallida en cuarentena
    quarantined_key.is_quarantined = True
    quarantined_key.save(update_fields=['is_quarantined'])
    _log_structured_event(
        f"CUARENTENA: Clave '{quarantined_key.name}' puesta en cuarentena tras fallos persistentes.",
        "WARNING",
        {"api_key_id": quarantined_key.id}
    )
    _send_admin_notification("Clave API en Cuarentena", f"La clave '{quarantined_key.name}' ha sido puesta en cuarentena.")

    # 2. Buscar la siguiente clave en la secuencia que no esté en cuarentena
    next_key = ApiKey.objects.filter(
        is_enabled=True,
        is_quarantined=False,
        id__gt=quarantined_key.id
    ).order_by('id').first()

    # 3. Si no hay una después, buscar desde el principio (ciclo)
    if not next_key:
        next_key = ApiKey.objects.filter(
            is_enabled=True,
            is_quarantined=False
        ).order_by('id').first()

    # 4. Actualizar el estado global
    automation_settings.active_api_key = next_key
    automation_settings.save(update_fields=['active_api_key'])
    
    if next_key:
        _log_structured_event(
            f"ROTACIÓN EXITOSA: La nueva clave activa es '{next_key.name}'.",
            "INFO",
            {"new_api_key_id": next_key.id}
        )
    else:
        _log_structured_event(
            "POOL AGOTADO: Todas las claves de API están en cuarentena. El sistema se detendrá.",
            "CRITICAL"
        )
        _send_admin_notification("¡ALERTA CRÍTICA! POOL DE API KEYS AGOTADO", "Todas las claves están en cuarentena. La generación de contenido está detenida hasta el reseteo diario.")


def log_task_event(
    task_id: str, message: str, is_error: bool = False, payload: dict = None
):
    """
    [V2] Escribe un evento de log en un archivo de texto dedicado para la tarea.
    Esta función está desacoplada de la base de datos para máxima velocidad y resiliencia.
    """
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
                # Usamos sort_keys=True para un orden consistente en los logs
                log_entry["payload"] = json.dumps(
                    payload, indent=2, ensure_ascii=False, sort_keys=True
                )
            except TypeError:
                log_entry["payload"] = f"Error al serializar payload: {str(payload)}"

        # Convertir el diccionario a una cadena de texto formateada para el log
        log_line = (
            f"[{log_entry['timestamp']}] [{log_entry['level']}] {log_entry['message']}"
        )
        if "payload" in log_entry:
            log_line += f"\n--- PAYLOAD ---\n{log_entry['payload']}\n-----------------\n"

        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")

    except Exception as e:
        # Si la escritura del log falla, lo registramos en el logger principal
        # para no detener la tarea por un fallo en el logging.
        logger.error(
            f"Error CRÍTICO al escribir en el archivo de log para la tarea {task_id}: {e}",
            exc_info=True,
        )


def _parse_master_schema(markdown_text: str) -> list:
    headings = re.findall(r"^(##+)\s(.*)", markdown_text, re.MULTILINE)
    return [(len(hashes), title.strip()) for hashes, title in headings]


def _parse_markdown_with_separator(raw_text: str) -> tuple[str, str]:
    """
    [ROBUSTNESS V6] Parsea la respuesta Markdown de la IA usando un separador explícito.
    Devuelve una tupla (content, sources). Maneja el caso de que el separador no exista.
    """
    separator = "---FUENTES---"
    if separator in raw_text:
        parts = raw_text.split(separator, 1)
        content = parts[0].strip()
        sources = parts[1].strip() if len(parts) > 1 else ""
        return content, sources
    else:
        # Si la IA no incluye el separador, asumimos que toda la respuesta es contenido.
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
    chunk_map = {
        slugify(original_parsed_schema[chunk.order - 1][1]): chunk for chunk in chunks
    }

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


def _get_predictive_topic_from_prompt(prompt_text: str) -> Topic | None:
    """
    [NUEVO] Intenta clasificar el contenido de forma predeterminada basándose en
    palabras clave en el prompt inicial para garantizar una jerarquía consistente.
    """
    if not prompt_text:
        return None

    prompt_lower = prompt_text.lower()
    area_name = "Contenidos en CampuStudiOnline"
    area, _ = KnowledgeArea.objects.get_or_create(name=area_name)
    
    # Regla 1: Historia de la Música
    if "historia de la música" in prompt_lower or "pink floyd" in prompt_lower:
        disciplina_name = "Artes y Humanidades"
        categoria_name = "Música"
        tema_name = "Historia de la Música"
        
        disciplina, _ = Discipline.objects.get_or_create(knowledge_area=area, name=disciplina_name)
        categoria, _ = MainCategory.objects.get_or_create(discipline=disciplina, name=categoria_name)
        tema, _ = Topic.objects.get_or_create(main_category=categoria, name=tema_name)
        return tema

    # Regla 2: Biografías
    if "biografía" in prompt_lower:
        disciplina_name = "Artes y Humanidades"
        categoria_name = "Historia"
        tema_name = "Biografías"
        
        disciplina, _ = Discipline.objects.get_or_create(knowledge_area=area, name=disciplina_name)
        categoria, _ = MainCategory.objects.get_or_create(discipline=disciplina, name=categoria_name)
        tema, _ = Topic.objects.get_or_create(main_category=categoria, name=tema_name)
        return tema

    # Regla 3: Formación Profesional
    if "formación profesional" in prompt_lower:
        disciplina_name = "Artes y Humanidades"
        categoria_name = "Desarrollo Personal"
        tema_name = "Formación Profesional"
        
        disciplina, _ = Discipline.objects.get_or_create(knowledge_area=area, name=disciplina_name)
        categoria, _ = MainCategory.objects.get_or_create(discipline=disciplina, name=categoria_name)
        tema, _ = Topic.objects.get_or_create(main_category=categoria, name=tema_name)
        return tema
        
    return None


def _get_or_create_topic_from_classification(classification_data: dict) -> Topic | None:
    try:
        area_name = "Contenidos en CampuStudiOnline"
        disciplina_name = classification_data.get("categoria_general")
        categoria_name = classification_data.get("subcategoria")
        palabras_clave = classification_data.get("palabras_clave", [])

        # [LÓGICA MEJORADA V2]
        # Se prioriza la búsqueda de palabras clave especiales sobre la subcategoría.
        special_keywords = ["Biografía", "Historia de la Música", "Formación Profesional"]
        tema_name = None
        
        # 1. Buscar coincidencia en palabras clave.
        for keyword in palabras_clave:
            if keyword in special_keywords:
                tema_name = keyword
                break
        
        # 2. Si no se encontró, usar la lógica por defecto.
        if not tema_name:
            tema_name = palabras_clave[0] if palabras_clave else categoria_name

        if not all([disciplina_name, categoria_name, tema_name]):
            logger.warning(
                f"Datos de clasificación intelectual incompletos: {classification_data}"
            )
            return None

        area, _ = KnowledgeArea.objects.get_or_create(name=area_name)
        disciplina, _ = Discipline.objects.get_or_create(
            knowledge_area=area, name=disciplina_name
        )
        categoria, _ = MainCategory.objects.get_or_create(
            discipline=disciplina, name=categoria_name
        )
        tema, _ = Topic.objects.get_or_create(
            main_category=categoria, name=tema_name, defaults={"parent": None}
        )
        return tema
    except Exception as e:
        logger.error(f"Error al procesar la jerarquía intelectual: {e}", exc_info=True)
        return None


def _get_or_create_free_categories_from_classification(
    classification_data: dict, course_title: str
) -> tuple:
    """
    [NUEVO] Obtiene o crea las categorías de contenido libre basándose en la clasificación de la IA.
    """
    master_name = classification_data.get("categoria_general")
    sub_name = classification_data.get("subcategoria")

    if not master_name:
        logger.warning(
            f"No se encontró 'categoria_general' en la clasificación para '{course_title}'. No se puede clasificar."
        )
        return None, None

    master_category, _ = FreeContentMasterCategory.objects.get_or_create(name=master_name)
    sub_category = None
    if sub_name:
        sub_category, _ = FreeContentSubCategory.objects.get_or_create(
            master_category=master_category, name=sub_name
        )
    return master_category, sub_category


def _send_completion_notifications(new_content: ContentMaterial):
    try:
        # Dado que ahora es una M2M, buscamos la primera asignatura para encontrar la solicitud
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
        email_body_text = (
            f"¡Hola!\n\nNos complace informarte que el material de estudio para la asignatura "
            f"'{new_content.title}' que solicitaste ha sido generado y ya está disponible en la plataforma.\n\n"
            f"Puedes acceder a él directamente a través del siguiente enlace:\n{full_url}\n\n"
            f"Gracias por tu paciencia y por ayudarnos a mejorar CampuStudiOnline.\n\n"
            f"Atentamente,\nEl equipo de CampuStudiOnline"
        )

        for user in requesters:
            send_notification_to_user(user, push_title, push_body, url=content_url)
            
            send_mail(
                subject=email_subject,
                message=email_body_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

        content_request.status = ContentRequest.StatusChoices.FULFILLED
        content_request.save(update_fields=["status"])
        logger.info(f"La solicitud de contenido para '{first_subject.name}' ha sido marcada como 'Satisfecha'.")

    except Exception as e:
        logger.error(f"Error al enviar notificaciones de finalización para el contenido {new_content.id}: {e}", exc_info=True)


def _send_admin_notification(title, body):
    """[NUEVO] Envía notificación push y email a todos los superusuarios activos."""
    try:
        admins = CustomUser.objects.filter(is_superuser=True, is_active=True)
        if not admins.exists():
            logger.warning("No se encontraron administradores activos para notificar.")
            return

        dashboard_url = reverse("content_automation:automation_control_center")
        
        # Notificación Push
        for admin in admins:
            send_notification_to_user(admin, title, body, url=dashboard_url)
        
        # Email
        email_subject = f"[CampuStudiOnline Automation] {title}"
        recipient_list = [admin.email for admin in admins]
        send_mail(
            subject=email_subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=True,
        )
        logger.info(f"Notificación de administrador enviada a {len(recipient_list)} admin(s): '{title}'")

    except Exception as e:
        logger.error(f"Error al enviar notificación de administrador: {e}", exc_info=True)


def _get_next_subject_queryset(settings):
    base_queryset = Subject.objects.filter(content_materials__isnull=True)
    
    # Excluimos asignaturas cuyos NOMBRES ya tienen una tarea activa.
    active_task_subject_names = PendingContentTask.objects.exclude(
        status__in=[
            PendingContentTask.StatusChoices.COMPLETED,
            PendingContentTask.StatusChoices.FAILED_FATAL
        ]
    ).values_list('subject__name', flat=True).distinct()

    query = base_queryset.exclude(name__in=active_task_subject_names)

    if settings.seed_branch:
        query = query.filter(academic_year__degree__branch=settings.seed_branch)
    if settings.seed_degree:
        query = query.filter(academic_year__degree=settings.seed_degree)
    if settings.seed_year:
        try:
            year_map = {"Primero": 1, "Segundo": 2, "Tercero": 3, "Cuarto": 4, "Quinto": 5}
            year_int = year_map.get(settings.seed_year)
            if year_int:
                query = query.filter(academic_year__year=year_int)
        except (ValueError, TypeError):
            pass
            
    return query


def _advance_seed_filters_if_needed(automation_settings):
    """
    [NON-STOP LOGIC V2] Comprueba si el lote actual está agotado, avanza al siguiente,
    y devuelve True si se ha modificado algún filtro, False en caso contrario.
    """
    if not any([automation_settings.seed_branch, automation_settings.seed_degree, automation_settings.seed_year]):
        return False

    remaining_subjects = _get_next_subject_queryset(automation_settings).exists()

    if not remaining_subjects:
        notification_title = "Lote de Generación Completado"
        message = ""
        
        if automation_settings.seed_year:
            message = f"Lote para '{automation_settings.seed_year}' del grado '{automation_settings.seed_degree.name}' completado. Se elimina filtro de año y se continúa."
            automation_settings.seed_year = ""
            automation_settings.save(update_fields=['seed_year'])
            _log_structured_event(message)
            _send_admin_notification(notification_title, message)
            return True

        if automation_settings.seed_degree:
            message = f"Lote para el grado '{automation_settings.seed_degree.name}' completado. Se elimina filtro de grado y se continúa."
            automation_settings.seed_degree = None
            automation_settings.save(update_fields=['seed_degree'])
            _log_structured_event(message)
            _send_admin_notification(notification_title, message)
            return True
            
        if automation_settings.seed_branch:
            message = f"Lote para la rama '{automation_settings.seed_branch.name}' completado. Se elimina filtro de rama y se continúa."
            automation_settings.seed_branch = None
            automation_settings.save(update_fields=['seed_branch'])
            _log_structured_event(message)
            _send_admin_notification(notification_title, message)
            return True
    
    return False


class ContentGenerationError(Exception):
    """Excepción personalizada para abortar la forma controlada por fallos no recuperables."""
    pass


@shared_task(bind=True, time_limit=21600, acks_late=True, rate_limit='12/m')
def generate_full_course_task(self, task_id: str):
    db.close_old_connections()
    logger.info(f"[V20 REFACTOR] Iniciando Tarea {task_id}, Intento: {self.request.retries + 1}")
    
    task = None
    api_key = None
    predictive_topic = None # Inicializar para evitar UnboundLocalError
    try:
        time.sleep(10)
        
        automation_settings = AutomationSettings.load()
        api_key = automation_settings.active_api_key

        if not api_key or not api_key.is_enabled or api_key.is_quarantined:
            log_task_event(task_id, f"ESTADO DEL SISTEMA: La clave activa ('{api_key.name if api_key else 'N/A'}') no está disponible. Reintentando en 15 minutos.", is_error=True)
            raise self.retry(countdown=900)

        task = PendingContentTask.objects.select_related(
            'subject__academic_year__degree__branch', 'subject__content_hash_family'
        ).get(id=task_id)

        # ======================================================================
        # GUARDIÁN DE FAMILIA DE CONTENIDO [REFACTORIZADO]: Previene la generación de contenido duplicado.
        # ======================================================================
        if task.subject and task.subject.content_hash_family:
            family = task.subject.content_hash_family
            log_task_event(task_id, f"GUARDIÁN: Verificando Familia de Contenido (Hash: {family.hash[:12]}...) para la asignatura '{task.subject.name}'.")

            if family.content_material:
                existing_material = family.content_material
                log_task_event(task_id, f"GUARDIÁN: La familia ya tiene material existente (ID: {existing_material.id}). Vinculando esta asignatura y finalizando.")
                with transaction.atomic():
                    # Asegura que esta asignatura está vinculada al material
                    existing_material.subject.add(task.subject)
                    
                    task_to_complete = PendingContentTask.objects.select_for_update().get(id=task_id)
                    task_to_complete.status = PendingContentTask.StatusChoices.COMPLETED
                    task_to_complete.content_material = existing_material
                    task_to_complete.notes = "Tarea completada por el Guardián de Familia. Se encontró y vinculó contenido preexistente a través de la familia."
                    task_to_complete.save(update_fields=["status", "content_material", "notes", "updated_at"])
                
                log_task_event(task_id, "GUARDIÁN: Vínculo asegurado y tarea marcada como completada. Ejecución finalizada.")
                return
        # ======================================================================

        if not task.log_file_path:
            log_dir = os.path.join(settings.BASE_DIR, "logs", "content_automation")
            os.makedirs(log_dir, exist_ok=True)
            task.log_file_path = os.path.join(log_dir, f"task_{task_id}.log")
            task.save(update_fields=["log_file_path"])

        log_task_event(task_id, f"Usando clave de API activa: '{api_key.name}'.")

        if task.status in [
            PendingContentTask.StatusChoices.PENDING,
            PendingContentTask.StatusChoices.FAILED_RETRYABLE,
            PendingContentTask.StatusChoices.FAILED_QUOTA,
        ]:
            task.status = PendingContentTask.StatusChoices.PROCESSING
            task.save(update_fields=["status"])
            log_task_event(task_id, "Tarea iniciada. Estado cambiado a 'Procesando'.")

        if task.status == PendingContentTask.StatusChoices.PAUSED:
            logger.info(f"Tarea {task_id} está en PAUSA. Re-encolando para futura comprobación.")
            self.retry(countdown=600)
            return

        if not task.structured_content or "master_schema" not in task.structured_content:
            log_task_event(task_id, "Fase de Inicialización: No se encontró plan de trabajo. Generándolo ahora.")
            
            # [FIX] Preservar la clasificación manual si ya existe
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
            metadata_prompt = (
                f"{metadata_prompt_base}\n\n"
                "IMPORTANTE: Devuelve la respuesta exclusivamente como un bloque de código JSON "
                "dentro de un bloque ```json ... ```. No incluyas ningún otro texto fuera de este bloque."
            )
            
            # [REFACTORIZADO V6] Se pasa la api_key explícitamente al servicio.
            success, response_text, _ = generate_text_content(metadata_prompt, api_key=api_key, task_id=task_id)

            if not success:
                raise ResourceExhausted(f"Fallo crítico en inicialización al generar metdatos: {response_text}")
            
            cleaned_json_str = clean_json_response(response_text)
            metadata = json.loads(cleaned_json_str)

            classification_data = metadata.get("clasificacion_intelectual", {})
            if not all(classification_data.get(key) for key in ["categoria_general", "subcategoria", "palabras_clave"]):
                raise ContentGenerationError("Clasificación intelectual inválida o incompleta por parte de la IA.")
            
            schema_prompt = generate_master_schema_prompt(topic_description, academic_context, learning_objectives, syllabus)
            # [REFACTORIZADO V6] Se pasa la api_key explícitamente al servicio.
            success, schema_or_error, _ = generate_text_content(schema_prompt, api_key=api_key, task_id=task_id)
            
            if not success:
                raise ResourceExhausted(f"Fallo crítico en inicialización al generar esquema: {schema_or_error}")
            
            master_schema_md = schema_or_error
            
            section_count = len(_parse_master_schema(master_schema_md))
            task.section_count = section_count
            
            # [FIX] Construir el nuevo diccionario y re-inyectar la clasificación manual
            new_structured_content = {
                "metadata": metadata,
                "master_schema": master_schema_md,
                "academic_context": academic_context,
            }
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
            initial_prompt = generate_atomic_content_prompt(
                course_title=task.course_title or task.subject.name,
                section_title=title,
                master_schema=task.structured_content["master_schema"],
                academic_context=academic_context,
            )
            log_task_event(task_id, f'Procesando sección {order}/{len(parsed_schema)}: "{title}"')
            log_task_event(task_id, "Enviando prompt atómico a la API.", payload={"prompt": initial_prompt})
            
            # [REFACTORIZADO V6] Se pasa la api_key explícitamente al servicio.
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
            
            # [REFACTORIZADO] Lógica de clasificación bifurcada
            manual_classification = task.structured_content.get('manual_classification')

            if task.subject:
                # Ruta 1: Contenido Académico (siempre automático)
                log_task_event(task_id, "Clasificación AUTOMÁTICA para contenido académico iniciada.")
                predictive_topic = _get_predictive_topic_from_prompt(task.subject.name)
                if predictive_topic:
                    target_topic = predictive_topic
                    log_task_event(task_id, f"Clasificación PREDICTIVA aplicada. Tema: '{predictive_topic.name}'.")
                else:
                    target_topic = _get_or_create_topic_from_classification(
                        task.structured_content["metadata"].get("clasificacion_intelectual", {})
                    )
                    log_task_event(task_id, "Clasificación por IA (fallback) aplicada.")
                master_category, sub_category = None, None
            
            elif manual_classification:
                # Ruta 2: Contenido Libre con clasificación MANUAL
                log_task_event(task_id, "Clasificación MANUAL para contenido libre iniciada.")
                master_category = FreeContentMasterCategory.objects.get(id=manual_classification['master_category_id'])
                sub_category = None
                if manual_classification.get('sub_category_id'):
                    sub_category = FreeContentSubCategory.objects.get(id=manual_classification['sub_category_id'])
                target_topic = None
            
            else:
                # Ruta 3: Contenido Libre con clasificación AUTOMÁTICA (fallback)
                log_task_event(task_id, "Clasificación AUTOMÁTICA para contenido libre iniciada (fallback).")
                master_category, sub_category = _get_or_create_free_categories_from_classification(
                    task.structured_content["metadata"].get("clasificacion_intelectual", {}),
                    final_course_title,
                )
                target_topic = None
            
            with transaction.atomic():
                task_final = PendingContentTask.objects.select_for_update().get(id=task_id)
                
                is_free = task_final.subject is None

                new_content = ContentMaterial.objects.create(
                    title=final_course_title,
                    short_description=task_final.structured_content["metadata"].get("descripcion_corta", ""),
                    markdown_content=final_markdown,
                    topic=target_topic,
                    master_category=master_category,
                    sub_category=sub_category,
                    creator=task_final.assigned_to,
                    is_free_content=is_free
                )
                
                if not is_free:
                    family = task_final.subject.content_hash_family
                    if family:
                        # ==================================================================
                        # VINCULACIÓN POR FAMILIA [REFACTORIZADO]: Asigna el nuevo contenido
                        # a la familia y a todas las asignaturas que la componen.
                        # ==================================================================
                        log_task_event(task_id, f"Vinculando nuevo contenido a la Familia Hash {family.hash[:12]}...")

                        # 1. Asignar el material como el canónico de la familia
                        family.content_material = new_content
                        family.save(update_fields=['content_material'])

                        # 2. Vincular el material con TODAS las asignaturas de la familia
                        all_subjects_in_family = family.subjects.all()
                        count = all_subjects_in_family.count()
                        new_content.subject.add(*all_subjects_in_family)
                        
                        log_task_event(task_id, f"VINCULACIÓN POR FAMILIA: Contenido vinculado a la familia y a sus {count} asignatura(s) miembro.")
                        # ==================================================================
                    else:
                        # Fallback por si la asignatura no tiene familia (no debería pasar)
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
                log_task_event(
                    task.id,
                    "FALLO FATAL: Contenido bloqueado por la política de seguridad de la API.",
                    is_error=True,
                    payload={"api_key": api_key.name, "error": error_str},
                )
                task.status = PendingContentTask.StatusChoices.FAILED_FATAL
                task.last_error = traceback.format_exc()
                task.notes = (
                    "La generación fue bloqueada por la API de Gemini debido a 'PROHIBITED_CONTENT'. "
                    "Esto es un fallo irrecuperable y requiere intervención manual para analizar el prompt."
                )
                task.save(update_fields=["status", "last_error", "notes"])
                _send_admin_notification(
                    "Tarea Fallida por Contenido Prohibido",
                    f"La tarea para '{task}' ha fallado permanentemente debido a contenido prohibido."
                )
                return

            log_task_event(task.id, f"Error de cuota API (Intento {self.request.retries + 1}/3).", is_error=True, payload={"api_key": api_key.name, "error": error_str})
            try:
                raise self.retry(exc=e, countdown=60, max_retries=2)
            except MaxRetriesExceededError:
                log_task_event(task.id, f"Máximo de reintentos por error de cuota. Rotando clave.", is_error=True)
                _rotate_to_next_active_key(api_key)
                task.status = PendingContentTask.StatusChoices.FAILED_QUOTA
                task.last_error = f"Clave '{api_key.name}' en cuarentena tras 3 fallos.\n{traceback.format_exc()}"
                task.save(update_fields=["status", "last_error"])

    except Exception as e:
        if task:
            error_traceback = traceback.format_exc()
            # [INYECCIÓN DE DIAGNÓSTICO] Forzamos el log del traceback completo al logger principal.
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
                _send_admin_notification("Tarea Fallida Permanentemente", f"La tarea para '{task}' ha fallado tras múltiples reintentos.")
        else:
            logger.critical(f"Error irrecuperable en tarea con ID {task_id} donde 'task' es None: {e}", exc_info=True)
    finally:
        db.close_old_connections()


@shared_task(bind=True)
def automation_main_loop_task(self):
    """
    [REFACTORIZADO V8] Bucle principal con auto-sincronización de clave activa e hibernación.
    """
    try:
        _check_and_perform_daily_reset()
        db.close_old_connections()
        automation_settings = AutomationSettings.load()

        if not automation_settings.is_running:
            status_msg = "DETENIDO: Interruptor maestro desactivado."
            if automation_settings.last_run_status != status_msg:
                _log_structured_event(status_msg, "INFO")
                automation_settings.last_run_status = status_msg
                automation_settings.save(update_fields=['last_run_status'])
            return

        # --- LÓGICA DE AUTO-SINCRONIZACIÓN Y ESTADO DE CLAVES ---
        active_key = automation_settings.active_api_key
        if not active_key or not active_key.is_enabled or active_key.is_quarantined:
            _log_structured_event(
                f"SINCRO: Clave activa ('{active_key.name if active_key else 'N/A'}') no es válida. Buscando reemplazo.", "INFO"
            )
            next_available_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).order_by('id').first()
            
            if next_available_key:
                automation_settings.active_api_key = next_available_key
                automation_settings.save(update_fields=['active_api_key'])
                _log_structured_event(
                    f"SINCRO EXITOSA: Nueva clave activa es '{next_available_key.name}'.", "INFO", {"new_api_key_id": next_available_key.id}
                )
            else:
                madrid_tz = pytz.timezone('Europe/Madrid')
                now_madrid = timezone.now().astimezone(madrid_tz)
                reset_time = automation_settings.quarantine_reset_time
                tomorrow = now_madrid.date() + timedelta(days=1)
                next_run_datetime_naive = datetime.combine(tomorrow, reset_time)
                next_run_datetime_aware = madrid_tz.localize(next_run_datetime_naive)
                status_msg = f"HIBERNANDO (POOL AGOTADO): No hay claves disponibles. Próxima ejecución: {next_run_datetime_aware.strftime('%Y-%m-%d %H:%M:%S %Z')}."
                if automation_settings.last_run_status != status_msg:
                    _log_structured_event(status_msg, "WARNING")
                    automation_settings.last_run_status = status_msg
                    automation_settings.save(update_fields=['last_run_status'])
                self.retry(eta=next_run_datetime_aware, max_retries=None)
                return
        
        # --- LÓGICA DE RESCATE Y BÚSQUEDA DE TRABAJO ---
        automation_settings.refresh_from_db()

        zombie_threshold = timezone.now() - timedelta(minutes=5)
        zombie_tasks = PendingContentTask.objects.filter(
            status__in=[PendingContentTask.StatusChoices.PROCESSING, PendingContentTask.StatusChoices.PENDING],
            updated_at__lt=zombie_threshold
        )
        for task in zombie_tasks:
            message = f"VIGILANTE: Tarea '{task.id}' detectada como ZOMBIE. Marcada para rescate."
            _log_structured_event(message, "WARNING", {"task_id": str(task.id)})
            task.status = PendingContentTask.StatusChoices.FAILED_RETRYABLE
            task.save(update_fields=["status"])

        task_to_rescue = PendingContentTask.objects.filter(
            status__in=[
                PendingContentTask.StatusChoices.FAILED_RETRYABLE,
                PendingContentTask.StatusChoices.FAILED_QUOTA,
            ]
        ).order_by('updated_at').first()

        if task_to_rescue:
            _log_structured_event(f"RESCATE INICIADO: Re-encolando la tarea {task_to_rescue.id}.")
            task_to_rescue.status = PendingContentTask.StatusChoices.PENDING
            task_to_rescue.save(update_fields=["status"])
            generate_full_course_task.delay(str(task_to_rescue.id))
            status_msg = f"AUTO-RECUPERACIÓN: Tarea para '{task_to_rescue}' re-encolada."
            automation_settings.last_run_status = status_msg
            automation_settings.last_run_timestamp = timezone.now()
            automation_settings.save(update_fields=['last_run_status', 'last_run_timestamp'])
            return

        if PendingContentTask.objects.filter(status__in=[PendingContentTask.StatusChoices.PROCESSING, PendingContentTask.StatusChoices.PENDING]).exists():
            status_msg = "EN ESPERA: Hay una tarea en proceso o pendiente de ser procesada."
            if automation_settings.last_run_status != status_msg:
                _log_structured_event(status_msg, "INFO")
                automation_settings.last_run_status = status_msg
                automation_settings.save(update_fields=['last_run_status'])
            return

        while True:
            subject_to_process = None
            approved_request = ContentRequest.objects.filter(status=ContentRequest.StatusChoices.APPROVED).order_by('updated_at').first()
            if approved_request and approved_request.subject.content_materials.count() == 0:
                subject_to_process = approved_request.subject
                origin = PendingContentTask.TaskOrigin.APPROVED_REQUEST
                with transaction.atomic():
                    req = ContentRequest.objects.select_for_update().get(id=approved_request.id)
                    req.status = ContentRequest.StatusChoices.IN_PROGRESS
                    req.save(update_fields=["status"])
                _log_structured_event(f"PRIORIDAD: Reclamada la solicitud para '{subject_to_process.name}'.")
            
            if not subject_to_process:
                subject_qs = _get_next_subject_queryset(automation_settings)
                subject_to_process = subject_qs.order_by('?').first()
                if subject_to_process:
                    origin = PendingContentTask.TaskOrigin.MASS_GENERATION

            if subject_to_process:
                admin_user = CustomUser.objects.filter(is_superuser=True, is_active=True).order_by('pk').first()
                if not admin_user:
                    _log_structured_event("CRÍTICO: No se encontró un superusuario para asignar la tarea.", "CRITICAL")
                    raise Exception("No se encontró un superusuario para asignar la tarea.")
                
                new_task = PendingContentTask.objects.create(
                    subject=subject_to_process, assigned_to=admin_user, task_origin=origin
                )
                
                log_msg = f"LANZADA: Tarea para el grupo '{subject_to_process.name}' (representante ID: {subject_to_process.id})."
                _log_structured_event(log_msg, "INFO", {"task_id": str(new_task.id)})
                generate_full_course_task.delay(str(new_task.id))
                status_msg = f"TAREA LANZADA: '{subject_to_process.name}' (ID: {new_task.id})."
                automation_settings.last_run_status = status_msg
                automation_settings.last_run_timestamp = timezone.now()
                automation_settings.save(update_fields=['last_run_status', 'last_run_timestamp'])
                break

            else:
                filters_were_advanced = _advance_seed_filters_if_needed(automation_settings)
                if filters_were_advanced:
                    _log_structured_event("RE-INTENTO: Lote finalizado, re-intentando encontrar trabajo con filtros más amplios.", "INFO")
                    continue
                else:
                    final_message = "SIN TRABAJO: No quedan más asignaturas para procesar en la configuración actual."
                    _log_structured_event(final_message, "INFO")
                    if automation_settings.last_run_status != final_message:
                         _send_admin_notification("Motor de Automatización en Pausa", final_message)
                         automation_settings.last_run_status = final_message
                         automation_settings.save(update_fields=['last_run_status'])
                    break

    except Exception as e:
        status_msg = f"ERROR CRÍTICO EN BUCLE: {e}"
        _log_structured_event(status_msg, level="CRITICAL", details={"traceback": traceback.format_exc()})
        logger.critical(f"AUTOMATION LOOP: {status_msg}", exc_info=True)
        if 'automation_settings' in locals() and automation_settings:
            automation_settings.last_run_status = status_msg
            automation_settings.save(update_fields=['last_run_status'])
    finally:
        db.close_old_connections()
