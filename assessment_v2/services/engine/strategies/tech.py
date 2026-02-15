# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/tech.py
from .base import BaseExamStrategy
from decimal import Decimal

class TechnicalStrategy(BaseExamStrategy):
    """
    Strategy for Technical Sciences and Engineering (ARCH_TECH).
    Implements RPP-TRAZA for error carry-over and step-based grading.
    
    ---
    
    Estrategia para Ciencias Técnicas e Ingeniería (ARCH_TECH).
    Implementa RPP-TRAZA para el arrastre de error y calificación basada en pasos.
    """
    def grade_item(self, item, student_input):
        """
        Grades technical items following V06DOC_BLOCKS.
        ---
        Califica ítems técnicos siguiendo V06DOC_BLOCKS.
        """
        logic = item.grading_logic
        if item.block_type == 'RPP-TRAZA':
            # V06DOC_BLOCKS: The logical approach takes precedence (50%).
            # V06DOC_BLOCKS: El planteamiento lógico prima (50%).
            return Decimal('0.5'), {"status": "PARTIAL_GRADING", "detail": "Procedural trace requires calculation audit."}
        return Decimal('0.0'), {"status": "PENDING"}

    def get_system_prompt(self):
        """
        Returns the prompt for technical archetypes.
        ---
        Devuelve el prompt para arquetipos técnicos.
        """
        return f"ROLE: Catedrático de Ingeniería. LEVEL: {self.pedagogical_level}. Focus on RPP-TRAZA mechanics and CTE/EHE/ISO compliance."

    def get_user_prompt(self, context_text, topic):
        """
        Injects study context for engineering problems.
        ---
        Inyecta contexto de estudio para problemas de ingeniería.
        """
        return f"Generate engineering problems for '{topic}' focusing on structural/logical design based on: {context_text}"

    def get_output_schema(self):
        """
        Defines the JSON schema for technical items.
        ---
        Define el esquema JSON para ítems técnicos.
        """
        return "JSON with RPP-TRAZA and W-TECH-CALC widget_id."

    def generate_structure(self, exam_uuid, sub_archetype_id='SUB-TEC-SOFT'):
        """
        Initial relational skeleton for ARCH_TECH.
        ---
        Esqueleto relacional inicial para ARCH_TECH.
        """
        contract = self.generate_contract_skeleton(exam_uuid, 'ARCH_TECH', sub_archetype_id)
        contract["subdivision_sequence"] = [
            {"subdivision_id": "SD_THEO", "title": "Fundamentos Teóricos", "items": []},
            {"subdivision_id": "SD_MODEL", "title": "Modelado y Abstracción", "items": []},
            {"subdivision_id": "SD_CALC", "title": "Cálculo y Verificación", "items": []}
        ]
        return contract
