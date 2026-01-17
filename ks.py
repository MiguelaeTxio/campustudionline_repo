[1mdiff --git a/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/tasks.py b/home/MiguelAeTxio/SWAP/tasks.py.prop[m
[1mindex b31be4f..e868c3f 100644[m
[1m--- a/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/tasks.py[m
[1m+++ b/home/MiguelAeTxio/SWAP/tasks.py.prop[m
[36m@@ -1116,40 +1116,71 @@[m [mdef generate_assessment_from_content_task(self, assessment_id):[m
                    else:[m
                        raise ResourceExhausted(class_resp)[m

                                elif step == 1:
                    log_assessment_task_event(assessment_id, f"PASO 1 (Fuente de Verdad) - Arquetipo: {subject_type}")[m
                    selection = assessment.selection_range[m
                    # Contenido REAL filtrado por sliders [31mfiltered_source[m[32m(Solo en memoria)[m
[32m                    filtered_source_memory[m = filter_content_by_selection(full_content, selection) if selection else full_content
                    
                    [32m# Variables para persistencia en BBDD (Por defecto vacías para limpiar UI)[m
[32m                    db_reading_stimulus = ""[m
[32m                    db_listening_transcript = ""[m
[32m                    [m
[32m                    # Variable para el Generador de Prompts (Memoria)[m
[32m                    prompt_source_text = ""[m

[32m                    # --- LÓGICA DE 3 SCRIPTS (SEPARACIÓN RADICAL) ---[m
                    [m
[31m                    # [HITO 6] BIFURCACIÓN DE FUENTE DE VERDAD[m
                    if subject_type == "LANGUAGES":[m
                        # [31mIDIOMAS: Generación creativa obligatoria[m[32m=== ARQUETIPO 1: IDIOMAS ===[m
[32m                        # Requiere estímulos EXPLICITOS para el alumno (Reading/Listening)[m
                        log_assessment_task_event(assessment_id, [31m"Modo[m[32m"ARQUETIPO[m IDIOMAS: Generando [31mestímulos artificiales...")[m[32mmateriales de lectura y audio...")[m
                        prompt = [31mgenerate_stimulus_creation_prompt(filtered_source,[m[32mgenerate_stimulus_creation_prompt(filtered_source_memory,[m subject_name, subject_type)
                        success, text, _ = generate_text_content(prompt, api_key=api_key)[m
                        if not success: raise ResourceExhausted(text)[m
                        [m
                        dat = dirtyjson.loads(clean_json_response(text))[m
[31m                        r_text = dat.get('reading_stimulus', '')[m
[31m                        l_text = dat.get('listening_transcript', '')[m
[31m                        if not r_text: raise ValueError("IA de Idiomas no generó reading_stimulus.")[m
                        [m
                        [32m# Aquí SI guardamos en BBDD porque el alumno DEBE verlos[m
[32m                        db_reading_stimulus = dat.get('reading_stimulus', '')[m
[32m                        db_listening_transcript = dat.get('listening_transcript', '')[m
[32m                        [m
[32m                        # Para el prompt de preguntas usamos estos estímulos generados[m
[32m                        prompt_source_text = db_reading_stimulus [m
[32m                        [m
[32m                        if not db_reading_stimulus: raise ValueError("IA de Idiomas no generó reading_stimulus.")[m

[32m                    elif subject_type == "EXACT_SCIENCES":[m
[32m                        # === ARQUETIPO 2: CIENCIAS EXACTAS ===[m
[32m                        # Fuente: Contenido Real. Visualización: NINGUNA (Solo preguntas).[m
[32m                        log_assessment_task_event(assessment_id, "ARQUETIPO CIENCIAS: Usando contenido real. UI limpia.")[m
[32m                        prompt_source_text = filtered_source_memory[m
[32m                        # db_reading_stimulus se mantiene VACÍO para que no salga el botón[m

                    else:[m
                        # [32m=== ARQUETIPO 3:[m HUMANIDADES [31m/ CIENCIAS: Fuente =[m[32mY OTRAS ===[m
[32m                        # Fuente:[m Contenido [31mReal[m[32mReal. Visualización: NINGUNA (Solo preguntas).[m
                        log_assessment_task_event(assessment_id, [31m"Modo TRIBUNAL:[m[32m"ARQUETIPO HUMANIDADES:[m Usando contenido [31mreal como Fuente Única.")[m
[31m                        r_text[m[32mreal. UI limpia.")[m
[32m                        prompt_source_text[m = [31mfiltered_source[m
[31m                        l_text = ""[m[32mfiltered_source_memory[m
[32m                        # db_reading_stimulus se mantiene VACÍO para que no salga el botón[m
                        [m
                        if not [31mr_text[m[32mprompt_source_text[m or [31mlen(r_text)[m[32mlen(prompt_source_text)[m < 50:
                            [31mr_text[m[32mprompt_source_text[m = full_content # Fallback [32mtécnico[m

                    [32m# Persistencia diferenciada[m
                    with transaction.atomic():[m
                        aa = Assessment.objects.select_for_update().get(pk=assessment_id)[m
                        aa.reading_stimulus = [31mr_text[m[32mdb_reading_stimulus       # Solo tendrá datos en IDIOMAS[m
                        aa.listening_transcript = [31ml_text[m[32mdb_listening_transcript # Solo tendrá datos en IDIOMAS[m
                        aa.status = Assessment.AssessmentStatus.PROCESSING[m
                        aa.save(update_fields=['reading_stimulus', 'listening_transcript', 'status'])[m
                    
                    [32m# Pasamos el texto fuente correcto al siguiente paso vía atributo temporal del objeto (hack de memoria)[m
[32m                    # o simplemente confiamos en que 'prompt_source_text' está disponible en el scope local para el paso 2[m
[32m                    # ya que estamos dentro del mismo 'while'.[m
[32m                    r_text = prompt_source_text [m
[32m                    l_text = db_listening_transcript[m
                    
                    step = 2[m

                elif step == 2:[m
