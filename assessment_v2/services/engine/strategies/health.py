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
            if student_input == correct_answer:
                return Decimal('1.0'), {"status": "CORRECT"}
            elif not student_input:
                return Decimal('0.0'), {"status": "OMITTED"}
            else:
                # Higher penalty in Health (especially in ROT)
                num_options = len(item.content.get('options', []))
                penalty_base = Decimal('1.0') / Decimal(str(num_options - 1)) if num_options > 1 else Decimal('0.5')
                
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

        return Decimal('0.0'), {"status": "PENDING"}

    def get_system_prompt(self):
        """
        Generates clinical role based on Sub-Archetype (V06DOC_SUBARCHETYPES).
        """
        roles = {
            'SUB-SAN-MED': "Rol: Facultativo Especialista (UGR). Foco: Diagnóstico Diferencial, Fisiopatología.",
            'SUB-SAN-CUID': "Rol: Enfermero/a Clínico (NANDA). Foco: Planes de cuidados, Seguridad, Técnica.",
            'SUB-SAN-BIO': "Rol: Especialista en Laboratorio/Bioquímica. Foco: Farmacología, Analítica, Método.",
            'SUB-SAN-PSY': "Rol: Psicólogo/a Clínico (DSM-5). Foco: Evaluación conductual, Psicometría.",
            'SUB-SAN-VET': "Rol: Cirujano Veterinario. Foco: Patología comparada, Zoonosis, Clínica animal."
        }
        base_role = roles.get(self.sub_archetype_id, "Rol: Evaluador Clínico ECOE.")

        itin_ctx = ""
        if self.itinerary_id == 'ITIN_ROT':
            itin_ctx = "CONTEXTO ROTATORIO: Tolerancia CERO a errores de seguridad. Activa KILL_SWITCH en pasos críticos."

        return f"{base_role}\n{itin_ctx}\nUsa bloques CDS-KILL para protocolos obligatorios y ILC-CONTEXT para interpretación de pruebas (Analíticas/Rayos X)."

    def get_user_prompt(self, context_text, topic):
        """
        ECOE generation instruction.
        """
        return (
            f"GENERATE HEALTH EXAM (ECOE MODEL).\n"
            f"TOPIC: {topic}\n"
            f"REF: {context_text[:50000]}\n"
            f"SUB-ARCH: {self.sub_archetype_id}. ITIN: {self.itinerary_id}.\n"
            f"RULES:\n"
            f"1. Create a clinical case with Anamnesis, Procedure, and Ethics.\n"
            f"2. Include at least one CDS-KILL block with kill_switch: True for a vital safety step.\n"
            f"3. Use W-CLIN-SCAN for items requiring diagnostic imaging interpretation."
        )

    def get_output_schema(self):
        """
        Full ECOE JSON Contract.
        """
        return {
            "subdivision_sequence": [
                {
                    "subdivision_id": "SD_FACT | SD_PROC | SD_ETHI",
                    "title": "string",
                    "items": [
                        {
                            "block_type": "CDS-KILL | PRM-STRIKE | ILC-CONTEXT",
                            "widget_id": "W-PROC-ACTION | W-OBJ-STRIKE | W-CLIN-SCAN",
                            "content": {
                                "stem": "string",
                                "options": "list (for PRM)",
                                "media_assets": ["urls"]
                            },
                            "grading_logic": {
                                "correct_answer": "any",
                                "kill_switch": True,
                                "penalty_factor": 0.5,
                                "keywords": ["diagnostic", "terms"]
                            },
                            "metadata": {
                                "competency_tag": "COMP_ESP | COMP_PROF",
                                "cognitive_tag": "COG_APP | COG_ANA | COG_EVAL"
                            }
                        }
                    ]
                }
            ]
        }

    def generate_structure(self, exam_uuid, sub_archetype_id='SUB-SAN-MED'):
        """
        ECOE Stations (V06DOC_SUBDIVISIONS Group C).
        """
        contract = self.generate_contract_skeleton(exam_uuid, 'ARCH_HEALTH', sub_archetype_id)
        contract["subdivision_sequence"] = [
            {"subdivision_id": "SD_FACT", "title": "Estación 1: Anamnesis y Hechos", "items": []},
            {"subdivision_id": "SD_PROC", "title": "Estación 2: Procedimiento Clínico", "items": []},
            {"subdivision_id": "SD_ETHI", "title": "Estación 3: Juicio Ético y Seguridad", "items": []}
        ]
        return contract
