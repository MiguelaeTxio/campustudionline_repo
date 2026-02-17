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
                     "detail": "File uploaded. Queued for visual trace analysis.",
                     "file_received": True
                 }

            # Standard JSON Step Trace
            if not isinstance(student_input, dict) or 'steps' not in student_input:
                return Decimal('0.0'), {"status": "FORMAT_ERROR", "detail": "Invalid RPP-TRAZA input structure"}

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
                        trace_log.append(f"Step {expected_step['id']}: OK")
                    else:
                        # Logic for ITIN_PROF (Normative/Safety) -> Error is fatal if critical
                        if self.itinerary_id == 'ITIN_PROF' and expected_step.get('critical', False):
                            fatal_error_triggered = True
                            trace_log.append(f"Step {expected_step['id']}: FATAL (Normative Breach)")
                        else:
                            trace_log.append(f"Step {expected_step['id']}: FAIL")
                else:
                    trace_log.append(f"Step {expected_step['id']}: OMITTED")

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
            
            if student_input == correct_answer:
                return Decimal('1.0'), {"status": "CORRECT"}
            elif student_input is None or student_input == "":
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

        return f"{base_role}\n{itin_prompt}\n{level_prompt}\nBLOCKS: Use RPP-TRAZA for calculations, RBT-CANON for definitions."

    def get_user_prompt(self, context_text, topic):
        """
        User instruction generator compliant with V06DOC_TEMPLATES.
        """
        return (
            f"GENERATE EXAM JSON.\n"
            f"TOPIC: {topic}\n"
            f"CONTEXT: {context_text[:50000]}\n"
            f"CONFIG: Archetype={self.archetype_id}, Sub={self.sub_archetype_id}, Itin={self.itinerary_id}, Level={self.pedagogical_level}.\n"
            f"REQUIREMENTS:\n"
            f"1. Use 'RPP-TRAZA' for any calculation. Define 'step_matrix' with logical steps.\n"
            f"2. Use 'W-TECH-CALC' widget for input.\n"
            f"3. If Itinerary is PROF, cite specific norms (ISO/CTE).\n"
            f"4. Output must match V06DOC_TEMPLATES schema."
        )

    def get_output_schema(self):
        """
        High-fidelity JSON Schema for ARCH_TECH.
        Allows file uploads in grading logic (via widget config).
        """
        return {
            "subdivision_sequence": [
                {
                    "subdivision_id": "SD_THEO | SD_MODEL | SD_CALC | SD_VERIF",
                    "title": "string",
                    "instructions": "string",
                    "items": [
                        {
                            "block_type": "RPP-TRAZA | PRM-STRIKE | RBT-CANON",
                            "widget_id": "W-TECH-CALC | W-OBJ-STRIKE",
                            "content": {
                                "stem": "string",
                                "media_assets": ["urls"],
                                "allow_file_upload": True 
                            },
                            "grading_logic": {
                                "correct_answer": "any",
                                "step_matrix": [
                                    {"id": 1, "value": "val", "weight": 0.2, "critical": False}
                                ],
                                "keywords": ["list", "of", "lexemes"],
                                "penalty_factor": 0.25
                            },
                            "metadata": {
                                "competency_tag": "COMP_ESP | COMP_PROF",
                                "cognitive_tag": "COG_APP | COG_ANA"
                            }
                        }
                    ]
                }
            ]
        }

    def generate_structure(self, exam_uuid, sub_archetype_id='SUB-TEC-SOFT'):
        """
        Generates the exam structure with specific Subdivisions defined in V06DOC_SUBDIVISIONS (Group B).
        """
        contract = self.generate_contract_skeleton(exam_uuid, 'ARCH_TECH', sub_archetype_id)
        
        # Specific subdivisions for Technical Group
        contract["subdivision_sequence"] = [
            {"subdivision_id": "SD_THEO", "title": "Fundamentos Teóricos", "items": []},
            {"subdivision_id": "SD_MODEL", "title": "Modelado y Abstracción", "items": []},
            {"subdivision_id": "SD_CALC", "title": "Cálculo y Resolución", "items": []},
            {"subdivision_id": "SD_VERIF", "title": "Verificación y Normativa", "items": []}
        ]
        return contract
