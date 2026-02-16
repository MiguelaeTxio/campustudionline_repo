# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/humanities.py
from .base import BaseExamStrategy
from decimal import Decimal

class HumanitiesStrategy(BaseExamStrategy):
    """
    Strategy for Arts and Humanities (ARCH_HUM).
    Implements EV-PALE for source exegesis and DRA-HOLO for dissertations.
    
    ---
    
    Estrategia para Artes y Humanidades (ARCH_HUM).
    Implementa EV-PALE para la exégesis de fuentes y DRA-HOLO para disertaciones.
    """
    def grade_item(self, item, student_input):
        """
        Grades humanitarian items using V06DOC_BLOCKS criteria.
        ---
        Califica ítems de humanidades usando los criterios de V06DOC_BLOCKS.
        """
        if item.block_type == 'DRA-HOLO':
            return Decimal('0.0'), {"status": "REQUIRES_CRITICAL_REVIEW", "rubric": "V06DOC_BLOCKS (Holística)"}
        return Decimal('0.0'), {"status": "PENDING"}

    def get_system_prompt(self):
        """
        Returns the prompt for humanities.
        ---
        Devuelve el prompt para humanidades.
        """
        return f"ROLE: Catedrático de Humanidades. LEVEL: {self.pedagogical_level}. Focus on exegesis, dialectics, and source criticism."

    def get_user_prompt(self, context_text, topic):
        """
        Generates the specific user instruction for Humanities Exams (Hermeneutic Model).
        ---
        Genera la instrucción específica de usuario para exámenes de humanidades (Modelo Hermenéutico).
        """
        return (
            f"TEMA: {topic}. "
            f"MATERIAL DE REFERENCIA: {context_text[:40000]} "
            f"INSTRUCCIÓN: Actúa como Catedrático de Humanidades UGR. Genera ejercicios de "
            f"exégesis de fuentes primarias y disertación dialéctica. "
            f"Nivel: {self.pedagogical_level}. Itinerario: {self.itinerary_id}. "
            f"Rigor: Máxima corrección formal y calidad discursiva."
        )

    def get_output_schema(self):
        """
        Defines the high-fidelity JSON structure for the Humanities Exam Contract.
        ---
        Define la estructura JSON de alta fidelidad para el Contrato de Examen de Humanidades.
        """
        return {
            "subdivision_sequence": [
                {
                    "subdivision_id": "SD_SOURCE | SD_DISC | SD_ARTE",
                    "title": "string",
                    "instructions": "string",
                    "items": [
                        {
                            "block_type": "EV-PALE | DRA-HOLO | BMT-SHIFT",
                            "widget_id": "W-HUM-TEXT | W-COMM-DIALOG",
                            "content": {
                                "stem": "string",
                                "source_material": "string",
                                "media_assets": ["urls"]
                            },
                            "grading_logic": {
                                "holistic_rubric": True,
                                "formal_penalty_max": 2.5
                            },
                            "metadata": {
                                "competency_tag": "COMP_GEN | COMP_TRA",
                                "cognitive_tag": "COG_ANA | COG_CREA"
                            }
                        }
                    ]
                }
            ]
        }

    def generate_structure(self, exam_uuid, sub_archetype_id='SUB-HUM-HIST'):
        """
        Initial structure for ARCH_HUM.
        ---
        Estructura inicial para ARCH_HUM.
        """
        contract = self.generate_contract_skeleton(exam_uuid, 'ARCH_HUM', sub_archetype_id)
        contract["subdivision_sequence"] = [
            {"subdivision_id": "SD_SOURCE", "title": "Crítica de Fuentes", "items": []},
            {"subdivision_id": "SD_DISC", "title": "Discurso Crítico", "items": []}
        ]
        return contract
