# /home/MiguelAeTxio/CampuStudiOnline/assessment/tasks.py
import logging
import re
import time
from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from google.api_core.exceptions import DeadlineExceeded
from datetime import timedelta

from .models import Assessment, Question, UserAnswer
from academic_structure.models import Subject
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

@shared_task
def generate_assessment_from_content_task(assessment_id):
    log_timestamp(f"GENERATION_TASK: INICIO para Assessment ID {assessment_id}.")

    try:
        with transaction.atomic():
            assessment = Assessment.objects.select_for_update().get(pk=assessment_id)
            if assessment.status != "PENDING":
                return f"Tarea omitida. Estado: {assessment.status}."
            assessment.status = "PROCESSING"
            assessment.save(update_fields=["status"])
    except Assessment.DoesNotExist:
        logger.error(f"GENERATION_TASK: No se encontró Assessment con ID: {assessment_id}.")
        return f"Error: Assessment con ID {assessment_id} no encontrado."

    try:
        full_content = assessment.content.get_full_markdown_content()
        if not full_content or not full_content.strip():
            raise ValueError("El contenido para la evaluación está vacío.")

        subject = assessment.content.subject
        
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

        if subject and subject.learning_objectives and subject.learning_objectives.strip():
            learning_objectives = subject.learning_objectives
            logger.info(f"Generando evaluación para contenido académico (Subject: {subject.name}).")
            prompt = (
                f"Tu tarea es crear un examen basado en los siguientes Objetivos de Aprendizaje:\n"
                f"<OBJETIVOS>\n{learning_objectives}\n</OBJETIVOS>\n\n"
                f"Usa el material de estudio adjunto como fuente para formular preguntas que evalúen estos objetivos.\n\n"
                f"{prompt_format_instructions}\n\n"
                f"Material de estudio:\n---\n{full_content}\n---"
            )
        else:
            logger.info(f"Generando evaluación para contenido libre (Título: {assessment.content.title}).")
            prompt = (
                f"Tu tarea es crear un examen basado en el siguiente texto, cubriendo sus conceptos clave.\n\n"
                f"{prompt_format_instructions}\n\n"
                f"Material de estudio:\n---\n{full_content}\n---"
            )

        success, response_text, api_key_used = generate_text_content(prompt)
        if not success:
            raise AIServiceCriticalError(f"La llamada a la API de texto falló: {response_text}")

        questions_data = _parse_assessment_text(response_text)

        if not questions_data:
            raise ValueError(
                "No se pudieron extraer preguntas del texto generado por la IA. "
                f"Respuesta cruda (primeros 500 chars): '{response_text[:500]}...'"
            )

        num_questions = len(questions_data)
        with transaction.atomic():
            assessment_to_complete = Assessment.objects.get(pk=assessment_id)
            assessment_to_complete.total_questions_expected = num_questions
            questions_to_create = [
                Question(
                    assessment=assessment_to_complete,
                    question_text=q["question"],
                    model_answer=q["model_answer"],
                )
                for q in questions_data
            ]
            Question.objects.bulk_create(questions_to_create)

            assessment_to_complete.status = "COMPLETED"
            assessment_to_complete.questions_processed = num_questions
            assessment_to_complete.save()

        log_timestamp(f"GENERATION_TASK: ÉXITO para Assessment ID {assessment_id}. Generadas {num_questions} preguntas.")

        context = {"assessment_pk": assessment_to_complete.pk, "content_title": assessment_to_complete.content.title}
        send_unified_notification(user=assessment_to_complete.user, subject_template="assessment/email/assessment_ready_subject.txt", body_template_prefix="assessment/email/assessment_ready_body", context=context)
        return f"Evaluación {assessment_id} generada con {num_questions} preguntas."

    except (DeadlineExceeded, AIServiceCriticalError) as e:
        logger.error(f"GENERATION_TASK: ERROR de API para Assessment ID {assessment_id}: {e}", exc_info=True)
        Assessment.objects.filter(pk=assessment_id).update(status="TIMEOUT_FAILURE")
        return f"Error de API en Assessment {assessment_id}."
    except Exception as e:
        logger.error(f"GENERATION_TASK: ERROR INESPERADO para Assessment ID {assessment_id}: {e}", exc_info=True)
        Assessment.objects.filter(pk=assessment_id).update(status="FAILED")
        return f"Error al procesar evaluación {assessment_id}: {e}"


@shared_task
def correct_assessment_task(assessment_id):
    log_timestamp(f"CORRECTION_TASK: INICIO para Assessment ID: {assessment_id}")
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
        user_answers = UserAnswer.objects.filter(question__assessment=assessment).select_related("question")
        num_answers = user_answers.count()

        if num_answers == 0:
            assessment.status = "COMPLETED"
            assessment.save(update_fields=["status"])
            return f"No hay respuestas para evaluación {assessment_id}."

        assessment.total_questions_expected = num_answers
        assessment.questions_processed = 0
        assessment.save(update_fields=["total_questions_expected", "questions_processed"])

        expiration_date = timezone.now() + timedelta(seconds=getattr(settings, "CORRECTION_VISIBILITY_DURATION_SECONDS", 86400))
        
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
            try:
                prompt = (
                    f"Evalúa la siguiente respuesta de un usuario, comparándola con la pregunta y la respuesta modelo.\n\n"
                    f'Pregunta: "{answer.question.question_text}"\n'
                    f'Respuesta Modelo: "{answer.question.model_answer}"\n'
                    f'Respuesta del Usuario: "{answer.answer_text}"\n\n'
                    f"{prompt_format_instructions}"
                )
                success, response_text, api_key_used = generate_text_content(prompt)

                if not success:
                    raise AIServiceCriticalError(f"La llamada a la API de texto falló: {response_text}")

                correction_result = _parse_correction_text(response_text)

                if correction_result and correction_result.get("score") is not None:
                    answer.score = correction_result["score"]
                    answer.feedback = correction_result["feedback"]
                    answer.correction_expiration_date = expiration_date
                    answer.save(update_fields=["score", "feedback", "correction_expiration_date"])
                else:
                    logger.warning(f"No se pudo parsear la corrección para UserAnswer ID {answer.id}. Respuesta: {response_text}")

            except Exception as e:
                logger.error(f"CORRECTION_TASK: ERROR corrigiendo UserAnswer ID {answer.id}: {e}", exc_info=True)
            
            Assessment.objects.filter(pk=assessment_id).update(questions_processed=F("questions_processed") + 1)
            if i < num_answers:
                time.sleep(5)

        with transaction.atomic():
            assessment_to_complete = Assessment.objects.select_related("content", "user").get(pk=assessment_id)
            assessment_to_complete.status = "RESULTS_AVAILABLE"
            assessment_to_complete.save(update_fields=["status"])

        log_timestamp(f"CORRECTION_TASK: ÉXITO para Assessment ID {assessment_id}.")
        context = {"assessment_pk": assessment_to_complete.pk, "content_title": assessment_to_complete.content.title}
        send_unified_notification(user=assessment_to_complete.user, subject_template="assessment/email/results_ready_subject.txt", body_template_prefix="assessment/email/results_ready_body", context=context)
        return f"Corrección de evaluación {assessment_id} completada."
    except Exception as e:
        logger.error(f"CORRECTION_TASK: ERROR INESPERADO para Assessment ID {assessment_id}: {e}", exc_info=True)
        Assessment.objects.filter(pk=assessment_id).update(status="FAILED")
        return f"Error en corrección de {assessment_id}: {e}"


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
        status="RESULTS_AVAILABLE", questions__user_answers__correction_expiration_date__lt=now
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
