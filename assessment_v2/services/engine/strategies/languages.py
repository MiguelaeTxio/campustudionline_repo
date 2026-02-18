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

    Estrategia para Lenguas Extranjeras (ARCH_LANG).
    Cumple con los modelos CertAccles/MCER y V06DOC_ARCHETYPES.
    
    CUBRE:
    - 3 Sub-arquetipos (CERT, PROF, LIT).
    - 5 Destrezas: Reading, Listening, Writing, Speaking, Mediación.
    - Motores: CLO-OPEN, CLO-MULTI, MAT-LINK, DRA-HOLO.
    - Sensibilidad de Itinerario: MAI (Estricto/Académico) vs MIN (Funcional/Tolerante).
    """

    def grade_item(self, item, student_input):
        """
        Grades linguistic items with strictness based on Itinerary.
        Ref: V06DOC_LEVELS & V06DOC_BLOCKS.

        Califica ítems lingüísticos con rigor basado en el itinerario.
        Ref: V06DOC_LEVELS & V06DOC_BLOCKS.
        """
        logic = item.grading_logic
        block_type = item.block_type
        
        # --- MOTOR 1: CLO-OPEN / CLO-MULTI (Gap Filling) ---
        if block_type in ["CLO-OPEN", "CLO-MULTI"]:
            correct_answer = str(logic.get("correct_answer", "")).lower().strip()
            student_answer = str(student_input).lower().strip()
            
            if student_answer == correct_answer:
                return Decimal("1.0"), {"status": "CORRECT", "feedback_category": "FB_CONCEPT"}
            
            # MAIOR Itinerary: Zero tolerance for spelling/grammar in gaps
            if self.itinerary_id == "ITIN_MAI":
                return Decimal("-0.5"), {"status": "INCORRECT", "detail": "Strict academic precision required.", "feedback_category": "FB_FORMAL"}
            
            # MINOR Itinerary: Flexible (Small typos might be ignored if meaning is clear)
            # Placeholder for future Levenshtein distance logic
            return Decimal("0.0"), {"status": "INCORRECT", "feedback_category": "FB_CONCEPT"}

        # --- MOTOR 2: MAT-LINK (Matching) ---
        elif block_type == "MAT-LINK":
            # Logic for Drag & Drop matching
            pairs = logic.get("pairs", {})
            hits = sum(1 for k, v in student_input.items() if pairs.get(k) == v)
            score = Decimal(str(hits / len(pairs))) if pairs else Decimal("0.0")
            return score, {"status": "GRADED", "hits": hits, "feedback_category": "FB_PROCEDURAL"}

        # --- MOTOR 3: DRA-HOLO (Writing/Essay) ---
        elif block_type == "DRA-HOLO":
            # Writing requires rubric-based grading (Hito 6 Phase 4)
            return Decimal("0.0"), {"status": "PENDING_AI_RUBRIC", "detail": "Writing analysis queued.", "feedback_category": "FB_FORMAL"}

        return Decimal("0.0"), {"status": "PENDING"}

    def get_section_plan(self):
        """
        Returns the mandatory section list for the orchestrator to build the DB skeleton.
        Ref: V06DOC_ARCHETYPES (Language sequence).

        Devuelve la lista mandatoria de secciones para que el orquestador construya el esqueleto en la BBDD.
        Ref: V06DOC_ARCHETYPES (Secuencia de Lenguas).
        """
        return [
            {"subdivision_id": "SD_READ", "title": "Reading Comprehension", "instructions": "Read the text and solve the linguistic challenges."},
            {"subdivision_id": "SD_LIST", "title": "Listening Comprehension", "instructions": "Analyze the audio transcripts and identify semantic nuances."},
            {"subdivision_id": "SD_WRIT", "title": "Written Production", "instructions": "Produce an academic text respecting formal register and specific terminology."},
            {"subdivision_id": "SD_MEDI", "title": "Linguistic Mediation", "instructions": "Synthesize and adapt information between different registers or languages."}
        ]

    def get_system_prompt(self):
        """
        Dynamic Role for Languages (V06DOC_SUBARCHETYPES).

        Rol dinámico para lenguas (V06DOC_SUBARCHETYPES).
        """
        roles = {
            "SUB-LIN-CERT": "Examinador CertAccles/MCER. Foco: Estandarización, Gramática, Uso de la lengua.",
            "SUB-LIN-PROF": "Experto en LSP (Language for Specific Purposes). Foco: Terminología Técnica.",
            "SUB-LIN-LIT": "Filólogo/Crítico Literario. Foco: Exégesis, Retórica, Análisis métrico."
        }
        base_role = roles.get(self.sub_archetype_id, "Profesor de Lenguas.")
        context = "RIGOR: MAIOR (Catedrático). No aceptes paráfrasis en terminología." if self.itinerary_id == "ITIN_MAI" else "RIGOR: MINOR (Funcional). Feedback constructivo."
        
        return (
            f"IDENTIDAD: {base_role} {context}\n"
            f"FORMATO: Responde EXCLUSIVAMENTE con un JSON que cumpla el schema OpenAPI 3.0 proporcionado.\n"
            f"REGLA CRÍTICA: Sin explicaciones ni etiquetas Markdown. Solo el JSON."
        )

    def get_user_prompt(self, context_text, topic, subdivision_id, generated_item_titles=None):
        """
        Atomic generation prompt for a specific subdivision with context memory.

        Prompt de generación atómica para una subdivisión específica con memoria de contexto.
        """
        memory = "\nAVOID REPETITION: The following items have already been generated: " + ", ".join(generated_item_titles) if generated_item_titles else ""
        return (
            f"GENERATE 3 ITEMS for subdivision: {subdivision_id}.\n"
            f"TEMA: {topic}. NIVEL: {self.pedagogical_level}.{memory}\n"
            f"CONTEXTO DOCENTE (RANGO SELECCIONADO):\n{context_text[:15000]}"
        )

    def get_output_schema(self):
        """
        Defines the formal OpenAPI 3.0 Schema for JSON Mode.
        Ref: V06DOC_TEMPLATES.

        Define el Schema formal OpenAPI 3.0 para el Modo JSON.
        Ref: V06DOC_TEMPLATES.
        """
        return {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "block_type": {"type": "string", "enum": ["CLO-OPEN", "CLO-MULTI", "MAT-LINK", "DRA-HOLO"]},
                            "widget_id": {"type": "string", "enum": ["W-TXT-CLOZE", "W-MIX-MATCH", "W-HUM-TEXT"]},
                            "content": {
                                "type": "object",
                                "properties": {
                                    "stem": {"type": "string"},
                                    "text_with_gaps": {"type": "string"}
                                },
                                "required": ["stem"]
                            },
                            "grading_logic": {
                                "type": "object",
                                "properties": {
                                    "correct_answer": {"type": "string"},
                                    "pairs": {"type": "object"}
                                }
                            },
                            "metadata": {
                                "type": "object",
                                "properties": {
                                    "competency_tag": {"type": "string"},
                                    "cognitive_tag": {"type": "string"}
                                },
                                "required": ["competency_tag", "cognitive_tag"]
                            }
                        },
                        "required": ["block_type", "widget_id", "content", "grading_logic", "metadata"]
                    }
                }
            },
            "required": ["items"]
        }
