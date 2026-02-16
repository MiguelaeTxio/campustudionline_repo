# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/health.py
from .base import BaseExamStrategy
from decimal import Decimal
import json

class HealthStrategy(BaseExamStrategy):
    """
    Exam strategy for Health Sciences (ARCH_HEALTH).
    Implements the ECOE model with KILL_SWITCH logic for safety-critical steps.
    
    ---
    
    Estrategia de examen para Ciencias de la Salud (ARCH_HEALTH).
    Implementa el modelo ECOE con lógica KILL_SWITCH para pasos críticos de seguridad.
    """

    def grade_item(self, item, student_input):
        """
        Grades items with support for CDS-KILL and ITIN_ROT fatal errors.
        ---
        Califica ítems con soporte para errores fatales CDS-KILL e ITIN_ROT.
        """
        logic = item.grading_logic
        block_type = item.block_type
        
        # 1. Bloque de Seguridad Crítica (CDS-KILL)
        if block_type == 'CDS-KILL':
            is_correct = student_input is True or student_input == logic.get('correct_answer')
            if not is_correct and logic.get('kill_switch', False):
                # V06DOC_SUBDIVISIONS: La omisión de un paso crítico anula la sección.
                return Decimal('0.0'), {
                    "status": "FATAL_ERROR",
                    "kill_switch_activated": True,
                    "feedback_category": "FB_SAFETY",
                    "justification": "Error fatal: Violación de protocolo de seguridad crítica."
                }
            return (Decimal('1.0'), {"status": "CORRECT"}) if is_correct else (Decimal('0.0'), {"status": "INCORRECT"})

        # 2. Bloque Objetivo (PRM-STRIKE) - Adaptado a Salud
        if block_type == 'PRM-STRIKE':
            correct_answer = logic.get('correct_answer')
            if student_input == correct_answer:
                return Decimal('1.0'), {"status": "CORRECT"}
            elif student_input:
                # En Salud (ITIN_ROT), el error puede ser penalizado o fatal según el ítem
                if logic.get('kill_switch'):
                    return Decimal('0.0'), {"status": "FATAL_ERROR", "kill_switch_activated": True}
                penalty = Decimal(str(logic.get('penalty_factor', 0.5))) # Mayor penalización en Salud
                return -penalty, {"status": "INCORRECT", "penalty_applied": float(penalty)}

        return Decimal('0.0'), {"status": "PENDING_AI_REVIEW"}

    def get_system_prompt(self):
        """
        Generates prompt for ECOE model (V06DOC_ARCHETYPES).
        ---
        Genera prompt para el modelo ECOE (V06DOC_ARCHETYPES).
        """
        return f"""
ROLE: Especialista en Evaluación Clínica (ECOE).
PEDAGOGICAL LEVEL: {self.pedagogical_level}
ITINERARY: {self.itinerary_id}

TECHNICAL INSTRUCTIONS (V06DOC_BLOCKS):
1. CDS-KILL: Use for mandatory safety steps. Must set kill_switch: true.
2. PRM-STRIKE: Focus on differential diagnosis (V06DOC_SUBARCHETYPES).
3. ILC-CONTEXT: Generate clinical cases based on lab results or imaging.

GRADING BIAS (V06DOC_SUBDIVISIONS):
- If ITIN_ROT: Safety is the priority. Errors in critical steps result in FATAL_ERROR.
- Feedback must use FB_SAFETY for protocol violations (V06DOC_METADATA).
"""

    def get_user_prompt(self, context_text, topic):
        """
        Generates the specific user instruction for Health Exams (ECOE Model).
        ---
        Genera la instrucción específica de usuario para exámenes de salud (Modelo ECOE).
        """
        return (
            f"TEMA: {topic}. "
            f"MATERIAL DE REFERENCIA: {context_text[:40000]} "
            f"INSTRUCCIÓN: Actúa como evaluador clínico UGR. Genera un caso clínico real "
            f"con estaciones de Anamnesis, Técnica y Ética. "
            f"Nivel: {self.pedagogical_level}. Itinerario: {self.itinerary_id}. "
            f"REGLA DE ORO: Si detectas un paso de riesgo letal, usa el bloque CDS-KILL."
        )

    def get_output_schema(self):
        """
        Defines the high-fidelity JSON structure for the ECOE Exam Contract.
        ---
        Define la estructura JSON de alta fidelidad para el Contrato de Examen ECOE.
        """
        return {
            "subdivision_sequence": [
                {
                    "subdivision_id": "SD_FACT | SD_PROC | SD_ETHI",
                    "title": "string",
                    "instructions": "string",
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
                                "penalty_factor": 0.5
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
        contract = self.generate_contract_skeleton(exam_uuid, 'ARCH_HEALTH', sub_archetype_id)
        contract["subdivision_sequence"] = [
            {"subdivision_id": "SD_FACT", "title": "Anamnesis y Hechos", "items": []},
            {"subdivision_id": "SD_PROC", "title": "Procedimiento y Técnica", "items": []},
            {"subdivision_id": "SD_ETHI", "title": "Ética y Seguridad", "items": []}
        ]
        return contract
