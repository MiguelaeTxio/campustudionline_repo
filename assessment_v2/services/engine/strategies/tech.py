# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/tech.py
from .base import BaseExamStrategy
from decimal import Decimal
import json
import re

class TechnicalStrategy(BaseExamStrategy):
    """
    Strategy for Technical Sciences and Engineering (ARCH_TECH).
    Fully compliant with V06DOC_ARCHETYPES, V06DOC_BLOCKS, and V06DOC_SUBARCHETYPES.
    
    COVERS:
    - 5 Sub-archetypes (SOFT, CIVIL, INDUS, PURE, CHEM).
    - 6 Itineraries (Including Normative PROF and Methodological INV).
    - 3 Pedagogical Levels (A, B, C).
    - Engines: RPP-TRAZA, PRM-STRIKE, RBT-CANON.
    - Widgets: W-TECH-CALC, W-OBJ-STRIKE.
    """

    def grade_item(self, item, student_input):
        """
        Grades technical items following V06DOC_BLOCKS logic strictly.
        Handles file uploads and complex structures.
        """
        logic = item.grading_logic
        block_type = item.block_type
        
        # --- MOTOR 1: RPP-TRAZA (Resolución Procedimental) ---
        # Ref: V06DOC_BLOCKS Section 1
        if block_type == 'RPP-TRAZA':
            # Support for File Uploads in procedural answers
            if isinstance(student_input, dict) and 'file_url' in student_input:
                 # Files require Async AI analysis (Manual/Vision API). 
                 # We mark as PENDING but acknowledge receipt.
                 return Decimal('0.0'), {
                     "status": "PENDING_AI_ANALYSIS", 
                     "detail": "Archivo subido correctamente. En cola para análisis de traza visual.",
                     "file_received": True
                 }

            # Standard JSON Step Trace
            if not isinstance(student_input, dict) or 'steps' not in student_input:
                return Decimal('0.0'), {"status": "FORMAT_ERROR", "detail": "Estructura de entrada RPP-TRAZA inválida."}

            step_matrix = logic.get('step_matrix', [])
            total_weight = Decimal('0.0')
            earned_score = Decimal('0.0')
            trace_log = []
            fatal_error_triggered = False

            for expected_step in step_matrix:
                step_weight = Decimal(str(expected_step.get('weight', 0.1)))
                total_weight += step_weight
                
                # Match step by ID
                student_step = next((s for s in student_input['steps'] if s.get('id') == expected_step.get('id')), None)
                
                if student_step:
                    step_val = student_step.get('value', '')
                    expected_val = expected_step.get('value', '')
                    
                    # Fuzzy match for numbers/formulas
                    if self._validate_technical_value(step_val, expected_val):
                        earned_score += step_weight
                        trace_log.append(f"Paso {expected_step['id']}: OK")
                    else:
                        # Logic for ITIN_PROF (Normative/Safety) -> Error is fatal if critical
                        if self.itinerary_id == 'ITIN_PROF' and expected_step.get('critical', False):
                            fatal_error_triggered = True
                            trace_log.append(f"Paso {expected_step['id']}: FATAL (Incumplimiento Normativo)")
                        else:
                            # [HITO 6 FIX] Lógica de Arrastre de Error / Inferencia (Incidencia 14)
                            trace_log.append(f"Paso {expected_step['id']}: DISCREPANCIA (Posible Arrastre de Error)")
                            return Decimal('0.0'), {
                                "status": "PENDING_AI_INFERENCE",
                                "detail": f"Fallo en paso {expected_step['id']}. Se requiere IA para validar inferencia lógica.",
                                "trace": trace_log
                            }
                else:
                    trace_log.append(f"Paso {expected_step['id']}: OMITIDO")

            if fatal_error_triggered:
                return Decimal('0.0'), {"status": "FATAL_ERROR", "trace": trace_log, "feedback_category": "FB_SAFETY"}

            # Normalize Score
            final_score = (earned_score / total_weight) if total_weight > 0 else Decimal('0.0')
            
            # Apply Level Rigor (V06DOC_LEVELS)
            if self.pedagogical_level == 'LVL_C': 
                # Level C requires perfect trace, partial errors penalized heavily
                if final_score < Decimal('1.0'):
                    final_score = final_score * Decimal('0.9')

            return final_score, {"status": "GRADED", "trace": trace_log}

        # --- MOTOR 2: PRM-STRIKE (Penalización UGR) ---
        # Ref: V06DOC_BLOCKS Section 1 - Formula [A - E/(N-1)]
        elif block_type == 'PRM-STRIKE':
            correct_answer = logic.get('correct_answer')
            num_options = len(item.content.get('options', []))
            
            if str(student_input).strip() == str(correct_answer).strip():
                return Decimal('1.0'), {"status": "CORRECT"}
            elif student_input is None or str(student_input).strip() == "":
                return Decimal('0.0'), {"status": "OMITTED"}
            else:
                # UGR Formula
                if num_options > 1:
                    penalty = Decimal('1.0') / Decimal(str(num_options - 1))
                else:
                    penalty = Decimal('0.5')
                
                return -penalty, {
                    "status": "INCORRECT", 
                    "penalty_applied": float(penalty), 
                    "formula": "1/(N-1)"
                }

        # --- MOTOR 3: RBT-CANON (Terminología Precisa) ---
        # Ref: V06DOC_BLOCKS Section 1
        elif block_type == 'RBT-CANON':
            required_lexemes = logic.get('keywords', [])
            student_text = str(student_input).lower()
            
            hit_count = 0
            for lexeme in required_lexemes:
                if re.search(r'\b' + re.escape(lexeme.lower()) + r'\b', student_text):
                    hit_count += 1
            
            if not required_lexemes:
                return Decimal('1.0'), {"status": "MANUAL_REVIEW"}

            # Strictness based on Itinerary
            # [HITO 6 FIX] Rigor estricto para Nivel C y Especializados (Incidencia 13)
            if self.pedagogical_level == 'LVL_C' or self.itinerary_id in ['ITIN_MAI', 'ITIN_INV']:
                threshold = 1.0
            else:
                threshold = 0.7
            ratio = hit_count / len(required_lexemes)
            
            if ratio >= threshold:
                return Decimal('1.0'), {"status": "CORRECT"}
            else:
                return Decimal(str(ratio)), {"status": "PARTIAL", "missing_lexemes": True}

        # --- MOTOR 4: DEMO-PROOF (Demostración Formal) ---
        # Used in SUB-TEC-PURE. Requires logical axiom validation.
        # Usado en SUB-TEC-PURE. Requiere validación de axiomas lógicos.
        elif block_type == 'DEMO-PROOF':
            required_axioms = logic.get('required_axioms', [])
            forbidden_fallacies = logic.get('forbidden_fallacies', [])
            student_text = str(student_input).lower()
            
            # Check for logical fallacies first
            for fallacy in forbidden_fallacies:
                if fallacy.lower() in student_text:
                    return Decimal('0.0'), {
                        "status": "LOGICAL_FALLACY", 
                        "detail": f"Falacia detectada: {fallacy}",
                        "feedback_category": "FB_CONCEPT"
                    }

            # Check coverage of axioms
            hits = sum(1 for ax in required_axioms if ax.lower() in student_text)
            
            if not required_axioms:
                return Decimal('1.0'), {"status": "MANUAL_REVIEW"}
            
            # Rigor: Demostrations require 100% coherence in Pure Sciences
            if self.sub_archetype_id == 'SUB-TEC-PURE' and hits < len(required_axioms):
                 return Decimal('0.4'), {
                     "status": "INCOMPLETE_PROOF", 
                     "detail": "La demostración carece de pasos intermedios obligatorios.",
                     "missing_axioms": len(required_axioms) - hits
                 }
            
            score = Decimal(str(hits / len(required_axioms)))
            return score, {"status": "GRADED", "axioms_verified": hits}

        # --- MOTOR 5: BLUEPRINT-DESIGN (Diseño de Planos/Esquemas) ---
        # Used in SUB-TEC-PROJ / CONS.
        elif block_type == 'BLUEPRINT-DESIGN':
            # Input expected: JSON with specific technical elements
            if not isinstance(student_input, dict):
                 return Decimal('0.0'), {"status": "FORMAT_ERROR"}
            
            required_elements = logic.get('required_elements', [])
            safety_constraints = logic.get('safety_constraints', []) # e.g., "min_pillar_width"
            
            student_elements = student_input.get('elements', [])
            
            # 1. Safety Check (Critical for Architecture/Engineering)
            for constraint in safety_constraints:
                param = constraint.get('param')
                min_val = float(constraint.get('min_value', 0))
                # Check if any element violates this
                for elem in student_elements:
                    if elem.get('type') == param and float(elem.get('value', 0)) < min_val:
                        return Decimal('0.0'), {
                            "status": "SAFETY_VIOLATION",
                            "detail": f"Elemento {param} incumple normativa de seguridad (Valor < {min_val}).",
                            "feedback_category": "FB_SAFETY"
                        }

            # 2. Element Presence Check
            found_count = 0
            student_elem_types = [e.get('type') for e in student_elements]
            for req in required_elements:
                if req in student_elem_types:
                    found_count += 1
            
            score = Decimal(str(found_count / len(required_elements))) if required_elements else Decimal('1.0')
            return score, {"status": "GRADED", "elements_found": found_count}

        return Decimal('0.0'), {"status": "PENDING"}

    def _validate_technical_value(self, input_val, expected_val):
        """Helper to validate numeric or string values with tolerance."""
        try:
            # Try numeric comparison with tolerance
            f_in = float(input_val)
            f_ex = float(expected_val)
            return abs(f_in - f_ex) < 0.01  # 1% tolerance standard
        except (ValueError, TypeError):
            # String comparison
            return str(input_val).strip().lower() == str(expected_val).strip().lower()

    def get_section_plan(self):
        """
        Returns the mandatory section list for the orchestrator to build the DB skeleton.
        Ref: V06DOC_ARCHETYPES.
        ---
        Devuelve la lista mandatoria de secciones para que el orquestador construya el esqueleto en la BBDD.
        Ref: V06DOC_ARCHETYPES.
        """
        return [
            {"subdivision_id": "SD_THEO", "title": "Fundamentos Teóricos", "instructions": "Demuestra tu dominio de los principios y leyes fundamentales.", "time_limit": 600},
            {"subdivision_id": "SD_MODEL", "title": "Modelado y Abstracción", "instructions": "Formaliza el problema planteado en lenguaje matemático o lógico.", "time_limit": 900},
            {"subdivision_id": "SD_CALC", "title": "Cálculo y Resolución", "instructions": "Desarrolla la solución paso a paso. Se evalúa la traza procedimental.", "time_limit": 1200},
            {"subdivision_id": "SD_VERIF", "title": "Verificación y Normativa", "instructions": "Comprueba la coherencia de los resultados y su adecuación a la norma.", "time_limit": 600}
        ]

    def get_exam_skeleton(self):
        """
        Returns the structural skeleton for the 7 Technical models.
        Ref: V06DOC_SUBARCHETYPES V5.0.
        """
        sid = self.sub_archetype_id
        skeleton = []

        # 1. SUB-TEC-SOFT: Informática (Modelo Algorítmico)
        if sid == 'SUB-TEC-SOFT':
            skeleton = [
                {"subdivision_id": "SD_ALGO", "title": "Algoritmia y Lógica", "instructions": "Implemente o analice la complejidad del algoritmo.", "layout_mode": "STANDARD", "items": [{"block_type": "RPP-TRAZA", "widget_id": "W-TECH-CALC"}]},
                {"subdivision_id": "SD_DEBUG", "title": "Depuración y Optimización", "instructions": "Identifique el error lógico o mejore el rendimiento.", "layout_mode": "STANDARD", "items": [{"block_type": "RPP-TRAZA", "widget_id": "W-TECH-CALC"}]}
            ]
        # 2. SUB-TEC-CIVIL: Caminos (Modelo Normativo)
        elif sid == 'SUB-TEC-CIVIL':
            skeleton = [
                {"subdivision_id": "SD_STRUCT", "title": "Cálculo de Estructuras", "instructions": "Calcule las reacciones y esfuerzos.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "RPP-TRAZA", "widget_id": "W-TECH-CALC"}]},
                {"subdivision_id": "SD_NORM", "title": "Cumplimiento Normativo", "instructions": "Verifique la adecuación al CTE/EHE.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE"}]}
            ]
        # 3. SUB-TEC-INDUS: Industrial (Termo-Mecánico)
        elif sid == 'SUB-TEC-INDUS':
            skeleton = [
                {"subdivision_id": "SD_THERMO", "title": "Termodinámica y Fluidos", "instructions": "Realice el balance energético del ciclo.", "layout_mode": "STANDARD", "items": [{"block_type": "RPP-TRAZA", "widget_id": "W-TECH-CALC"}]},
                {"subdivision_id": "SD_MECH", "title": "Mecanismos y Máquinas", "instructions": "Analice la cinemática o eficiencia del sistema.", "layout_mode": "STANDARD", "items": [{"block_type": "RPP-TRAZA", "widget_id": "W-TECH-CALC"}]}
            ]
        # 4. SUB-TEC-CHEM: Ing. Química (Reactores)
        elif sid == 'SUB-TEC-CHEM':
            skeleton = [
                {"subdivision_id": "SD_REACT", "title": "Diseño de Reactores", "instructions": "Determine el volumen o conversión del reactor.", "layout_mode": "STANDARD", "items": [{"block_type": "RPP-TRAZA", "widget_id": "W-TECH-CALC"}]},
                {"subdivision_id": "SD_MASS_BAL", "title": "Balances de Materia", "instructions": "Calcule los flujos de entrada y salida.", "layout_mode": "STANDARD", "items": [{"block_type": "RPP-TRAZA", "widget_id": "W-TECH-CALC"}]}
            ]
        # 5. SUB-TEC-PROJ: Arquitectura (Modelo Proyectual)
        elif sid == 'SUB-TEC-PROJ':
            skeleton = [
                {"subdivision_id": "SD_SITE", "title": "Análisis de Sitio y Contexto", "instructions": "Analice las condicionantes urbanas e históricas.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "RBT-CANON", "widget_id": "W-OBJ-STRIKE"}]},
                {"subdivision_id": "SD_COMP", "title": "Composición y Diseño", "instructions": "Justifique la solución formal y funcional.", "layout_mode": "STANDARD", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT"}]}
            ]
        # 6. SUB-TEC-CONS: Edificación (Modelo Constructivo)
        elif sid == 'SUB-TEC-CONS':
            skeleton = [
                {"subdivision_id": "SD_TECH", "title": "Detalle Constructivo", "instructions": "Identifique los elementos del sistema constructivo.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE"}]},
                {"subdivision_id": "SD_MGMT", "title": "Gestión y Seguridad de Obra", "instructions": "Valore los riesgos y la ejecución técnica.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE"}]}
            ]
        # 7. SUB-TEC-PURE: Ciencias Puras (Modelo Demostrativo)
        elif sid == 'SUB-TEC-PURE':
            skeleton = [
                {"subdivision_id": "SD_AXIOM", "title": "Axiomas y Definiciones", "instructions": "Enuncie los principios fundamentales.", "layout_mode": "STANDARD", "items": [{"block_type": "RBT-CANON", "widget_id": "W-OBJ-STRIKE"}]},
                {"subdivision_id": "SD_PROOF", "title": "Demostración Formal", "instructions": "Desarrolle la derivación lógica completa.", "layout_mode": "STANDARD", "items": [{"block_type": "RPP-TRAZA", "widget_id": "W-TECH-CALC"}]}
            ]
        else:
            skeleton = [
                {"subdivision_id": "SD_GEN", "title": "Problema Técnico General", "instructions": "Resuelva el supuesto planteado.", "layout_mode": "STANDARD", "items": [{"block_type": "RPP-TRAZA", "widget_id": "W-TECH-CALC"}]}
            ]

        return skeleton


    def get_system_prompt(self):
        """
        Generates technical role based on the 7 Technical Sub-Archetypes (V5.0).
        ---
        Genera el rol técnico basado en los 7 Sub-Arquetipos Técnicos (V5.0).
        """
        roles = {
            'SUB-TEC-SOFT': "Rol: Arquitecto de Software Senior. Foco: Algoritmia, Estructuras de Datos y Arquitectura.",
            'SUB-TEC-CIVIL': "Rol: Ingeniero de Caminos (ICC). Foco: Cálculo de Estructuras y Normativa Técnica (CTE).",
            'SUB-TEC-INDUS': "Rol: Ingeniero Industrial. Foco: Termodinámica, Máquinas y Procesos Industriales.",
            'SUB-TEC-CHEM': "Rol: Ingeniero Químico. Foco: Reactores y Balances de Materia/Energía.",
            'SUB-TEC-PROJ': "Rol: Arquitecto Proyectista. Foco: Composición, Proyecto y Análisis Urbano.",
            'SUB-TEC-CONS': "Rol: Arquitecto Técnico / Ing. Edificación. Foco: Técnica Constructiva y Gestión de Obra.",
            'SUB-TEC-PURE': "Rol: Doctor en Ciencias Puras (Física/Mates). Foco: Rigor Deductivo y Demostración."
        }
        base_role = roles.get(self.sub_archetype_id, "Rol: Catedrático de Ingeniería.")
        
        itin_prompt = ""
        if self.itinerary_id == 'ITIN_PROF':
            itin_prompt = "CONTEXTO PROFESIONAL: Exige cumplimiento estricto de reglamentación técnica."
        
        return f"""{base_role}
{itin_prompt}
REGLA: Usa RPP-TRAZA para cálculos y RBT-CANON para definiciones técnicas."""
    def get_user_prompt(self, context_text, topic, subdivision_id, generated_item_titles=None):
        """
        Generates the user prompt injecting the study material context (ATOMIC).
        ---
        Genera el prompt de usuario inyectando el contexto del material de estudio (ATÓMICO).
        """
        memory = f"\nEvita repetir estos conceptos ya generados: {', '.join(generated_item_titles)}" if generated_item_titles else ""
        return (
            f"GENERA 3 ÍTEMS para la sección: {subdivision_id}.\n"
            f"TEMA: {topic}. {memory}\n"
            f"CONTEXTO: {context_text[:50000]}\n"
            f"CONFIG: Sub={self.sub_archetype_id}, Itin={self.itinerary_id}, Level={self.pedagogical_level}.\n"
            f"REQUISITOS:\n"
            f"1. Para la fase {subdivision_id}, utiliza el bloque más adecuado (RPP-TRAZA para cálculo o PRM-STRIKE para teoría).\n"
            f"2. Salida estrictamente JSON (Array 'items')."
        )

    def get_output_schema(self):
        """
        Defines the expected JSON schema for the AI model response (ATOMIC).
        ---
        Define el esquema JSON esperado para la respuesta del modelo de IA (ATÓMICO).
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
                            "block_type": {"type": "string", "enum": ["RPP-TRAZA", "PRM-STRIKE", "RBT-CANON"]},
                            "widget_id": {"type": "string", "enum": ["W-TECH-CALC", "W-OBJ-STRIKE"]},
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
                                        "anyOf": [{"type": "string"}, {"type": "number"}, {"type": "boolean"}]
                                    },
                                    "step_matrix": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "integer"},
                                                "value": {"type": "string"},
                                                "weight": {"type": "number"},
                                                "critical": {"type": "boolean"}
                                            },
                                            "required": ["id", "value"]
                                        }
                                    }
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
                        "required": ["block_type", "widget_id", "content", "grading_logic", "metadata"]
                    }
                }
            },
            "required": ["items"]
        }
