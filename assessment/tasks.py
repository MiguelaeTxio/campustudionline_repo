# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment/tasks.py
import logging
import re
import time
import traceback
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from google.api_core.exceptions import DeadlineExceeded
from datetime import timedelta

from .models import Assessment, Question, UserAnswer, AssessmentSettings
from academic_structure.models import Subject
from content_automation.models import ApiKey
from core.services.gemini_service import generate_text_content, AIServiceCriticalError
from core.services.gemini_schemas import ASSESSMENT_CORRECTION_SCHEMA
from core.utils import send_unified_notification

logger = logging.getLogger(__name__)
User = get_user_model()


def log_timestamp(message):
    logger.info(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] {message}")


# --- Helper Functions for Parsing ---

def _parse_assessment_text(text: str) -> list:
    """
    Parsea la respuesta de texto plano de la IA para extraer preguntas y respuestas.
    """
    questions = []
    pattern = re.compile(
        r"\[---PREGUNTA---\](.*?)" r"\[---RESPUESTA---\](.*?)" r"\[---FIN-PREGUNTA---\]",
        re.DOTALL,
    )
    matches = pattern.findall(text)
    for match in matches:
        question_text = match[0].strip()
        model_answer = match[1].strip()
        if question_text and model_answer:
            questions.append(
                {"question": question_text, "model_answer": model_answer}
            )
    return questions


def _parse_correction_text(text: str) -> dict:
    """
    Parsea la respuesta de texto plano de la IA para extraer puntuación y feedback.
    """
    score = None
    feedback = ""

    score_match = re.search(r"PUNTUACION:\s*(\d+)", text, re.IGNORECASE)
    if score_match:
        try:
            score = int(score_match.group(1))
            if not (0 <= score <= 100):
                score = None # Invalid score range
        except (ValueError, IndexError):
            score = None

    feedback_match = re.search(r"FEEDBACK:\s*(.*)", text, re.DOTALL | re.IGNORECASE)
    if feedback_match:
        feedback = feedback_match.group(1).strip()

    return {"score": score, "feedback": feedback}


# --- Celery Tasks ---

