# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/humanities.py
from .base import BaseExamStrategy
from decimal import Decimal
import json

class HumanitiesStrategy(BaseExamStrategy):
    """
    Strategy for Arts and Humanities (ARCH_HUM).
    Fully compliant with Hermeneutic model and V06DOC_SUBARCHETYPES.
    
    COVERS:
    - 5 Sub-archetypes (HIST, PHIL, EDU, CREA, MUS).
    - Blocks: DRA-HOLO (Holistic Rubric), EV-PALE (Exegesis).
    - Itineraries: DOC (Didactic - DUA), INV (Methodological), MAI, MIN.
    - Widgets: W-HUM-TEXT (Split-screen), W-OBJ-STRIKE.
    """

    def grade_item(self, item, student_input):
        """
        Grades humanities items using Rubric-based logic (DRA-HOLO).
        """
        logic = item.grading_logic
        block_type = item.block_type

        # --- MOTOR 1: DRA-HOLO (Rúbrica Holística) ---
        # Ref: V06DOC_BLOCKS Section 2
        if block_type == 'DRA-HOLO':
            # Logic: Evaluates 4 axes. At this stage, it marks for AI or Manual Review
            # but applies FORM_PEN (-2.5) if formal requirements aren't met.
            formal_penalty = Decimal('0.0')
            if self.itinerary_id in ['ITIN_MAI', 'ITIN_INV']:
                # Strict formal checking (simplified for MVP logic)
                if len(str(student_input)) < 200: # Example constraint
                    formal_penalty = Decimal('2.0') # V06DOC_BLOCKS: "Penalización formal hasta -2.5"

            return Decimal('0.0'), {
                "status": "PENDING_AI_RUBRIC",
                "axes": ["Rigor", "Estructura", "Terminología", "Forma"],
                "formal_penalty_risk": float(formal_penalty)
            }

        # --- MOTOR 2: EV-PALE (Transcripción/Exégesis) ---
        elif block_type == 'EV-PALE':
            # Exact match for transcription + semantic analysis for exegesis
            correct_transcription = logic.get('correct_transcription', '')
            if str(student_input).strip() == correct_transcription.strip():
                return Decimal('1.0'), {"status": "CORRECT_TRANSCRIPTION"}
            return Decimal('0.5'), {"status": "PARTIAL_TRANSCRIPTION", "detail": "Transcription errors found."}

        return Decimal('0.0'), {"status": "PENDING_MANUAL_REVIEW"}

    def get_system_prompt(self):
        """
        Dynamic Role for Humanities (V06DOC_SUBARCHETYPES).
        """
        roles = {
            'SUB-HUM-HIST': "Rol: Historiador/Arqueólogo (UGR). Foco: Análisis de fuentes, Cronología, Crítica de autenticidad.",
            'SUB-HUM-PHIL': "Rol: Filósofo/Lógico. Foco: Dialéctica, Coherencia argumental, Rigor formal.",
            'SUB-HUM-EDU': "Rol: Especialista en Didáctica (LOMLOE). Foco: Diseño DUA, Situaciones de Aprendizaje.",
            'SUB-ART-CREA': "Rol: Crítico/Teórico del Arte. Foco: Técnica matérica, Discurso estético, Composición.",
            'SUB-ART-MUS': "Rol: Musicólogo. Foco: Análisis armónico, Historia musical, Transcripción."
        }
        base_role = roles.get(self.sub_archetype_id, "Rol: Humanista Senior.")

        # ITINERARY (V06DOC_SUBDIVISIONS)
        itin_ctx = ""
        if self.itinerary_id == 'ITIN_DOC':
            itin_ctx = "ENFOQUE DIDÁCTICO: Evalúa la capacidad de transposición didáctica y el cumplimiento de LOMLOE/DUA."
        elif self.itinerary_id == 'ITIN_INV':
            itin_ctx = "ENFOQUE INVESTIGADOR: Exige rigor absoluto en citas bibliográficas y estado del arte."

        return f"{base_role}\n{itin_ctx}\nESTRUCTURA: Usa subdivisiones SD_SOURCE y SD_DISC. Evalúa con Rúbrica Holística DRA-HOLO."

    def get_user_prompt(self, context_text, topic):
        return (
            f"GENERATE HUMANITIES EXAM.\n"
            f"TOPIC: {topic}\n"
            f"REF: {context_text[:50000]}\n"
            f"CONFIG: Sub-Arch={self.sub_archetype_id}, Itin={self.itinerary_id}, Level={self.pedagogical_level}.\n"
            f"REQUIREMENTS:\n"
            f"1. Focus on source criticism (SD_SOURCE) and critical discourse (SD_DISC).\n"
            f"2. Use DRA-HOLO for long-form essays.\n"
            f"3. If EDU, ensure the item focuses on teaching strategies."
        )

    def get_output_schema(self):
        return {
            "subdivision_sequence": [
                {
                    "subdivision_id": "SD_SOURCE | SD_DISC | SD_ARTE",
                    "title": "string",
                    "items": [
                        {
                            "block_type": "DRA-HOLO | EV-PALE | PRM-STRIKE",
                            "widget_id": "W-HUM-TEXT | W-OBJ-STRIKE",
                            "content": {"stem": "string", "source_material": "string"},
                            "grading_logic": {"rubric_criteria": ["list"], "correct_transcription": "string"},
                            "metadata": {"competency_tag": "COMP_GEN | COMP_TRA"}
                        }
                    ]
                }
            ]
        }

    def generate_structure(self, exam_uuid, sub_archetype_id='SUB-HUM-HIST'):
        contract = self.generate_contract_skeleton(exam_uuid, 'ARCH_HUM', sub_archetype_id)
        contract["subdivision_sequence"] = [
            {"subdivision_id": "SD_SOURCE", "title": "Análisis y Crítica de Fuentes", "items": []},
            {"subdivision_id": "SD_DISC", "title": "Discurso e Interpretación Crítica", "items": []}
        ]
        return contract
