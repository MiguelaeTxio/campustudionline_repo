import re

with open("/home/MiguelAeTxio/SWAP/tasks_atomic.py.prop", "r") as f:
    content = f.read()

# Sustituir el bloque del Paso 2 por el Bucle Atómico Real
old_step_2_pattern = r"# --- PASO 2: GENERACIÓN DE EXAMEN.*?step = 3"
new_step_2_logic = """# --- PASO 2: GENERACIÓN DE EXAMEN (FLUJO ATÓMICO 1:1) ---
                elif step == 2:
                    log_assessment_task_event(assessment_id, f"PASO 2 (Generación Atómica) - {subject_type}")
                    
                    # 1. Fase A: Crear el esqueleto determinista en la base de datos
                    _create_assessment_skeleton(assessment)
                    questions = assessment.questions.all().order_by('id')
                    
                    # 2. Fase B: Bucle de llamadas a la API (Una por cada pregunta)
                    for idx, q_obj in enumerate(questions, 1):
                        log_assessment_task_event(assessment_id, f"Generando Ítem {idx}/{len(questions)} (ID: {q_obj.id})...")
                        
                        if subject_type == "CEFR_LANGUAGES":
                            from core.services.assessment_strategies.languages_strategy import generate_languages_item_prompt, get_language_config
                            cfg = get_language_config(subject_name)
                            lvl = assessment.prompt_data.get('cefr_level', 'B1')
                            prompt = generate_languages_item_prompt(r_text_memory, l_text_memory, lvl, cfg['lang'], q_obj)
                        else:
                            # Otros arquetipos aún no migrados al flujo 1:1
                            continue

                        # Llamada individual
                        success, resp, _ = generate_text_content(prompt, api_key=api_key)
                        
                        if success:
                            data_list = _parse_assessment_text(resp)
                            if data_list and len(data_list) > 0:
                                data = data_list[0]
                                q_obj.question_text = data.get('question_text', q_obj.question_text)
                                q_obj.options = data.get('options', [])
                                q_obj.model_answer = data.get('model_answer', q_obj.model_answer)
                                # [REPARACIÓN CLOZE] Asegurar token si la IA falla
                                if q_obj.is_cloze and '[...]' not in q_obj.question_text:
                                    q_obj.question_text += " [...]"
                                q_obj.save()
                                
                                assessment.questions_processed = idx
                                assessment.save(update_fields=['questions_processed'])
                            
                            time.sleep(1) # Pausa de seguridad para la cuota
                        else:
                            raise ResourceExhausted(f"Error en ítem {idx}: {resp}")

                    step = 3"""

content = re.sub(old_step_2_pattern, new_step_2_logic, content, flags=re.DOTALL)

with open("/home/MiguelAeTxio/SWAP/tasks_atomic.py.prop", "w") as f:
    f.write(content)
