# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/languages.py
from .base import BaseExamStrategy
from decimal import Decimal
import json

class LanguagesStrategy(BaseExamStrategy):
    """
    Exam strategy for languages based on international standards.
    Implements UGR-standard penalty formulas for objective items.
    
    ---
    
    Estrategia de examen para idiomas basada en estándares internacionales.
    Implementa fórmulas de penalización estándar UGR para ítems objetivos.
    """

    def grade_item(self, item, student_input):
        """
        Implements the UGR formula: [Correct - (Incorrect/(N-1))].
        Current implementation for PRM-STRIKE (Multiple Choice).
        ---
        Implementa la fórmula UGR: [Aciertos - (Errores/(N-1))].
        Implementación actual para PRM-STRIKE (Selección Múltiple).
        """
        logic = item.grading_logic
        correct_answer = logic.get('correct_answer')
        penalty = Decimal(str(logic.get('penalty_factor', 0.33)))
        
        # Logic for Multiple Choice (PRM-STRIKE)
        if item.block_type == 'PRM-STRIKE':
            if student_input == correct_answer:
                return Decimal('1.0'), {"status": "CORRECT", "detail": "Match found."}
            elif student_input:
                # Apply penalty for wrong answer to discourage guessing
                return -penalty, {"status": "INCORRECT", "penalty_applied": float(penalty)}
        
        # Production blocks (DRA-HOLO, BMT-SHIFT) currently default to pending
        return Decimal('0.0'), {"status": "PENDING_AI_REVIEW", "detail": "Requires linguistic analysis."}

    def get_output_schema(self):
        """Returns the item payload schema description."""
        return "Object containing block_type, widget_id, content, grading_logic, and metadata."

    def get_system_prompt(self):
        """Inyecta las mecánicas de V06DOC_BLOCKS en el cerebro de la IA."""
        p_factor = 0.33 # Penalty factor for 4 options
        return f"""
ROLE: UniversIA Linguistic Expert.
PEDAGOGICAL LEVEL: {self.pedagogical_level}
ITINERARY: {self.itinerary_id}

TECHNICAL INSTRUCTIONS:
Generate items following V06DOC_BLOCKS mechanics:
1. PRM-STRIKE: Multiple Choice with penalty_factor={p_factor}.
2. CLO-MULTI: Multiple Choice Cloze (Text with selectables).
3. MAT-LINK: Matching (Link headers to paragraphs).
4. DRA-HOLO: Holistic rubrics for production.
"""

    def get_user_prompt(self, context_text, topic):
        return f"Generate assessment items for topic '{topic}' using this material: {context_text}"

    def generate_structure(self, exam_uuid, sub_archetype_id='SUB-LIN-CERT'):
        """Creates the initial relational structure skeleton."""
        contract = self.generate_contract_skeleton(exam_uuid, 'ARCH_LANG', sub_archetype_id)
        contract["subdivision_sequence"] = [
            {"subdivision_id": "SD_READ", "title": "Reading & Use of English", "items": []},
            {"subdivision_id": "SD_LIST", "title": "Listening", "items": []},
            {"subdivision_id": "SD_WRIT", "title": "Writing", "items": []},
            {"subdivision_id": "SD_MEDI", "title": "Mediation", "items": []},
            {"subdivision_id": "SD_SPEAK", "title": "Speaking", "items": []}
        ]
        return contract
