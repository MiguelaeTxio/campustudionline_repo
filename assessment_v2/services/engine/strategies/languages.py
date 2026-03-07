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
            # [HITO 6 FIX] Soporte para multirrespuesta Array vs String (Incidencia 12)
            raw_correct = logic.get("correct_answer", "")
            valid_answers = [str(a).lower().strip() for a in raw_correct] if isinstance(raw_correct, list) else [str(raw_correct).lower().strip()]
            student_answer = str(student_input).lower().strip()
            
            if student_answer in valid_answers:
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
        elif block_type == "BMT-SHIFT":
            # [HITO 6 FIX] Incidencia 59: Motor de Mediación y Transferencia
            student_text = str(student_input).strip()
            if not student_text:
                return Decimal("0.0"), {"status": "OMITTED"}
            word_count = len(student_text.split())
            return min(Decimal(str(word_count / 100.0)), Decimal("1.0")), {"status": "GRADED", "word_count": word_count, "feedback_category": "FB_PROCEDURAL"}

        elif block_type == "DRA-HOLO":
            # [HITO 6 FIX] Incidencia 59: Implementación de Motor DRA-HOLO
            student_text = str(student_input).strip()
            if not student_text:
                return Decimal("0.0"), {"status": "OMITTED"}
            word_count = len(student_text.split())
            return min(Decimal(str(word_count / 150.0)), Decimal("1.0")), {"status": "GRADED", "word_count": word_count, "feedback_category": "FB_FORMAL"}

        return Decimal("0.0"), {"status": "PENDING"}

    def get_immersion_mode(self):
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
        mode = self.get_immersion_mode()
        loc_secs = self.config.get('localized_sections', {})
        
        # Estructura de mapeo para inmersión UGR
        sections_data = [
            {
                "id": "SD_READ", 
                "veh": "Comprensión Lectora", "tar": loc_secs.get("SD_READ", {}).get("title", "Reading Comprehension"),
                "i_veh": "Lee el texto y resuelve los desafíos lingüísticos.", "i_tar": loc_secs.get("SD_READ", {}).get("instructions", "Read the text and solve the linguistic challenges.")
            },
            {
                "id": "SD_LIST", 
                "veh": "Comprensión Auditiva", "tar": loc_secs.get("SD_LIST", {}).get("title", "Listening Comprehension"),
                "i_veh": "Analiza las transcripciones de audio e identifica matices semánticos.", "i_tar": loc_secs.get("SD_LIST", {}).get("instructions", "Analyze the audio transcripts and identify semantic nuances.")
            },
            {
                "id": "SD_WRIT", 
                "veh": "Producción Escrita", "tar": loc_secs.get("SD_WRIT", {}).get("title", "Written Production"),
                "i_veh": "Produce un texto académico respetando el registro formal.", "i_tar": loc_secs.get("SD_WRIT", {}).get("instructions", "Produce an academic text respecting formal register.")
            },            {
                "id": "SD_SPEAK", 
                "veh": "Expresión Oral", "tar": loc_secs.get("SD_SPEAK", {}).get("title", "Speaking"),
                "i_veh": "Interacción fluida evaluada mediante el módulo UniversIA.", "i_tar": loc_secs.get("SD_SPEAK", {}).get("instructions", "Fluent interaction evaluated via the UniversIA module.")
            },

            {
                "id": "SD_MEDI", 
                "veh": "Mediación Lingüística", "tar": loc_secs.get("SD_MEDI", {}).get("title", "Linguistic Mediation"),
                "i_veh": "Sintetiza y adapta información entre diferentes registros.", "i_tar": loc_secs.get("SD_MEDI", {}).get("instructions", "Synthesize and adapt information between different registers.")
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


    def get_exam_skeleton(self):
        """
        Returns the structural skeleton for the 6 UGR Language models.
        Ref: V06DOC_SUBARCHETYPES V5.0.
        """
        sid = self.sub_archetype_id
        skeleton = []

        # 1. SUB-LIN-INSTR: Modelo Instrumental (B1/C1 - 5 Destrezas)
        if sid in ["SUB-LIN-INSTR", "SUB-LIN-CERT"]:
            plan = self.get_section_plan()
            for sec in plan:
                sec["layout_mode"] = "SPLIT_TEXT" if sec["subdivision_id"] == "SD_READ" else "STANDARD"
                if sec["subdivision_id"] == "SD_READ":
                    sec["items"] = [{"block_type": "CLO-MULTI", "widget_id": "W-TXT-CLOZE", "task_instruction": "Genera un texto con huecos a rellenar (CLO-MULTI) evaluando comprensión lectora y léxico."}]
                elif sec["subdivision_id"] == "SD_LIST":
                    sec["items"] = [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Genera preguntas de opción múltiple basadas en la transcripción de audio (PRM-STRIKE)."}]
                elif sec["subdivision_id"] == "SD_WRIT":
                    sec["layout_mode"] = "SPLIT_TEXT"
                    sec["items"] = [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": "Plantea un tema de redacción académica (ensayo/artículo) que requiera registro formal (DRA-HOLO)."}]
                # [HITO 6 FIX] Discrepancia 2: Widget correcto para Speaking (DIA-INTERACT)
                elif sec["subdivision_id"] == "SD_SPEAK":
                    sec["items"] = [{"block_type": "DIA-INTERACT", "widget_id": "W-COMM-DIALOG", "task_instruction": "Inicia una simulación de entrevista oral interactiva (UniversIA)."}]
                else:
                    sec["items"] = [{"block_type": "CLO-OPEN", "widget_id": "W-TXT-CLOZE", "task_instruction": "Genera un texto con huecos abiertos sin opciones (CLO-OPEN) para evaluar precisión léxico-gramatical."}]
                skeleton.append(sec)

        # 2. SUB-LIN-MINOR: Modelo Iniciación (Chino/Ruso Minor)
        elif sid == "SUB-LIN-MINOR":
            skeleton = [
                {"subdivision_id": "SD_WRIT", "title": "Grafía y Dictado", "instructions": "Escriba los caracteres/términos dictados.", "layout_mode": "STANDARD", "items": [{"block_type": "RBT-CANON", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Genera un ejercicio de reconocimiento de grafías o caracteres (RBT-CANON)."}]},
                {"subdivision_id": "SD_READ", "title": "Estructuras Básicas", "instructions": "Complete las oraciones gramaticales.", "layout_mode": "STANDARD", "items": [{"block_type": "CLO-MULTI", "widget_id": "W-TXT-CLOZE", "task_instruction": "Genera oraciones con huecos a rellenar evaluando gramática básica (CLO-MULTI)."}]},
                {"subdivision_id": "SD_MEDI", "title": "Cultura y Civilización", "instructions": "Responda sobre el contexto socio-cultural.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Genera preguntas de opción múltiple sobre cultura y civilización del idioma (PRM-STRIKE)."}]}
            ]

        # 3. SUB-LIN-PHILO: Modelo Filológico (Historia de la Lengua)
        elif sid == "SUB-LIN-PHILO":
            skeleton = [
                {"subdivision_id": "SD_SOURCE", "title": "Gramática Histórica", "instructions": "Analice la evolución fonética de los étimos.", "layout_mode": "STANDARD", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": "Genera un ejercicio de análisis de evolución fonética de étimos."}]},
                {"subdivision_id": "SD_LIST", "title": "Análisis Fonético", "instructions": "Transcriba y analice los rasgos fonológicos.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "CLO-OPEN", "widget_id": "W-TXT-CLOZE", "task_instruction": "Genera un texto para transcripción y análisis de rasgos fonológicos."}]}
            ]

        # 4. SUB-LIN-NORM: Modelo Norma y Uso (Español Actual)
        elif sid == "SUB-LIN-NORM":
            skeleton = [
                {"subdivision_id": "SD_READ", "title": "Análisis de Desviaciones", "instructions": "Identifique y corrija errores de norma.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "CLO-MULTI", "widget_id": "W-TXT-CLOZE", "task_instruction": "Genera un texto con errores normativos para identificar y corregir."}]},
                {"subdivision_id": "SD_DISC", "title": "Exégesis Normativa", "instructions": "Justifique el uso según la normativa académica.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": "Genera un caso de exégesis normativa para justificar el uso académico."}]}
            ]

        # 5. SUB-LIN-TRA-TECH: Traducción Técnica
        elif sid in ["SUB-LIN-TRA-TECH", "SUB-LIN-PROF"]:
            skeleton = [
                {"subdivision_id": "SD_READ", "title": "Glosario Terminológico", "instructions": "Vincule los términos técnicos con su equivalente.", "layout_mode": "STANDARD", "items": [{"block_type": "MAT-LINK", "widget_id": "W-MIX-MATCH", "task_instruction": "Genera un glosario de términos técnicos para vincular con su equivalente."}]},
                {"subdivision_id": "SD_MEDI", "title": "Traducción Técnica", "instructions": "Traduzca el texto manteniendo la precisión.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": "Proporciona un texto técnico complejo para su traducción precisa."}]}
            ]

        # 6. SUB-LIN-TRA-LIT: Traducción Literaria
        elif sid in ["SUB-LIN-TRA-LIT", "SUB-LIN-LIT"]:
            skeleton = [
                {"subdivision_id": "SD_READ", "title": "Análisis Estilístico", "instructions": "Identifique los rasgos de estilo del autor.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "CLO-MULTI", "widget_id": "W-TXT-CLOZE", "task_instruction": "Genera un texto literario con huecos para identificar rasgos de estilo."}]},
                {"subdivision_id": "SD_MEDI", "title": "Traducción Literaria", "instructions": "Traduzca preservando la carga estética.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": "Proporciona un texto literario para traducir preservando su carga estética."}]}
            ]

        return skeleton

    def get_system_prompt(self):
        """
        Returns the specific system prompt for the academic archetype.

        Devuelve el prompt de sistema específico para el arquetipo académico.
        """
        roles = {
            "SUB-LIN-INSTR": "Examinador CertAccles/MCER. Foco: Estandarización, Gramática y 5 Destrezas.",
            "SUB-LIN-MINOR": "Profesor de Iniciación. Foco: Grafía, Gramática base y Cultura.",
            "SUB-LIN-PHILO": "Filólogo Histórico. Foco: Gramática histórica, Fonética y Evolución lingüística.",
            "SUB-LIN-NORM": "Académico de la Lengua. Foco: Análisis de desviaciones, normativa y exégesis técnica.",
            "SUB-LIN-TRA-TECH": "Experto en LSP (Language for Specific Purposes). Foco: Glosarios y Traducción Profesional.",
            "SUB-LIN-TRA-LIT": "Crítico Literario / Traductor. Foco: Estilística comparada y crítica de traducción."
        }
        base_role = roles.get(self.sub_archetype_id, "Profesor de Lenguas.")
        mode = self.get_immersion_mode()
        target_lang = self.config.get('target_language_code', 'es') if hasattr(self, 'config') else 'es'
        
        return (
            f"IDENTIDAD: {base_role}\n"
            f"IDIOMA OBJETIVO (ISO): {target_lang}\n"
            f"MODO DE INMERSIÓN: {mode}. Si es TOTAL, genera TODA la salida en el idioma '{target_lang}'.\n"
            f"REGLA CRÍTICA: Sin explicaciones. Solo el JSON atómico."
        )

    def get_user_prompt(self, context_text, topic, subdivision_id, generated_item_titles=None, skeleton_json=None):
        """
        Atomic generation prompt for a specific subdivision with context memory.

        Prompt de generación atómica para una subdivisión específica con memoria de contexto.
        """
        memory = "\nEVITA REPETICIÓN: " + ", ".join(generated_item_titles) if generated_item_titles else ""
        skeleton_instruction = f"\nESQUELETO A RELLENAR:\n{skeleton_json}\n(Debes devolver EXACTAMENTE estos ítems conservando intacto su 'item_id').\n" if skeleton_json else "\n(Asegúrate de incluir el 'item_id' proporcionado para cada ítem).\n"
        return (
            f"ACTÚA COMO MOTOR DE RENDERIZADO DE CONTENIDO (Patrón Skeleton-First).\n"
            f"Tu ÚNICA función es rellenar el contenido de los ítems solicitados en la sección: {subdivision_id}.\n"
            f"TEMA: {topic}. NIVEL: {self.pedagogical_level}.{memory}\n"
            f"CONTEXTO DOCENTE:\n{(context_text or '')[:15000]}\n"
            f"{skeleton_instruction}"
            f"CONFIG: Arquetipo={self.sub_archetype_id}, Itinerario={self.itinerary_id}, Modo={self.get_immersion_mode()}.\n"
            f"SALIDA: JSON estricto (Array 'items'). NO inventes ítems nuevos, rellena solo los solicitados."
        )

