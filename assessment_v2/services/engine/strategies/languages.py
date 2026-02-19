# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/languages.py
import json
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

    def _get_immersion_mode(self):
        """
        Heuristic to determine the interface language based on V06DOC_LEVELS V1.2 (UGR Normative).
        Deduce el modo de inmersión según la normativa de la UGR.
        """
        if self.pedagogical_level == 'LVL_C':
            return 'TOTAL'
        if self.itinerary_id == 'ITIN_MAI':
            return 'TOTAL' if self.pedagogical_level == 'LVL_B' else 'BILINGUAL'
        return 'BILINGUAL' if self.pedagogical_level == 'LVL_B' else 'VEHICULAR'

    def get_section_plan(self):
        """
        Returns the mandatory section list for the orchestrator to build the DB skeleton.
        Ref: V06DOC_ARCHETYPES (Language sequence).

        Devuelve la lista mandatoria de secciones para que el orquestador construya el esqueleto en la BBDD.
        Ref: V06DOC_ARCHETYPES (Secuencia de Lenguas).
        """
        mode = self._get_immersion_mode()
        
        # Estructura de mapeo para inmersión UGR
        sections_data = [
            {
                "id": "SD_READ", 
                "veh": "Comprensión Lectora", "tar": "Reading Comprehension",
                "i_veh": "Lee el texto y resuelve los desafíos lingüísticos.", "i_tar": "Read the text and solve the linguistic challenges."
            },
            {
                "id": "SD_LIST", 
                "veh": "Comprensión Auditiva", "tar": "Listening Comprehension",
                "i_veh": "Analiza las transcripciones de audio e identifica matices semánticos.", "i_tar": "Analyze the audio transcripts and identify semantic nuances."
            },
            {
                "id": "SD_WRIT", 
                "veh": "Producción Escrita", "tar": "Written Production",
                "i_veh": "Produce un texto académico respetando el registro formal.", "i_tar": "Produce an academic text respecting formal register."
            },
            {
                "id": "SD_MEDI", 
                "veh": "Mediación Lingüística", "tar": "Linguistic Mediation",
                "i_veh": "Sintetiza y adapta información entre diferentes registros.", "i_tar": "Synthesize and adapt information between different registers."
            }
        ]

        plan = []
        for s in sections_data:
            if mode == 'VEHICULAR':
                title, instr = s['veh'], s['i_veh']
            elif mode == 'BILINGUAL':
                title, instr = f"{s['veh']} / {s['tar']}", s['i_tar']
            else: # TOTAL
                title, instr = s['tar'], s['i_tar']
            
            plan.append({
                "subdivision_id": s['id'],
                "title": title,
                "instructions": instr,
                "time_limit": 900
            })
        return plan

    def get_system_prompt(self):
        """
        Returns the specific system prompt for the academic archetype.

        Devuelve el prompt de sistema específico para el arquetipo académico.
        """
        roles = {
            "SUB-LIN-CERT": "Examinador CertAccles/MCER. Foco: Estandarización, Gramática.",
            "SUB-LIN-PROF": "Experto en LSP (Language for Specific Purposes). Foco: Terminología Técnica.",
            "SUB-LIN-LIT": "Filólogo/Crítico Literario. Foco: Exégesis, Retórica, Análisis métrico."
        }
        base_role = roles.get(self.sub_archetype_id, "Profesor de Lenguas.")
        mode = self._get_immersion_mode()
        
        return (
            f"IDENTIDAD: {base_role}\n"
            f"MODO DE INMERSIÓN: {mode}. Si es TOTAL, genera TODA la salida en el idioma objetivo.\n"
            f"REGLA CRÍTICA: Sin explicaciones. Solo el JSON atómico."
        )

    def get_user_prompt(self, context_text, topic, subdivision_id, generated_item_titles=None):
        """
        Atomic generation prompt for a specific subdivision with context memory.

        Prompt de generación atómica para una subdivisión específica con memoria de contexto.
        """
        memory = "\nEVITA REPETICIÓN: " + ", ".join(generated_item_titles) if generated_item_titles else ""
        return (
            f"GENERA 3 ÍTEMS para la sección: {subdivision_id}.\n"
            f"TEMA: {topic}. NIVEL: {self.pedagogical_level}.{memory}\n"
            f"CONTEXTO DOCENTE:\n{context_text[:15000]}\n\n"
            f"CONFIG: Arquetipo={self.sub_archetype_id}, Itinerario={self.itinerary_id}, Modo={self._get_immersion_mode()}.\n"
            f"SALIDA: JSON estricto (Array 'items')."
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
                                    "text_with_gaps": {"type": "string"},
                                    "options": {"type": "array", "items": {"type": "string"}}
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
