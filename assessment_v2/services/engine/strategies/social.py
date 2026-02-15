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
        Injects context for juridical/social cases.
        ---
        Inyecta contexto para casos jurídicos/sociales.
        """
        return f"Generate case studies for '{topic}' requiring regulatory framing based on: {context_text}"

    def get_output_schema(self):
        """
        Defines the schema for ARCH_SOC.
        ---
        Define el esquema para ARCH_SOC.
        """
        return "JSON with case study blocks and W-LAW-NAV widget_id."

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