@shared_task(bind=True, acks_late=True)
def generate_assessment_from_content_task(self, assessment_id):
    log_timestamp(f"GENERATION_TASK: INICIO para Assessment ID {assessment_id}. Intento: {self.request.retries + 1}")
    
    assessment = None
    try:
        with transaction.atomic():
            assessment = Assessment.objects.select_related(
                'content_copy', 'user'
            ).select_for_update().get(pk=assessment_id)

            if assessment.status not in [Assessment.AssessmentStatus.PENDING, Assessment.AssessmentStatus.FAILED_RETRYABLE]:
                return f"Tarea omitida. Estado actual: {assessment.get_status_display()}."

            assessment.status = Assessment.AssessmentStatus.PROCESSING
            assessment.save(update_fields=["status"])

    except Assessment.DoesNotExist:
        logger.error(f"GENERATION_TASK: No se encontró Assessment con ID: {assessment_id}.")
        return

    try:
        original_content = assessment.content_copy.original_content
        full_content = original_content.get_full_markdown_content()

        if not full_content or not full_content.strip():
            raise ValueError("El contenido para la evaluación está vacío.")

        subjects = getattr(original_content, "subjects", None)
        subject = subjects.first() if subjects and subjects.exists() else None

        prompt_format_instructions = (
            "**FORMATO DE SALIDA OBLIGATORIO:**\n"
            "Cada par pregunta-respuesta DEBE seguir esta estructura exacta, usando los separadores como se indica:\n"
            "[---PREGUNTA---]\n"
            "Aquí el texto completo de la pregunta.\n"
            "[---RESPUESTA---]\n"
            "Aquí el texto completo de la respuesta modelo.\n"
            "[---FIN-PREGUNTA---]\n\n"
            "Repite esta estructura para cada pregunta que generes."
        )

        if subject and subject.learning_objectives:
            learning_objectives = subject.learning_objectives
            prompt = (
                f"Tu tarea es crear un examen basado en los siguientes Objetivos de Aprendizaje:\n"
                f"<OBJETIVOS>\n{learning_objectives}\n</OBJETIVOS>\n\n"
                f"Usa el material de estudio adjunto como fuente para formular preguntas que evalúen estos objetivos.\n\n"
                f"{prompt_format_instructions}\n\n"
                f"Material de estudio:\n---\n{full_content}\n---"
            )
        else:
            prompt = (
                f"Tu tarea es crear un examen basado en el siguiente texto, cubriendo sus conceptos clave.\n\n"
                f"{prompt_format_instructions}\n\n"
                f"Material de estudio:\n---\n{full_content}\n---"
            )

        api_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).first()
        if not api_key:
            raise ValueError("No se encontró una clave de API activa y disponible.")

        success, response_text, _ = generate_text_content(prompt, api_key=api_key)
        if not success:
            raise AIServiceCriticalError(f"La llamada a la API de texto falló: {response_text}")

        questions_data = _parse_assessment_text(response_text)
        if not questions_data:
            raise ValueError(f"No se pudieron extraer preguntas. Respuesta IA: '{response_text[:500]}...'")

        with transaction.atomic():
            # Re-fetch for update
            assessment_to_complete = Assessment.objects.select_for_update().get(pk=assessment_id)
            assessment_to_complete.total_questions_expected = len(questions_data)
            Question.objects.bulk_create([
                Question(assessment=assessment_to_complete, **q) for q in questions_data
            ])
            assessment_to_complete.status = Assessment.AssessmentStatus.COMPLETED
            assessment_to_complete.questions_processed = len(questions_data)
            assessment_to_complete.save()

        log_timestamp(f"GENERATION_TASK: ÉXITO para Assessment ID {assessment_id}.")
        context = {"assessment": assessment_to_complete}
        send_unified_notification(user=assessment_to_complete.user, subject_template="assessment/email/assessment_ready_subject.txt", body_template_prefix="assessment/email/assessment_ready_body", context=context)

    except (DeadlineExceeded, AIServiceCriticalError, ValueError) as e:
        logger.error(f"GENERATION_TASK: ERROR RECUPERABLE para Assessment ID {assessment_id}: {e}", exc_info=True)
        if assessment:
            assessment.status = Assessment.AssessmentStatus.FAILED_RETRYABLE
            assessment.last_error = traceback.format_exc()
            assessment.save(update_fields=["status", "last_error"])
        try:
            raise self.retry(exc=e, countdown=60)
        except MaxRetriesExceededError:
            logger.critical(f"GENERATION_TASK: FALLO FATAL para Assessment ID {assessment_id} tras múltiples reintentos.")
            assessment.status = Assessment.AssessmentStatus.FAILED_FATAL
            assessment.save(update_fields=["status"])
    except Exception as e:
        logger.error(f"GENERATION_TASK: ERROR INESPERADO para Assessment ID {assessment_id}: {e}", exc_info=True)
        if assessment:
            assessment.status = Assessment.AssessmentStatus.FAILED_RETRYABLE
            assessment.last_error = traceback.format_exc()
            assessment.save(update_fields=["status", "last_error"])
        try:
            raise self.retry(exc=e, countdown=300)
        except MaxRetriesExceededError:
            logger.critical(f"GENERATION_TASK: FALLO FATAL (inesperado) para Assessment ID {assessment_id}.")
            assessment.status = Assessment.AssessmentStatus.FAILED_FATAL
            assessment.save(update_fields=["status"])


