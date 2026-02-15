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
        Injects context for source criticism.
        ---
        Inyecta contexto para la crítica de fuentes.
        """
        return f"Generate essay topics and source analysis for '{topic}' based on: {context_text}"

    def get_output_schema(self):
        """
        Defines the schema for ARCH_HUM.
        ---
        Define el esquema para ARCH_HUM.
        """
        return "JSON with DRA-HOLO and EV-PALE blocks."

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
