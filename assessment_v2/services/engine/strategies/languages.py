# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/languages.py
from .base import BaseExamStrategy
from decimal import Decimal
import re

class LanguagesStrategy(BaseExamStrategy):
    """
    Strategy for Foreign Languages (ARCH_LANG).
    Compliant with CertAccles/MCER models and V06DOC_ARCHETYPES.
    
    COVERS:
    - 3 Sub-archetypes (CERT, PROF, LIT).
    - 5 Destrezas: Reading, Listening, Writing, Speaking, Mediación.
    - Engines: CLO-OPEN, CLO-MULTI, MAT-LINK, DRA-HOLO.
    - Itinerary Sensitivity: MAI (Strict/Academic) vs MIN (Functional/Tolerant).
    """

    def grade_item(self, item, student_input):
        """
        Grades linguistic items with strictness based on Itinerary.
        Ref: V06DOC_LEVELS & V06DOC_BLOCKS.
        """
        logic = item.grading_logic
        block_type = item.block_type
        
        # --- MOTOR 1: CLO-OPEN / CLO-MULTI (Gap Filling) ---
        if block_type in ['CLO-OPEN', 'CLO-MULTI']:
            correct_answer = str(logic.get('correct_answer', '')).lower().strip()
            student_answer = str(student_input).lower().strip()
            
            if student_answer == correct_answer:
                return Decimal('1.0'), {"status": "CORRECT"}
            
            # MAIOR Itinerary: Zero tolerance for spelling/grammar in gaps
            if self.itinerary_id == 'ITIN_MAI':
                return Decimal('-0.5'), {"status": "INCORRECT", "detail": "Strict academic precision required."}
            
            # MINOR Itinerary: Flexible (Small typos might be ignored if meaning is clear)
            # Placeholder for future Levenshtein distance logic
            return Decimal('0.0'), {"status": "INCORRECT"}

        # --- MOTOR 2: MAT-LINK (Matching) ---
        elif block_type == 'MAT-LINK':
            # Logic for Drag & Drop matching
            pairs = logic.get('pairs', {})
            hits = sum(1 for k, v in student_input.items() if pairs.get(k) == v)
            score = Decimal(str(hits / len(pairs))) if pairs else Decimal('0.0')
            return score, {"status": "GRADED", "hits": hits}

        # --- MOTOR 3: DRA-HOLO (Writing/Essay) ---
        elif block_type == 'DRA-HOLO':
            # Writing requires rubric-based grading (Hito 6 Phase 4)
            return Decimal('0.0'), {"status": "PENDING_AI_RUBRIC", "detail": "Writing analysis queued."}

        return Decimal('0.0'), {"status": "PENDING"}

    def get_system_prompt(self):
        """
        Dynamic Role for Languages (V06DOC_SUBARCHETYPES).
        """
        roles = {
            'SUB-LIN-CERT': "Rol: Examinador CertAccles/MCER. Foco: Estandarización, Gramática, Uso de la lengua.",
            'SUB-LIN-PROF': "Rol: Experto en LSP (Language for Specific Purposes). Foco: Terminología Técnica.",
            'SUB-LIN-LIT': "Rol: Filólogo/Crítico Literario. Foco: Exégesis, Retórica, Análisis métrico."
        }
        base_role = roles.get(self.sub_archetype_id, "Rol: Profesor de Lenguas.")

        # ITINERARY Nuance
        if self.itinerary_id == 'ITIN_MAI':
            context = "RIGOR: MAIOR (Catedrático). No aceptes paráfrasis en terminología. Penaliza errores gramaticales base."
        else:
            context = "RIGOR: MINOR (Funcional). Valora la eficacia comunicativa. Feedback constructivo."

        return f"{base_role}\n{context}\nESTRUCTURA: Genera secciones para las 5 destrezas MCER."

    def get_user_prompt(self, context_text, topic):
        """
        CertAccles generation prompt.
        """
        return (
            f"GENERATE LANGUAGE EXAM.\n"
            f"TOPIC: {topic}. MCER LEVEL: {self.pedagogical_level}.\n"
            f"ITINERARY: {self.itinerary_id}.\n"
            f"REQUIREMENTS:\n"
            f"1. Segregate by Reading, Writing, and Use of English.\n"
            f"2. Use CLO-OPEN for advanced grammar validation.\n"
            f"3. Use W-TXT-CLOZE for embedded text inputs."
        )

    def get_output_schema(self):
        return {
            "subdivision_sequence": [
                {
                    "subdivision_id": "SD_READ | SD_WRIT | SD_LIST | SD_SPEAK | SD_MEDI",
                    "title": "string",
                    "items": [
                        {
                            "block_type": "CLO-OPEN | CLO-MULTI | MAT-LINK | DRA-HOLO",
                            "widget_id": "W-TXT-CLOZE | W-MIX-MATCH | W-HUM-TEXT",
                            "content": {"stem": "string", "text_with_gaps": "string"},
                            "grading_logic": {"correct_answer": "string", "pairs": "dict"},
                            "metadata": {"competency_tag": "COMP_GEN | COMP_ESP"}
                        }
                    ]
                }
            ]
        }

    def generate_structure(self, exam_uuid, sub_archetype_id='SUB-LIN-CERT'):
        """
        Language-specific 5 destrezas structure (V06DOC_ARCHETYPES).
        """
        contract = self.generate_contract_skeleton(exam_uuid, 'ARCH_LANG', sub_archetype_id)
        contract["subdivision_sequence"] = [
            {"subdivision_id": "SD_READ", "title": "Reading Comprehension", "items": []},
            {"subdivision_id": "SD_LIST", "title": "Listening Comprehension", "items": []},
            {"subdivision_id": "SD_WRIT", "title": "Written Production", "items": []},
            {"subdivision_id": "SD_MEDI", "title": "Linguistic Mediation", "items": []}
        ]
        return contract