@shared_task(bind=True, acks_late=True)
def correct_assessment_task(self, assessment_id):
    log_timestamp(f"CORRECTION_TASK: INICIO para Assessment ID: {assessment_id}. Intento: {self.request.retries + 1}")
    
    assessment = None
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
        user_answers = UserAnswer.objects.filter(question__assessment=assessment).select_related("question")

        if not user_answers.exists():
            assessment.status = Assessment.AssessmentStatus.COMPLETED
            assessment.save(update_fields=["status"])
            return

        assessment.total_questions_expected = user_answers.count()
        assessment.questions_processed = 0
        assessment.save(update_fields=["total_questions_expected", "questions_processed"])

        app_settings = AssessmentSettings.get_settings()
        expiration_date = timezone.now() + timedelta(days=app_settings.results_expiration_days)
        prompt_format_instructions = (
            "**FORMATO DE SALIDA OBLIGATORIO:**\n"
            "Debes generar DOS líneas, cada una con un prefijo claro:\n"
            "PUNTUACION: [Un número entero de 0 a 100]\n"
            "FEEDBACK: [Tu feedback constructivo detallado]"
        )

        for i, answer in enumerate(user_answers, 1):
            if not answer.answer_text:
                Assessment.objects.filter(pk=assessment_id).update(questions_processed=F("questions_processed") + 1)
                continue
            
            prompt = (
                f"Evalúa la siguiente respuesta de un usuario, comparándola con la pregunta y la respuesta modelo.\n\n"
                f'Pregunta: "{answer.question.question_text}"\n'
                f'Respuesta Modelo: "{answer.question.model_answer}"\n'
                f'Respuesta del Usuario: "{answer.answer_text}"\n\n'
                f"{prompt_format_instructions}"
            )
            success, response_text, _ = generate_text_content(prompt)

            if not success:
                raise AIServiceCriticalError(f"API falló para UserAnswer ID {answer.id}: {response_text}")

            correction = _parse_correction_text(response_text)
            if correction and correction.get("score") is not None:
                answer.score = correction["score"]
                answer.feedback = correction["feedback"]
                answer.correction_expiration_date = expiration_date
                answer.save(update_fields=["score", "feedback", "correction_expiration_date"])
            
            Assessment.objects.filter(pk=assessment_id).update(questions_processed=F("questions_processed") + 1)
            if i < user_answers.count():
                time.sleep(5)

        with transaction.atomic():
            assessment_to_complete = Assessment.objects.select_for_update().get(pk=assessment_id)
            assessment_to_complete.status = Assessment.AssessmentStatus.RESULTS_AVAILABLE
            assessment_to_complete.results_expiration_date = expiration_date
            assessment_to_complete.save(update_fields=["status", "results_expiration_date"])

        log_timestamp(f"CORRECTION_TASK: ÉXITO para Assessment ID {assessment_id}.")
        context = {"assessment_pk": assessment_id, "content_title": assessment_to_complete.content_copy.original_content.title}
        send_unified_notification(user=assessment_to_complete.user, subject_template="assessment/email/results_ready_subject.txt", body_template_prefix="assessment/email/results_ready_body", context=context)

    except (AIServiceCriticalError) as e:
        logger.error(f"CORRECTION_TASK: ERROR RECUPERABLE para Assessment ID {assessment_id}: {e}", exc_info=True)
        if assessment:
            assessment.status = Assessment.AssessmentStatus.FAILED_RETRYABLE
            assessment.last_error = traceback.format_exc()
            assessment.save(update_fields=["status", "last_error"])
        try:
            raise self.retry(exc=e, countdown=60)
        except MaxRetriesExceededError:
            logger.critical(f"CORRECTION_TASK: FALLO FATAL para Assessment ID {assessment_id}.")
            assessment.status = Assessment.AssessmentStatus.FAILED_FATAL
            assessment.save(update_fields=["status"])
    except Exception as e:
        logger.error(f"CORRECTION_TASK: ERROR INESPERADO para Assessment ID {assessment_id}: {e}", exc_info=True)
        if assessment:
            assessment.status = Assessment.AssessmentStatus.FAILED_RETRYABLE
            assessment.last_error = traceback.format_exc()
            assessment.save(update_fields=["status", "last_error"])
        try:
            raise self.retry(exc=e, countdown=300)
        except MaxRetriesExceededError:
            logger.critical(f"CORRECTION_TASK: FALLO FATAL (inesperado) para Assessment ID {assessment_id}.")
            assessment.status = Assessment.AssessmentStatus.FAILED_FATAL
            assessment.save(update_fields=["status"])


@shared_task(name="assessment.tasks.expire_untaken_assessments")
def expire_untaken_assessments():
    now = timezone.now()
    expiration_limit = getattr(settings, "ASSESSMENT_EXPIRATION_SECONDS", 86400)
    expiration_threshold = now - timedelta(seconds=expiration_limit)
    log_timestamp(f"EXPIRE_UNTAKEN_TASK: Buscando evaluaciones 'COMPLETED' creadas antes de {expiration_threshold}.")

    assessments_to_expire = Assessment.objects.filter(status="COMPLETED", created_at__lt=expiration_threshold)
    count = assessments_to_expire.count()

    if count == 0:
        return "No hay evaluaciones no realizadas para expirar."

    updated_rows = assessments_to_expire.update(status="EXPIRED_UNTAKEN")
    log_timestamp(f"EXPIRE_UNTAKEN_TASK: Se han hecho caducar {updated_rows} evaluaciones.")
    return f"Se han marcado como caducadas {updated_rows} evaluaciones."


@shared_task(name="assessment.tasks.purge_and_penalize_corrections")
def purge_and_penalize_corrections():
    now = timezone.now()
    log_timestamp(f"PURGE_PENALIZE_TASK: Buscando correcciones caducadas antes de {now}.")

    expired_assessments = Assessment.objects.filter(
        status="RESULTS_AVAILABLE", results_expiration_date__lt=now
    ).distinct()

    if not expired_assessments.exists():
        return "No hay correcciones para procesar."

    assessments_to_penalize = expired_assessments.filter(was_viewed=False)
    penalized_count = assessments_to_penalize.update(status="CORRECTION_EXPIRED")
    if penalized_count > 0:
        log_timestamp(f"PURGE_PENALIZE_TASK: Penalizadas {penalized_count} evaluaciones no vistas.")

    answers_to_purge = UserAnswer.objects.filter(question__assessment__in=expired_assessments, score__isnull=False)
    purged_count = answers_to_purge.update(
        score=None, feedback="La corrección y el feedback de esta respuesta han caducado."
    )
    if purged_count > 0:
        log_timestamp(f"PURGE_PENALIZE_TASK: Purgado el contenido de {purged_count} respuestas.")

    return f"Tarea completada. Penalizadas: {penalized_count}. Purgadas: {purged_count}."
