import re

# Nuevos imports a inyectar al principio
NEW_IMPORTS = """from assessment.utils import classify_subject_strategy, segment_content_for_assessment, filter_content_by_selection
# [HITO 6] ESTRATEGIAS SEGREGADAS
from core.services.assessment_strategies.classifier import generate_classifier_prompt
from core.services.assessment_strategies.humanities_strategy import generate_humanities_prompt
from core.services.assessment_strategies.languages_strategy import generate_languages_stimuli_prompt, generate_languages_exam_prompt
from core.services.assessment_strategies.sciences_strategy import generate_sciences_prompt
"""

# Nueva función generate_assessment_from_content_task COMPLETA Y SEGREGADA
NEW_TASK_FUNCTION = r'''@shared_task(bind=True, acks_late=True, max_retries=5, default_retry_delay=60)
def generate_assessment_from_content_task(self, assessment_id):
    """
    [HITO 6 - V_FINAL] Pipeline con Estrategias Totalmente Segregadas (Archivos Diferentes).
    """
    from django.shortcuts import get_object_or_404
    log_assessment_task_event(assessment_id, f"TAREA GENERACIÓN: Inicio ejecución v{self.request.retries + 1}.")
    
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
        original_content = assessment.content_copy.original_content
        full_content = original_content.get_full_markdown_content()
        
        subject_obj = original_content.subject.first()
        subject_name = subject_obj.name if subject_obj else original_content.title
        branch_name = subject_obj.academic_year.degree.branch.name if (subject_obj and subject_obj.academic_year) else "General"
        
        step = 0
        subject_type = "HUMANITIES_GENERIC"
        
        # Variables de estado para pasar datos entre pasos
        r_text_memory = "" # Para Humanidades/Ciencias (Contenido Real)
        l_text_memory = "" # Para Idiomas (Transcript)

        while step <= 2:
            automation_settings = AutomationSettings.load()
            api_key = automation_settings.active_api_key
            
            if not api_key or not api_key.is_enabled or api_key.is_quarantined:
                 api_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).order_by('id').first()
                 if api_key:
                     automation_settings.active_api_key = api_key
                     automation_settings.save(update_fields=['active_api_key'])
                 else:
                     log_assessment_task_event(assessment_id, "POOL AGOTADO. Esperando 5m...", level="ERROR")
                     raise self.retry(countdown=300)

            try:
                # --- PASO 0: CLASIFICACIÓN (Router) ---
                if step == 0:
                    log_assessment_task_event(assessment_id, f"PASO 0 (Clasificación) - Key: {api_key.name}")
                    prompt = generate_classifier_prompt(subject_name, branch_name)
                    success, resp, _ = generate_text_content(prompt, api_key=api_key)
                    
                    if success:
                        raw_type = clean_json_response(resp).strip().upper()
                        valid_types = ["EXACT_SCIENCES", "LANGUAGES", "LEGAL", "ARTS", "SOCIETY", "HISTORY", "PHILOLOGY", "HUMANITIES_GENERIC"]
                        found = "HUMANITIES_GENERIC"
                        for vt in valid_types:
                            if vt in raw_type:
                                found = vt
                                break
                        subject_type = found
                        log_assessment_task_event(assessment_id, f"Arquetipo Detectado: {subject_type}")
                        step = 1
                    else:
                        raise ResourceExhausted(resp)

                # --- PASO 1: PREPARACIÓN DE FUENTE (Bifurcación Radical) ---
                elif step == 1:
                    selection = assessment.selection_range
                    filtered_content = filter_content_by_selection(full_content, selection) if selection else full_content
                    
                    db_reading = ""
                    db_listening = ""
                    
                    if subject_type == "LANGUAGES":
                        # ESTRATEGIA IDIOMAS: Generar estímulos artificiales
                        log_assessment_task_event(assessment_id, "Ejecutando Estrategia: IDIOMAS (Generación Creativa)")
                        prompt = generate_languages_stimuli_prompt(filtered_content, subject_name)
                        success, text, _ = generate_text_content(prompt, api_key=api_key)
                        if not success: raise ResourceExhausted(text)
                        
                        dat = dirtyjson.loads(clean_json_response(text))
                        db_reading = dat.get('reading_stimulus', '')
                        db_listening = dat.get('listening_transcript', '')
                        
                        # En idiomas, la "fuente" para las preguntas ES el estímulo generado
                        r_text_memory = db_reading
                        l_text_memory = db_listening
                        
                        if not db_reading: raise ValueError("Fallo en generación de Reading.")

                    elif subject_type == "EXACT_SCIENCES":
                        # ESTRATEGIA CIENCIAS: Contenido Real
                        log_assessment_task_event(assessment_id, "Ejecutando Estrategia: CIENCIAS (Resolución Problemas)")
                        r_text_memory = filtered_content
                        # db_reading queda VACÍO -> UI limpia

                    else:
                        # ESTRATEGIA HUMANIDADES (Tribunales): Contenido Real
                        log_assessment_task_event(assessment_id, f"Ejecutando Estrategia: TRIBUNAL {subject_type} (Conocimiento)")
                        r_text_memory = filtered_content
                        if not r_text_memory or len(r_text_memory) < 50: r_text_memory = full_content
                        # db_reading queda VACÍO -> UI limpia

                    # Guardar en BBDD (Solo Idiomas tendrá datos visibles)
                    with transaction.atomic():
                        aa = Assessment.objects.select_for_update().get(pk=assessment_id)
                        aa.reading_stimulus = db_reading
                        aa.listening_transcript = db_listening
                        aa.status = Assessment.AssessmentStatus.PROCESSING
                        aa.save(update_fields=['reading_stimulus', 'listening_transcript', 'status'])
                    step = 2

                # --- PASO 2: GENERACIÓN DE EXAMEN (Llamadas a archivos distintos) ---
                elif step == 2:
                    log_assessment_task_event(assessment_id, f"PASO 2 (Generación Preguntas) - {subject_type}")
                    
                    prompt = ""
                    if subject_type == "LANGUAGES":
                        prompt = generate_languages_exam_prompt(r_text_memory, l_text_memory)
                    elif subject_type == "EXACT_SCIENCES":
                        prompt = generate_sciences_prompt(r_text_memory)
                    else:
                        # Humanidades (Cualquiera de los tribunales)
                        prompt = generate_humanities_prompt(r_text_memory, tribunal_type=subject_type)
                    
                    success, text, _ = generate_text_content(prompt, api_key=api_key)
                    if not success: raise ResourceExhausted(text)
                    
                    questions_data = _parse_assessment_text(text)
                    if not questions_data: raise ValueError("IA no devolvió preguntas válidas.")
                    
                    with transaction.atomic():
                        a = Assessment.objects.select_for_update().get(pk=assessment_id)
                        a.questions.all().delete()
                        a.total_questions_expected = len(questions_data)
                        a.save(update_fields=['total_questions_expected'])
                        for idx, q_data in enumerate(questions_data, 1):
                            Question.objects.create(assessment=a, **q_data)
                            a.questions_processed = idx
                            a.save(update_fields=['questions_processed'])
                    step = 3

            except (ResourceExhausted, AIServiceCriticalError) as e:
                api_key.refresh_from_db()
                api_key.consecutive_failures += 1
                api_key.save(update_fields=["consecutive_failures"])
                log_assessment_task_event(assessment_id, f"FALLO CUOTA ({api_key.consecutive_failures}/4): {api_key.name}", level="WARNING")
                
                if api_key.consecutive_failures >= 4:
                    api_key.is_quarantined = True
                    api_key.save(update_fields=["is_quarantined"])
                    _request_quarantine_via_mailbox(api_key)
                
                time.sleep(5)
                continue

        # Finalización exitosa
        with transaction.atomic():
            comp_assessment = Assessment.objects.select_for_update().get(pk=assessment_id)
            comp_assessment.status = Assessment.AssessmentStatus.COMPLETED
            comp_assessment.last_error = None
            comp_assessment.save()
        log_assessment_task_event(assessment_id, "Proceso completado con ÉXITO.", level="SUCCESS")

    except Exception as e:
        log_assessment_task_event(assessment_id, f"ERROR FATAL: {str(e)}", level="ERROR")
        Assessment.objects.filter(pk=assessment_id).update(status=Assessment.AssessmentStatus.GENERATION_FAILED_RETRYABLE, last_error=str(e))
        raise self.retry(exc=e)
'''

with open("/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/tasks.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Inyectar imports
content = content.replace(
    "from assessment.utils import classify_subject_strategy, segment_content_for_assessment, filter_content_by_selection",
    NEW_IMPORTS
)

# 2. Reemplazar la función entera generate_assessment_from_content_task
pattern_func = re.compile(r'@shared_task\(bind=True, acks_late=True, max_retries=5, default_retry_delay=60\)\s*def generate_assessment_from_content_task.*?raise self\.retry\(exc=e\)', re.DOTALL)

match = pattern_func.search(content)
if match:
    content = content.replace(match.group(0), NEW_TASK_FUNCTION)
else:
    print("NO SE ENCONTRÓ LA FUNCIÓN PARA REEMPLAZAR")

with open("/home/MiguelAeTxio/SWAP/tasks.py.strategy_impl", "w", encoding="utf-8") as f:
    f.write(content)
