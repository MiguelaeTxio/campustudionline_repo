import logging
import json
import time
from celery import shared_task
from django.utils import timezone
from django.core.files.base import ContentFile
from .models import Assessment, Question
from orchestrator.models import ApiKey
from core.services import gemini_service
from core.services.assessment_strategies.languages_strategy import generate_languages_stimuli_prompt, generate_languages_item_prompt, get_target_language

logger = logging.getLogger(__name__)

@shared_task(name="assessment.process_fase_b")
def process_assessment_fase_b(assessment_id):
    """
    [HITO 6] Orquestador de Fase B: Relleno de contenido y generación de audio MP3.
    Refactorizado para Flujo Atómico (Item-by-Item) según Ley Técnica UGR.
    """
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
        if assessment.status != Assessment.AssessmentStatus.PROCESSING:
            return "Estado no válido para procesamiento."

        # 1. Rotación de ApiKey
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
            if hasattr(val, 'text'):
                return val.text.strip()
            if isinstance(val, dict):
                return val.get('text', val.get('content', val.get('body', str(val))))
            if isinstance(val, list):
                return "".join([_extract_text(p) for p in val])
            return str(val) if val else ""

        assessment.reading_stimulus = _extract_text(stimuli_data.get("reading_stimulus"))
        assessment.listening_transcript = _extract_text(stimuli_data.get("listening_transcript"))
        assessment.save()
        
        # 3. Relleno de Esqueleto (Atomic Flow)
        # Determinamos configuración lingüística
        itinerary = assessment.language_itinerary or ("MINOR" if assessment.is_minor_language else "MAIOR")
        target_lang = get_target_language(assessment.content.title)
        
        questions_qs = assessment.questions.all().order_by('id')
        
        for index, question_obj in enumerate(questions_qs):
            try:
                # a. Generar prompt específico (Firma corregida para Atomic Flow)
                item_prompt = generate_languages_item_prompt(
                    reading_text=assessment.reading_stimulus,
                    listening_transcript=assessment.listening_transcript,
                    cefr_level="B1" if itinerary == "MINOR" else "C1",
                    question_obj=question_obj,
                    itinerary=itinerary,
                    target_lang=target_lang
                )
                
                # b. Llamada a Gemini (Atómica) con retry local simple
                q_success = False
                for _ in range(2):
                    q_success, q_raw, _ = gemini_service.generate_text_content(item_prompt, api_key)
                    if q_success: break
                
                if q_success:
                    q_data = json.loads(gemini_service.clean_json_response(q_raw))
                    
                    question_obj.question_text = q_data.get("question_text", "Error generating question")
                    question_obj.model_answer = q_data.get("model_answer", "")
                    question_obj.options = q_data.get("options", [])
                    
                    # [HITO 6] Auto-Reparación de Cloze Engine (Self-Healing)
                    if question_obj.interaction_type in ['QT_CLZ_OPT', 'QT_CLZ_OPN']:
                        if '[' not in question_obj.question_text or ']' not in question_obj.question_text:
                            token = ""
                            if question_obj.options:
                                opts = [str(o) for o in question_obj.options]
                                if question_obj.model_answer not in opts:
                                    opts.append(question_obj.model_answer)
                                token = f"[{'/'.join(opts)}]"
                            else:
                                token = f"[{question_obj.model_answer}]"
                            
                            if question_obj.model_answer in question_obj.question_text:
                                question_obj.question_text = question_obj.question_text.replace(question_obj.model_answer, token)
                            else:
                                question_obj.question_text = f"{question_obj.question_text} {token}"
                    
                    question_obj.save()
                    # Actualizamos progreso
                    assessment.questions_processed = index + 1
                    assessment.save(update_fields=['questions_processed'])
                else:
                    assessment.add_log_event(f"Fallo generando pregunta {question_obj.id}", "ERROR")
            
            except Exception as q_e:
                logger.error(f"Error procesando pregunta {question_obj.id}: {q_e}")
                continue # Continuamos con la siguiente para no bloquear el examen

        # 5. Generación de Audio Nativo (MP3 Obligatorio)
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
                time.sleep(2)
            
            if audio_success:
                filename = f"assessment_audio_{assessment.pk}.mp3"
                assessment.generated_audio.save(filename, ContentFile(audio_data), save=False)
                assessment.add_log_event(f"Audio MP3 generado correctamente")
            else:
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
