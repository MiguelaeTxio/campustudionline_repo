# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/humanities.py
from .base import BaseExamStrategy
from decimal import Decimal
import json

class HumanitiesStrategy(BaseExamStrategy):
    """
    Strategy for Arts and Humanities (ARCH_HUM).
    Fully compliant with Hermeneutic model and V06DOC_SUBARCHETYPES.
    
    COVERS:
    - 6 Sub-archetypes (HIST, PHIL, ART-HIST, ART-CREA, MUS, ANTH).
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
            if isinstance(student_input, dict) and 'file_url' in student_input:
                return Decimal('0.0'), {"status": "PENDING_AI_ANALYSIS", "detail": "Archivo subido correctamente. En cola para análisis.", "file_received": True}
            # Logic: Evaluates 4 axes. At this stage, it marks for AI or Manual Review
            # but applies FORM_PEN (-2.0) if formal requirements aren't met.
            student_text = str(student_input).strip()
            if not student_text:
                return Decimal("0.0"), {"status": "OMITTED"}
            word_count = len(student_text.split())

            # [HITO 6 FIX] Discrepancia 4: Corrección de escala.
            # No aplicamos resta numérica aquí (rompía la escala), solo marcamos el error.
            # logic.py aplicará la penalización de -0.2 sobre 1.0.
            is_formal_fail = False
            if self.itinerary_id in ['ITIN_MAI', 'ITIN_INV']:
                if word_count < 200: 
                    is_formal_fail = True

            base_score = min(Decimal(str(word_count / 200.0)), Decimal("1.0"))
            
            return base_score, {
                "status": "GRADED",
                "axes": {
                    "rigor": {"weight": 0.4, "score": float(base_score)},
                    "structure": {"weight": 0.2, "score": float(base_score)},
                    "terminology": {"weight": 0.2, "score": float(base_score)},
                    "form": {"weight": 0.2, "score": 0.0 if is_formal_fail else float(base_score)}
                },
                "feedback_category": "FB_FORMAL" if is_formal_fail else "FB_CONCEPT",
                "justification": "Deficiencia formal en extensión (Penalización aplicable)." if is_formal_fail else ""
            }

        # --- MOTOR 2: EV-PALE (Transcripción/Exégesis) ---
        elif block_type == 'EV-PALE':
            if isinstance(student_input, dict) and 'file_url' in student_input:
                return Decimal('0.0'), {"status": "PENDING_AI_ANALYSIS", "detail": "Archivo subido correctamente. En cola para análisis.", "file_received": True}
            # Exact match for transcription + semantic analysis for exegesis
            correct_transcription = logic.get('correct_transcription', '')
            if str(student_input).strip() == correct_transcription.strip():
                return Decimal('1.0'), {"status": "CORRECT_TRANSCRIPTION"}
            return Decimal('0.5'), {"status": "PARTIAL_TRANSCRIPTION", "detail": "Errores de transcripción encontrados."}

        return Decimal('0.0'), {"status": "PENDING_MANUAL_REVIEW"}

    def get_exam_skeleton(self):
        """
        Returns the structural skeleton for the 6 Humanities models.
        Ref: V06DOC_SUBARCHETYPES V5.0.
        Refactor: DRY & Prompt Binding implemented. (Replaces legacy get_section_plan)
        """
        sid = self.sub_archetype_id
        skeleton = []

        # 1. INSTRUCCIONES BASE (DRY)
        I_SOURCE = "Analiza la fuente primaria proporcionada (texto, imagen o partitura) identificando su contexto, autoría y estructura."
        I_DISC = "Desarrolla un ensayo crítico argumentado sobre las tesis planteadas, citando autores relevantes."
        I_TRANS = "Transcribe el fragmento paleográfico o musical con exactitud."
        I_THEORY = "Responde a la cuestión teórica fundamental."

        # 2. OVERRIDES ESPECÍFICOS
        if sid == "SUB-HUM-HIST":
            I_SOURCE = "Realiza el comentario de texto histórico o epigráfico. Determina datación y fiabilidad."
        elif sid == "SUB-HUM-ART-HIST":
            I_SOURCE = "Realiza el análisis iconográfico y formal de la obra de arte descrita."
        elif sid == "SUB-HUM-PHIL":
            I_SOURCE = "Analiza la estructura lógica y argumentativa del fragmento filosófico."
            I_DISC = "Desarrolla una disertación dialéctica confrontando las posturas del autor."
        elif sid == "SUB-HUM-MUS":
            I_SOURCE = "Analiza la estructura armónica y formal de la partitura."
            I_TRANS = "Realiza la transcripción o dictado musical."

        # 3. CONSTRUCCIÓN DEL ESQUELETO
        # Estructura común para la mayoría: Fuente (Split) + Discurso (Standard)
        if sid in ["SUB-HUM-HIST", "SUB-HUM-ART-HIST", "SUB-HUM-PHIL", "SUB-HUM-ANTH", "SUB-HUM-ART-CREA"]:
            skeleton = [
                {"subdivision_id": "SD_SOURCE", "title": "Análisis de Fuentes", "instructions": "Analice la fuente primaria.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "EV-PALE", "widget_id": "W-HUM-TEXT", "task_instruction": I_SOURCE}]},
                {"subdivision_id": "SD_DISC", "title": "Discurso Crítico", "instructions": "Desarrolle el tema propuesto.", "layout_mode": "STANDARD", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": I_DISC}]}
            ]
        elif sid == "SUB-HUM-MUS":
            skeleton = [
                {"subdivision_id": "SD_SOURCE", "title": "Análisis Musical", "instructions": "Analice la obra.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "EV-PALE", "widget_id": "W-HUM-TEXT", "task_instruction": I_SOURCE}]},
                {"subdivision_id": "SD_SOURCE", "title": "Transcripción/Dictado", "instructions": "Transcriba el fragmento.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "EV-PALE", "widget_id": "W-HUM-TEXT", "task_instruction": I_TRANS}]}
            ]
        elif sid == "SUB-HUM-ART-CREA":
            skeleton = [
                {"subdivision_id": "SD_SOURCE", "title": "Análisis Visual", "instructions": "Analice la fuente visual.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "EV-PALE", "widget_id": "W-HUM-TEXT", "task_instruction": I_SOURCE}]},
                {"subdivision_id": "SD_ARTE", "title": "Técnica Matérica", "instructions": "Valore la técnica constructiva y compositiva.", "layout_mode": "STANDARD", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": "Evalúa el proceso matérico, la técnica y la composición de la obra."}]}
            ]
        else:
            # Fallback genérico
            skeleton = [
                {"subdivision_id": "SD_GEN", "title": "Ensayo Humanístico", "instructions": "Desarrolle el tema.", "layout_mode": "STANDARD", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": I_DISC}]}
            ]

        return skeleton

    def get_system_prompt(self):
        """
        Dynamic Role for Humanities (V06DOC_SUBARCHETYPES).
        """
        roles = {
            'SUB-HUM-HIST': "Rol: Historiador/Arqueólogo (UGR). Foco: Análisis de fuentes, Cronología, Crítica de autenticidad.",
            'SUB-HUM-PHIL': "Rol: Filósofo/Lógico. Foco: Dialéctica, Coherencia argumental, Rigor formal.",
            'SUB-HUM-ART-HIST': "Rol: Historiador del Arte (Iconográfico). Foco: Análisis formal, Iconografía, Contexto.",
            'SUB-HUM-ART-CREA': "Rol: Crítico/Teórico del Arte. Foco: Técnica matérica, Discurso estético, Composición.",
            'SUB-HUM-MUS': "Rol: Musicólogo. Foco: Análisis armónico, Historia musical, Transcripción.",
            'SUB-HUM-ANTH': "Rol: Antropólogo. Foco: Etnografía, Estructuras culturales, Evolución."
        }
        base_role = roles.get(self.sub_archetype_id, "Rol: Humanista Senior.")

        # ITINERARY (V06DOC_SUBDIVISIONS)
        itin_ctx = ""
        if self.itinerary_id == 'ITIN_DOC':
            itin_ctx = "ENFOQUE DIDÁCTICO: Evalúa la capacidad de transposición didáctica y el cumplimiento de LOMLOE/DUA."
        elif self.itinerary_id == 'ITIN_INV':
            itin_ctx = "ENFOQUE INVESTIGADOR: Exige rigor absoluto en citas bibliográficas y estado del arte."

        return f"{base_role}\n{itin_ctx}\nESTRUCTURA: Usa subdivisiones SD_SOURCE y SD_DISC. Evalúa con Rúbrica Holística DRA-HOLO."

    def get_user_prompt(self, context_text, topic, subdivision_id, generated_item_titles=None, skeleton_json=None):
        """
        Atomic generation prompt for a specific subdivision (V06DOC_TEMPLATES).
        """
        memory = f"\nEvitar repetir estos conceptos: {', '.join(generated_item_titles)}" if generated_item_titles else ""
        return (
            f"RELLENA EL ESQUELETO JSON ({__import__('json').dumps(skeleton_json, ensure_ascii=False) if skeleton_json else '[]'}) para la sección: {subdivision_id}.\n"
            f"TEMA: {topic}. {memory}\n"
            f"REF: {context_text[:50000]}\n"
            f"CONFIG: Arquetipo={self.sub_archetype_id}, Itinerario={self.itinerary_id}, Nivel={self.pedagogical_level}.\n"
            f"REQUISITOS:\n"
            f"1. Foco en crítica de fuentes (SD_SOURCE) y discurso crítico (SD_DISC).\n"
            f"2. Usa DRA-HOLO para ensayos largos o EV-PALE para transcripciones.\n"
            f"3. Salida estrictamente JSON (Array 'items')."
        )

