# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment/tasks.py
import logging
import json
from celery import shared_task
from django.utils import timezone
from django.core.files.base import ContentFile
from .models import Assessment, Question
from orchestrator.models import ApiKey
from core.services import gemini_service
from core.services.assessment_strategies.languages_strategy import generate_languages_stimuli_prompt, generate_languages_exam_prompt

logger = logging.getLogger(__name__)

@shared_task(name="assessment.process_fase_b")
def process_assessment_fase_b(assessment_id):
    """
    [HITO 6] Orquestador de Fase B: Relleno de contenido y generación de audio MP3.
    """
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
        if assessment.status != Assessment.AssessmentStatus.PROCESSING:
            return "Estado no válido para procesamiento."

        # 1. Rotación de ApiKey (Basado en PAIR de orquestador)
        api_key = ApiKey.get_best_key()
        if not api_key:
            assessment.add_log_event("No hay API Keys disponibles", "CRITICAL")
            assessment.status = Assessment.AssessmentStatus.GENERATION_FAILED_RETRYABLE
            assessment.save()
            return "No keys"

        # 2. Generación de Estímulos (Reading/Listening)
        stimuli_prompt = generate_languages_stimuli_prompt(
            assessment.content.markdown_content, 
            assessment.content.title
        )
        
        success, raw_json, _ = gemini_service.generate_text_content(stimuli_prompt, api_key)
        if not success:
            raise Exception(f"Fallo en estímulos: {raw_json}")

        stimuli_data = json.loads(gemini_service.clean_json_response(raw_json))
        
        def _extract_text(val):
            # Caso 1: Es el objeto AttributedDict del SDK de Google
            if hasattr(val, 'text'):
                return val.text.strip()
            # Caso 2: Es un diccionario con claves comunes
            if isinstance(val, dict):
                return val.get('text', val.get('content', val.get('body', str(val))))
            # Caso 3: Es una lista (a veces Gemini devuelve partes)
            if isinstance(val, list):
                return "".join([_extract_text(p) for p in val])
            return str(val) if val else ""

        assessment.reading_stimulus = _extract_text(stimuli_data.get("reading_stimulus"))
        assessment.listening_transcript = _extract_text(stimuli_data.get("listening_transcript"))
        
        # 3. Generación de Preguntas
        exam_prompt = generate_languages_exam_prompt(
            assessment.reading_stimulus,
            assessment.listening_transcript,
            stimuli_data.get("cefr_level", "B1")
        )
        
        success, raw_json, _ = gemini_service.generate_text_content(exam_prompt, api_key)
        if not success:
            raise Exception(f"Fallo en examen: {raw_json}")

        exam_data = json.loads(gemini_service.clean_json_response(raw_json))
        
        
        # 4. Relleno de Esqueleto (Atomic Flow)
        # Obtenemos las preguntas vacías creadas en la Fase A
        questions_qs = assessment.questions.all().order_by('id')
        exam_questions = exam_data.get("questions", [])

        for question_obj, data in zip(questions_qs, exam_questions):
            question_obj.question_text = data["question_text"]
            question_obj.model_answer = data["model_answer"]
            question_obj.options = data.get("options", [])
            # [HITO 6] Parsing Estructural para Match/Order
            if question_obj.interaction_type in ['QT_MATCH', 'QT_ORDER'] and not question_obj.options:
                # Si Gemini no devuelve opciones, intentamos inferir o loguear error
                # Para MATCH se espera lista de pares o diccionario
                assessment.add_log_event(f"Advertencia: {question_obj.interaction_type} sin opciones en Q{question_obj.pk}", "WARNING")
            

            
            # [HITO 6] Auto-Reparación de Cloze Engine (Self-Healing)
            # Si es tipo Cloze y no detectamos corchetes, inyectamos el token formateado.
            if question_obj.interaction_type in ['QT_CLZ_OPT', 'QT_CLZ_OPN']:
                if '[' not in question_obj.question_text or ']' not in question_obj.question_text:
                    # 1. Construcción del Token [opcion1/opcion2] o [respuesta]
                    token = ""
                    if question_obj.options: # Cloze con opciones
                        opts = [str(o) for o in question_obj.options]
                        # Aseguramos que la correcta esté incluida para evitar bloqueos
                        if question_obj.model_answer not in opts:
                            opts.append(question_obj.model_answer)
                        token = f"[{'/'.join(opts)}]"
                    else: # Cloze abierto
                        token = f"[{question_obj.model_answer}]"
                    
                    # 2. Cirugía (Inyección)
                    # Intento A: Sustitución de la respuesta exacta en el texto
                    if question_obj.model_answer in question_obj.question_text:
                         question_obj.question_text = question_obj.question_text.replace(question_obj.model_answer, token)
                         assessment.add_log_event(f"Auto-Reparación Cloze (Sustitución) en Q{question_obj.pk}", "WARNING")
                    # Intento B: Fallback (Añadir al final)
                    else:
                         question_obj.question_text = f"{question_obj.question_text} {token}"
                         assessment.add_log_event(f"Auto-Reparación Cloze (Append) en Q{question_obj.pk}", "WARNING")
            
            question_obj.save()

        # 5. Generación de Audio Nativo (MP3 Obligatorio con Reintentos)
        if assessment.listening_transcript:
            audio_prompt = f"Lee este texto con acento nativo perfecto para un examen de idiomas: {assessment.listening_transcript}"
            
            audio_success = False
            audio_data = None
            max_retries = 3
            
            for intento in range(1, max_retries + 1):
                logger.info(f"Intento {intento} de generación de audio para Assessment {assessment_id}")
                audio_success, audio_data, _ = gemini_service.generate_audio_content(audio_prompt, api_key)
                if audio_success:
                    break
                time.sleep(2)  # Delay proactivo entre reintentos
            
            if audio_success:
                filename = f"assessment_audio_{assessment.pk}.mp3"
                assessment.generated_audio.save(filename, ContentFile(audio_data), save=False)
                assessment.add_log_event(f"Audio MP3 generado correctamente (Intento {intento})")
            else:
                # Si falla el audio, la evaluación NO está completa.
                assessment.add_log_event("Error crítico: Fallo en la generación de audio tras reintentos", "ERROR")
                raise Exception("Recurso de audio obligatorio no generado. Abortando finalización.")

        assessment.status = Assessment.AssessmentStatus.COMPLETED
        assessment.save()
        return f"Assessment {assessment_id} completado."

    except Exception as e:
        logger.error(f"Error en Fase B: {e}")
        if 'assessment' in locals():
            assessment.status = Assessment.AssessmentStatus.GENERATION_FAILED_RETRYABLE
            assessment.last_error = str(e)
            assessment.save()
        return str(e)
