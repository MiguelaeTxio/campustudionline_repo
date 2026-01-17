import re

# Vamos a reemplazar el bloque del Paso 1 (Fuente de Verdad) para implementar la SEPARACIÓN RADICAL.
# En Humanidades/Ciencias, la variable 'reading_stimulus' de la BBDD se fuerza a vacía.

NEW_LOGIC_STEP_1 = r'''                elif step == 1:
                    log_assessment_task_event(assessment_id, f"PASO 1 (Fuente de Verdad) - Arquetipo: {subject_type}")
                    selection = assessment.selection_range
                    # Contenido REAL filtrado por sliders (Solo en memoria)
                    filtered_source_memory = filter_content_by_selection(full_content, selection) if selection else full_content
                    
                    # Variables para persistencia en BBDD (Por defecto vacías para limpiar UI)
                    db_reading_stimulus = ""
                    db_listening_transcript = ""
                    
                    # Variable para el Generador de Prompts (Memoria)
                    prompt_source_text = ""

                    # --- LÓGICA DE 3 SCRIPTS (SEPARACIÓN RADICAL) ---
                    
                    if subject_type == "LANGUAGES":
                        # === ARQUETIPO 1: IDIOMAS ===
                        # Requiere estímulos EXPLICITOS para el alumno (Reading/Listening)
                        log_assessment_task_event(assessment_id, "ARQUETIPO IDIOMAS: Generando materiales de lectura y audio...")
                        prompt = generate_stimulus_creation_prompt(filtered_source_memory, subject_name, subject_type)
                        success, text, _ = generate_text_content(prompt, api_key=api_key)
                        if not success: raise ResourceExhausted(text)
                        
                        dat = dirtyjson.loads(clean_json_response(text))
                        
                        # Aquí SI guardamos en BBDD porque el alumno DEBE verlos
                        db_reading_stimulus = dat.get('reading_stimulus', '')
                        db_listening_transcript = dat.get('listening_transcript', '')
                        
                        # Para el prompt de preguntas usamos estos estímulos generados
                        prompt_source_text = db_reading_stimulus 
                        
                        if not db_reading_stimulus: raise ValueError("IA de Idiomas no generó reading_stimulus.")

                    elif subject_type == "EXACT_SCIENCES":
                        # === ARQUETIPO 2: CIENCIAS EXACTAS ===
                        # Fuente: Contenido Real. Visualización: NINGUNA (Solo preguntas).
                        log_assessment_task_event(assessment_id, "ARQUETIPO CIENCIAS: Usando contenido real. UI limpia.")
                        prompt_source_text = filtered_source_memory
                        # db_reading_stimulus se mantiene VACÍO para que no salga el botón

                    else:
                        # === ARQUETIPO 3: HUMANIDADES Y OTRAS ===
                        # Fuente: Contenido Real. Visualización: NINGUNA (Solo preguntas).
                        log_assessment_task_event(assessment_id, "ARQUETIPO HUMANIDADES: Usando contenido real. UI limpia.")
                        prompt_source_text = filtered_source_memory
                        # db_reading_stimulus se mantiene VACÍO para que no salga el botón
                        
                        if not prompt_source_text or len(prompt_source_text) < 50:
                            prompt_source_text = full_content # Fallback técnico

                    # Persistencia diferenciada
                    with transaction.atomic():
                        aa = Assessment.objects.select_for_update().get(pk=assessment_id)
                        aa.reading_stimulus = db_reading_stimulus       # Solo tendrá datos en IDIOMAS
                        aa.listening_transcript = db_listening_transcript # Solo tendrá datos en IDIOMAS
                        aa.status = Assessment.AssessmentStatus.PROCESSING
                        aa.save(update_fields=['reading_stimulus', 'listening_transcript', 'status'])
                    
                    # Pasamos el texto fuente correcto al siguiente paso vía atributo temporal del objeto (hack de memoria)
                    # o simplemente confiamos en que 'prompt_source_text' está disponible en el scope local para el paso 2
                    # ya que estamos dentro del mismo 'while'.
                    r_text = prompt_source_text 
                    l_text = db_listening_transcript
                    
                    step = 2'''

with open("/home/MiguelAeTxio/SWAP/tasks.py.prop", "r", encoding="utf-8") as f:
    content = f.read()

# Buscamos el bloque "elif step == 1:" existente y lo reemplazamos completo
# El bloque anterior terminaba justo antes de "elif step == 2:"
pattern = re.compile(r'elif step == 1:.*?step = 2', re.DOTALL)

match = pattern.search(content)
if match:
    content = content.replace(match.group(0), NEW_LOGIC_STEP_1)
else:
    print("No se encontró el bloque step 1 para reemplazar")

with open("/home/MiguelAeTxio/SWAP/tasks.py.prop", "w", encoding="utf-8") as f:
    f.write(content)
