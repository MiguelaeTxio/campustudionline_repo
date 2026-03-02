# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/health.py
from .base import BaseExamStrategy
from decimal import Decimal
import json

class HealthStrategy(BaseExamStrategy):
    """
    Exam strategy for Health Sciences (ARCH_HEALTH).
    Fully compliant with ECOE model and V06DOC_SUBARCHETYPES.
    
    COVERS:
    - 5 Sub-archetypes (MED, CUID, BIO, PSY, VET).
    - Blocks: CDS-KILL (Fatal), PRM-STRIKE, ILC-CONTEXT.
    - Itineraries: ROT (Rotatorio - Strict Safety), MAI, MIN.
    - Widgets: W-PROC-ACTION, W-CLIN-SCAN, W-OBJ-STRIKE.
    """

    def grade_item(self, item, student_input):
        """
        Grades health items following V06DOC_BLOCKS.
        Prioritizes patient safety (KILL_SWITCH).
        """
        logic = item.grading_logic
        block_type = item.block_type
        
        # --- MOTOR 1: CDS-KILL (Checklist Dicotómico de Seguridad) ---
        # Ref: V06DOC_BLOCKS Section 2
        if block_type == 'CDS-KILL':
            # Expected input: bool or {"checked": bool}
            is_performed = student_input is True or (isinstance(student_input, dict) and student_input.get('checked'))
            correct_state = logic.get('correct_answer', True)

            if is_performed == correct_state:
                return Decimal('1.0'), {"status": "CORRECT", "safety": "SECURE"}
            else:
                # If the step is critical (KILL_SWITCH), score is 0 for the whole section
                if logic.get('kill_switch', False) or self.itinerary_id == 'ITIN_ROT':
                    return Decimal('0.0'), {
                        "status": "FATAL_ERROR", 
                        "kill_switch_activated": True,
                        "feedback_category": "FB_SAFETY",
                        "justification": "Violación de protocolo crítico de seguridad. El paciente está en riesgo."
                    }
                return Decimal('0.0'), {"status": "INCORRECT", "feedback_category": "FB_PROCEDURAL"}

        # --- MOTOR 2: PRM-STRIKE (Diagnóstico Diferencial) ---
        # Ref: V06DOC_BLOCKS Section 1
        elif block_type == 'PRM-STRIKE':
            correct_answer = logic.get('correct_answer')
            if str(student_input).strip() == str(correct_answer).strip():
                return Decimal('1.0'), {"status": "CORRECT"}
            elif not student_input:
                return Decimal('0.0'), {"status": "OMITTED"}
            else:
                # Higher penalty in Health (especially in ROT)
                num_options = len(item.content.get('options', []))
                penalty_base = Decimal('1.0') / Decimal(str(max(1, num_options - 1))) if num_options > 1 else Decimal('0.5')
                
                # Double penalty for wrong diagnosis in Rotatorio
                if self.itinerary_id == 'ITIN_ROT':
                    penalty_base = penalty_base * Decimal('1.5')
                
                return -penalty_base, {"status": "INCORRECT", "penalty": float(penalty_base)}

        # --- MOTOR 3: ILC-CONTEXT (Interpretación de Pruebas/Contexto) ---
        # Ref: V06DOC_BLOCKS Section 2
        elif block_type == 'ILC-CONTEXT':
            # Requires semantic comparison of diagnostic inference
            # For now, we use keyword matching + pending AI refinement
            keywords = logic.get('keywords', [])
            student_text = str(student_input).lower()
            hits = sum(1 for kw in keywords if kw.lower() in student_text)
            
            if not keywords: return Decimal('1.0'), {"status": "MANUAL_REVIEW"}
            
            score = Decimal(str(hits / len(keywords)))
            return score, {"status": "GRADED", "hits": hits}

        # --- MOTOR 4: LIKERT-SCALE (Escala de Desempeño ECOE) ---
        # Ref: V06DOC_BLOCKS Section 2 (Incidencia 38)
        elif block_type == 'LIKERT-SCALE':
            # Input esperado: Valor entero 1-5 o 0-10
            try:
                val = float(student_input)
                max_val = float(logic.get('max_scale', 5))
                min_threshold = float(logic.get('min_threshold', 3))
                
                # Normalización a 0.0 - 1.0
                normalized_score = Decimal(str(val / max_val))
                normalized_score = min(max(normalized_score, Decimal('0.0')), Decimal('1.0'))
                
                status = "COMPETENT" if val >= min_threshold else "NEEDS_IMPROVEMENT"
                
                return normalized_score, {
                    "status": status, 
                    "raw_value": val, 
                    "max_value": max_val,
                    "feedback_category": "FB_PROCEDURAL"
                }
            except (ValueError, TypeError):
                return Decimal('0.0'), {"status": "FORMAT_ERROR", "detail": "Valor de escala Likert inválido."}

        return Decimal('0.0'), {"status": "PENDING"}

    def get_section_plan(self):
        """
        Returns the mandatory section list for the orchestrator (SKELETON-FIRST).
        Ref: V06DOC_ARCHETYPES.
        """
        # Lógica de ECOE Completa para Itinerario Rotatorio (Incidencia 37)
        if self.itinerary_id == 'ITIN_ROT':
            return [
                {
                    "subdivision_id": "SD_ANAMNESIS",
                    "title": "Estación 1: Anamnesis y Entrevista",
                    "instructions": "Realice la entrevista clínica completa. Indague en antecedentes y sintomatología.",
                    "time_limit": 420 # 7 minutos estándar ECOE
                },
                {
                    "subdivision_id": "SD_EXPLORATION",
                    "title": "Estación 2: Exploración Física",
                    "instructions": "Ejecute las maniobras de exploración física pertinentes por sistemas.",
                    "time_limit": 420
                },
                {
                    "subdivision_id": "SD_TESTS",
                    "title": "Estación 3: Pruebas Complementarias",
                    "instructions": "Solicite e interprete las pruebas diagnósticas (Imagen/Lab) necesarias.",
                    "time_limit": 300 # 5 minutos
                },
                {
                    "subdivision_id": "SD_DIAG_PLAN",
                    "title": "Estación 4: Juicio Clínico y Plan",
                    "instructions": "Establezca el diagnóstico diferencial y el plan terapéutico.",
                    "time_limit": 420
                },
                {
                    "subdivision_id": "SD_COMM_ETHICS",
                    "title": "Estación 5: Comunicación y Ética",
                    "instructions": "Informe al paciente/familia y gestione aspectos bioéticos o legales.",
                    "time_limit": 300
                }
            ]
        
        # Plan estándar para Grado/Teoría (3 Fases)
        return [
            {
                "subdivision_id": "SD_FACT",
                "title": "Fase 1: Recopilación de Datos",
                "instructions": "Identifique los datos clínicos relevantes del caso.",
                "time_limit": 300
            },
            {
                "subdivision_id": "SD_CLINICAL",
                "title": "Fase 2: Razonamiento Clínico",
                "instructions": "Elabore el diagnóstico y tratamiento.",
                "time_limit": 600
            },
            {
                "subdivision_id": "SD_SAFETY",
                "title": "Fase 3: Seguridad y Normativa",
                "instructions": "Valore riesgos y cumplimiento de protocolos.",
                "time_limit": 300
            }
        ]

    def get_exam_skeleton(self):
        """
        Returns the structural skeleton for the 10 Health models.
        Ref: V06DOC_SUBARCHETYPES V5.0.
        Refactor: DRY & Prompt Binding implemented.
        """
        sid = self.sub_archetype_id
        skeleton = []

        # 1. INSTRUCCIONES CENTRALIZADAS (DRY)
        I_CLINIC_Q = "Genera una pregunta clínica de opción múltiple (4 opciones) basada en el caso o patología."
        I_IMAGE = "Describe detalladamente una prueba de imagen (RX/CT/Resonancia) o hallazgo visual en el stem para su interpretación."
        I_SAFETY = "Genera un checklist de seguridad crítico. El usuario debe marcar los pasos obligatorios para evitar riesgos."
        I_TREATMENT = "Establezca el plan terapéutico o farmacológico adecuado (4 opciones)."

        # 2. CONSTRUCCIÓN DEL ESQUELETO

        # 1. SUB-SAN-MED-CLIN: Medicina Clínica
        if sid == "SUB-SAN-MED-CLIN":
            skeleton = [
                {"subdivision_id": "SD_FACT", "title": "Anamnesis y Hechos", "instructions": "Identifique signos y síntomas clave.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": I_CLINIC_Q}]},
                {"subdivision_id": "SD_DIAG", "title": "Diagnóstico por Imagen", "instructions": "Interprete la prueba diagnóstica.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "ILC-CONTEXT", "widget_id": "W-CLIN-SCAN", "task_instruction": I_IMAGE}]},
                {"subdivision_id": "SD_THERA", "title": "Plan Terapéutico", "instructions": "Establezca el tratamiento adecuado.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": I_TREATMENT}]}
            ]
        # 2. SUB-SAN-MED-BASIC: Básicas Médicas (Anatomía/Fisio)
        elif sid == "SUB-SAN-MED-BASIC":
            skeleton = [
                {"subdivision_id": "SD_IDENT", "title": "Identificación Anatómica", "instructions": "Señale la estructura o tejido en la imagen.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "ILC-CONTEXT", "widget_id": "W-CLIN-SCAN", "task_instruction": "Describe una imagen anatómica o histológica para que el alumno identifique la estructura señalada."}]},
                {"subdivision_id": "SD_FUNC", "title": "Fisiología y Función", "instructions": "Explique el mecanismo fisiológico.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Genera una pregunta sobre mecanismos fisiológicos o función celular."}]}
            ]
        # 3. SUB-SAN-ODON: Odontología
        elif sid == "SUB-SAN-ODON":
            skeleton = [
                {"subdivision_id": "SD_IMAG", "title": "Radiología Dental", "instructions": "Identifique hallazgos en la ortopantomografía.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "ILC-CONTEXT", "widget_id": "W-CLIN-SCAN", "task_instruction": "Describe una ortopantomografía o radiografía periapical con una patología dental visible."}]},
                {"subdivision_id": "SD_PROC", "title": "Procedimiento Técnico", "instructions": "Ejecute el protocolo de intervención dental.", "layout_mode": "STANDARD", "items": [{"block_type": "CDS-KILL", "widget_id": "W-PROC-ACTION", "task_instruction": I_SAFETY}]}
            ]
        # 4. SUB-SAN-FISIO: Fisioterapia
        elif sid == "SUB-SAN-FISIO":
            skeleton = [
                {"subdivision_id": "SD_VALORATION", "title": "Valoración Funcional", "instructions": "Determine el grado de afectación funcional.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": I_CLINIC_Q}]},
                {"subdivision_id": "SD_ANAT_PALP", "title": "Anatomía Palpatoria", "instructions": "Localice el punto gatillo o estructura.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "ILC-CONTEXT", "widget_id": "W-CLIN-SCAN", "task_instruction": "Describe una zona anatómica para palpación o identificación de puntos gatillo."}]}
            ]
        # 5. SUB-SAN-CUID: Enfermería (NANDA)
        elif sid == "SUB-SAN-CUID":
            skeleton = [
                {"subdivision_id": "SD_NANDA", "title": "Planificación (NANDA)", "instructions": "Priorice los diagnósticos de enfermería.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Genera una pregunta sobre diagnósticos NANDA/NIC/NOC o priorización de cuidados."}]},
                {"subdivision_id": "SD_SAFE", "title": "Protocolo de Seguridad", "instructions": "Asegure los pasos críticos de la técnica.", "layout_mode": "STANDARD", "items": [{"block_type": "CDS-KILL", "widget_id": "W-PROC-ACTION", "task_instruction": I_SAFETY}]}
            ]
        # 6. SUB-SAN-LAB: Bioquímica/Farmacia
        elif sid == "SUB-SAN-LAB":
            skeleton = [
                {"subdivision_id": "SD_ANALYTIC", "title": "Cálculo y Analítica", "instructions": "Determine los niveles o dosis requeridas.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Genera un problema de cálculo de dosis, concentraciones o interpretación de valores analíticos."}]},
                {"subdivision_id": "SD_LAB_PROC", "title": "Procedimiento de Laboratorio", "instructions": "Ejecute el protocolo de seguridad en lab.", "layout_mode": "STANDARD", "items": [{"block_type": "CDS-KILL", "widget_id": "W-PROC-ACTION", "task_instruction": I_SAFETY}]}
            ]
        # 7. SUB-SAN-PSY-CLIN: Psicología Clínica
        elif sid == "SUB-SAN-PSY-CLIN":
            skeleton = [
                {"subdivision_id": "SD_DSM", "title": "Diagnóstico DSM/CIE", "instructions": "Categorice el trastorno según criterios.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Genera una pregunta de diagnóstico diferencial basada en criterios DSM-5/CIE-11."}]},
                {"subdivision_id": "SD_BEHAV", "title": "Análisis Conductual", "instructions": "Identifique los refuerzos y conductas.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "ILC-CONTEXT", "widget_id": "W-CLIN-SCAN", "task_instruction": "Describe un registro conductual o transcripción de sesión para análisis funcional."}]}
            ]
        # 8. SUB-SAN-PSY-EXP: Psicología Experimental
        elif sid == "SUB-SAN-PSY-EXP":
            skeleton = [
                {"subdivision_id": "SD_STATS", "title": "Análisis de Datos", "instructions": "Interprete los resultados estadísticos.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Genera una pregunta sobre interpretación de gráficas, p-valores o diseño estadístico."}]},
                {"subdivision_id": "SD_DESIGN", "title": "Diseño Experimental", "instructions": "Identifique variables y sesgos.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Genera una pregunta sobre control de variables, validez interna/externa o sesgos."}]}
            ]
        # 9. SUB-SAN-VET: Veterinaria
        elif sid == "SUB-SAN-VET":
            skeleton = [
                {"subdivision_id": "SD_CLINIC", "title": "Clínica Animal", "instructions": "Identifique la patología en el animal.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "ILC-CONTEXT", "widget_id": "W-CLIN-SCAN", "task_instruction": "Describe una imagen clínica de un animal (ej: lesión dérmica, postura) para diagnóstico."}]},
                {"subdivision_id": "SD_SURGERY", "title": "Cirugía y Anestesia", "instructions": "Verifique los puntos críticos pre-quirúrgicos.", "layout_mode": "STANDARD", "items": [{"block_type": "CDS-KILL", "widget_id": "W-PROC-ACTION", "task_instruction": I_SAFETY}]}
            ]
        # 10. SUB-SAN-NUT: Nutrición
        elif sid == "SUB-SAN-NUT":
            skeleton = [
                {"subdivision_id": "SD_DIET", "title": "Cálculo Dietético", "instructions": "Calcule el balance nutricional del caso.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Genera un problema de cálculo de aportes calóricos, macronutrientes o balance hídrico."}]},
                {"subdivision_id": "SD_BROM", "title": "Bromatología", "instructions": "Identifique componentes o contaminantes.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Genera una pregunta sobre seguridad alimentaria, etiquetado o química de alimentos."}]}
            ]
        else:
            skeleton = [
                {"subdivision_id": "SD_GEN", "title": "Evaluación de Salud General", "instructions": "Resuelva el caso clínico.", "layout_mode": "STANDARD", "items":[{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": I_CLINIC_Q}]},
                {"subdivision_id": "SD_NORM", "title": "Protocolo y Normativa", "instructions": "Encuadre en protocolo oficial.", "layout_mode": "STANDARD", "items":[{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Valore la actuación clínica según el protocolo médico oficial."}]}
            ]

        return skeleton

    def get_system_prompt(self):
        """
        Generates clinical role based on the 10 Health Sub-Archetypes (V5.0).
        """
        roles = {
            'SUB-SAN-MED-CLIN': "Rol: Facultativo Especialista (UGR). Foco: Diagnóstico Diferencial, Razonamiento Clínico.",
            'SUB-SAN-MED-BASIC': "Rol: Catedrático de Ciencias Básicas (UGR). Foco: Anatomía, Fisiología e Identificación.",
            'SUB-SAN-ODON': "Rol: Odontólogo Especialista. Foco: Técnica Dental, Materiales y Radiología.",
            'SUB-SAN-FISIO': "Rol: Fisioterapeuta Clínico. Foco: Valoración Funcional y Anatomía Palpatoria.",
            'SUB-SAN-CUID': "Rol: Enfermero/a Clínico (NANDA). Foco: Planes de cuidados, Seguridad y Protocolos.",
            'SUB-SAN-LAB': "Rol: Especialista en Laboratorio/Bioquímica. Foco: Farmacología, Analítica y Balances.",
            'SUB-SAN-PSY-CLIN': "Rol: Psicólogo Clínico. Foco: Diagnóstico DSM/CIE y Evaluación Conductual.",
            'SUB-SAN-PSY-EXP': "Rol: Investigador Experimental. Foco: Estadística, Metodología y Diseño.",
            'SUB-SAN-VET': "Rol: Cirujano Veterinario. Foco: Clínica animal, Cirugía y Zoonosis.",
            'SUB-SAN-NUT': "Rol: Dietista-Nutricionista. Foco: Bromatología, Dietética y Salud Pública."
        }
        base_role = roles.get(self.sub_archetype_id, "Rol: Evaluador de Ciencias de la Salud.")
        itin_ctx = "CONTEXTO ROTATORIO/SEGURIDAD: Tolerancia CERO. Activa KILL_SWITCH en pasos críticos." if self.itinerary_id == 'ITIN_ROT' else ""

        return f"""{base_role}
{itin_ctx}
REGLA: Usa W-CLIN-SCAN para imágenes y W-PROC-ACTION para pasos de seguridad vital."""

    def get_output_schema(self):
        """
        Atomic JSON Schema for ARCH_HEALTH.
        Uses anyOf for Union Types (Gemini 2.5 Safe).
        """
        return {
            "type": "object",
            "properties": {
                "section_stimulus": {"type": "string"},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "block_type": {"type": "string", "enum": ["CDS-KILL", "PRM-STRIKE", "ILC-CONTEXT"]},
                            "widget_id": {"type": "string", "enum": ["W-PROC-ACTION", "W-OBJ-STRIKE", "W-CLIN-SCAN"]},
                            "content": {
                                "type": "object",
                                "properties": {
                                    "stem": {"type": "string"},
                                    "options": {"type": "array", "items": {"type": "string"}},
                                    "media_assets": {"type": "array", "items": {"type": "string"}}
                                },
                                "required": ["stem"]
                            },
                            "grading_logic": {
                                "type": "object",
                                "properties": {
                                    "correct_answer": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "boolean"}
                                        ]
                                    },
                                    "kill_switch": {"type": "boolean"},
                                    "penalty_factor": {"type": "number"},
                                    "keywords": {"type": "array", "items": {"type": "string"}}
                                }
                            },
                            "metadata": {
                                "type": "object",
                                "properties": {
                                    "competency_tag": {"type": "string"},
                                    "cognitive_tag": {"type": "string"}
                                },
                                "required": ["competency_tag", "cognitive_tag"]
                            }
                        },
                        "required": ["item_id", "content", "grading_logic", "metadata"]
                    }
                }
            },
            "required": ["items"]
        }
