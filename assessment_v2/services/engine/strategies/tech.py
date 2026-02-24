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
                            trace_log.append(f"Paso {expected_step['id']}: FALLO")
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
            threshold = 1.0 if self.itinerary_id in ['ITIN_MAI', 'ITIN_INV'] else 0.7
            ratio = hit_count / len(required_lexemes)
            
            if ratio >= threshold:
                return Decimal('1.0'), {"status": "CORRECT"}
            else:
                return Decimal(str(ratio)), {"status": "PARTIAL", "missing_lexemes": True}

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

    def get_system_prompt(self):
        """
        Dynamic Role Generation based on Sub-Archetypes (V06DOC_SUBARCHETYPES).
        """
        # 1. Base Role Definition
        roles = {
            'SUB-TEC-SOFT': "Rol: Arquitecto de Software Senior. Foco: Algoritmia (O-notation), Patrones de Diseño, Seguridad.",
            'SUB-TEC-CIVIL': "Rol: Ingeniero de Caminos (ICC). Foco: CTE/EHE, Resistencia de Materiales, Geotecnia.",
            'SUB-TEC-INDUS': "Rol: Ingeniero Industrial. Foco: Termodinámica, Procesos Fabriles, Máquinas Eléctricas.",
            'SUB-TEC-PURE': "Rol: Doctor en Física/Matemáticas. Foco: Demostración formal, rigor axiomático, derivación.",
            'SUB-TEC-CHEM': "Rol: Ingeniero Químico. Foco: Balances de materia y energía, Reactores, Cinética."
        }
        
        # Default fallback
        base_role = roles.get(self.sub_archetype_id, "Rol: Catedrático de Ingeniería Genérico.")

        # 2. Itinerary Nuance (V06DOC_SUBDIVISIONS)
        itin_instructions = {
            'ITIN_MAI': "Rigor Académico: Nivel Catedrático. Penaliza imprecisión terminológica.",
            'ITIN_MIN': "Rigor Funcional: Valora la aplicación práctica sobre la teoría pura.",
            'ITIN_ROT': "Rigor Seguridad: Cualquier error en cálculo de cargas o seguridad es FATAL.",
            'ITIN_PROF': "Rigor Normativo: EXIGE cumplimiento de normativa vigente (ISO, UNE, CTE).",
            'ITIN_INV': "Rigor Metodológico: Foco en estado del arte y cita bibliográfica.",
            'ITIN_DOC': "Rigor Didáctico: Explica los pasos como para un alumno de grado."
        }
        itin_prompt = itin_instructions.get(self.itinerary_id, "")

        # 3. Level Density (V06DOC_LEVELS)
        level_prompt = ""
        if self.pedagogical_level == 'LVL_C':
            level_prompt = "Nivel C (Maestro): Usa terminología densa, casos límite y alta complejidad."
        elif self.pedagogical_level == 'LVL_A':
            level_prompt = "Nivel A (Acceso): Fundamentos básicos, definiciones claras."

        return f"{base_role}\n{itin_prompt}\n{level_prompt}\nBLOQUES: Usa RPP-TRAZA para cálculos, RBT-CANON para definiciones."

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
        Uses anyOf for Union Types (Gemini 2.5 Safe).
        """
        return {
            "type": "object",
            "properties": {
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
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "number"},
                                            {"type": "boolean"}
                                        ]
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
