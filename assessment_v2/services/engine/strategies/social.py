# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/social.py
from .base import BaseExamStrategy
from decimal import Decimal

class SocialStrategy(BaseExamStrategy):
    """
    Strategy for Social and Legal Sciences (ARCH_SOC).
    Focuses on case analysis and regulatory framing.
    
    ---
    
    Estrategia para Ciencias Sociales y Jurídicas (ARCH_SOC).
    Se centra en el análisis de casos y el encuadre normativo.
    """
    def grade_item(self, item, student_input):
        """
        Grades social/legal cases according to V06DOC_SUBDIVISIONS.
        ---
        Califica casos sociales/jurídicos según V06DOC_SUBDIVISIONS.
        """
        return Decimal('0.0'), {"status": "REQUIRES_JURIDICAL_ANALYSIS", "role": "Magistrado/Economista"}

    def get_system_prompt(self):
        """
        Returns the prompt for social archetypes.
        ---
        Devuelve el prompt para arquetipos sociales.
        """
        return f"ROLE: Experto Jurídico/Económico. LEVEL: {self.pedagogical_level}. Focus on case studies and official regulations."

    def get_user_prompt(self, context_text, topic):
        """
        Generates the specific user instruction for Social/Legal Exams (Casuistic Model).
        ---
        Genera la instrucción específica de usuario para exámenes sociales/jurídicos (Modelo Casuístico).
        """
        return (
            f"TEMA: {topic}. "
            f"MATERIAL DE REFERENCIA: {context_text[:40000]} "
            f"INSTRUCCIÓN: Actúa como Magistrado o Consultor Senior. Genera un supuesto de hecho "
            f"real que requiera encuadre normativo y dictamen técnico. Usa el widget W-LAW-NAV."
            f"Nivel: {self.pedagogical_level}. Itinerario: {self.itinerary_id}."
        )

    def get_output_schema(self):
        """
        Defines the high-fidelity JSON structure for the Social/Legal Exam Contract.
        ---
        Define la estructura JSON de alta fidelidad para el Contrato de Examen Social/Jurídico.
        """
        return {
            "subdivision_sequence": [
                {
                    "subdivision_id": "SD_FACT | SD_NORM | SD_PROC",
                    "title": "string",
                    "instructions": "string",
                    "items": [
                        {
                            "block_type": "ILC-CONTEXT | PRM-STRIKE",
                            "widget_id": "W-LAW-NAV | W-OBJ-STRIKE",
                            "content": {
                                "stem": "string",
                                "options": "list (for PRM)",
                                "case_context": "string"
                            },
                            "grading_logic": {
                                "correct_answer": "any",
                                "legal_precedent_required": "boolean"
                            },
                            "metadata": {
                                "competency_tag": "COMP_ESP | COMP_TRA",
                                "cognitive_tag": "COG_ANA | COG_EVAL"
                            }
                        }
                    ]
                }
            ]
        }

    def generate_structure(self, exam_uuid, sub_archetype_id='SUB-SOC-JUR'):
        """
        Initial structure for ARCH_SOC.
        ---
        Estructura inicial para ARCH_SOC.
        """
        contract = self.generate_contract_skeleton(exam_uuid, 'ARCH_SOC', sub_archetype_id)
        contract["subdivision_sequence"] = [
            {"subdivision_id": "SD_FACT", "title": "Hechos y Relevancia", "items": []},
            {"subdivision_id": "SD_NORM", "title": "Encuadre Normativo", "items": []},
            {"subdivision_id": "SD_PROC", "title": "Resolución y Dictamen", "items": []}
        ]
        return contract
