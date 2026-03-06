# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/social.py
from .base import BaseExamStrategy
from decimal import Decimal
import json

class SocialStrategy(BaseExamStrategy):
    """
    Strategy for Social and Legal Sciences (ARCH_SOC).
    Fully compliant with Casuistic model and V06DOC_SUBARCHETYPES.
    
    COVERS:
    - 4 Sub-archetypes (JUR, ECON, BEHAV, COMM).
    - Itineraries: PROF (Executive/Dictamen), MAI, MIN.
    - Widgets: W-LAW-NAV, W-OBJ-STRIKE, W-HUM-TEXT.
    """

    def grade_item(self, item, student_input):
        """
        Grades social/legal items. Focus on 'Encuadre Normativo' and 'Fundamentación'.
        """
        logic = item.grading_logic
        block_type = item.block_type

        # --- MOTOR: DRA-HOLO (Exégesis Legal/Económica) ---
        if block_type == 'DRA-HOLO':
            # Requires citation of norms or data sources
            required_citations = logic.get('required_norms', [])
            student_text = str(student_input).lower()
            
            # Count valid citations (Rigor Factor)
            citations_found = sum(1 for norm in required_citations if norm.lower() in student_text)
            
            # [HITO 6 FIX] Incidencia 60: Multiplicador de Fuentes Reales
            real_sources_multiplier = Decimal('1.2') if citations_found > 0 else Decimal('1.0')

            if self.itinerary_id == 'ITIN_PROF':
                # Professional level demands 100% citation accuracy
                if citations_found < len(required_citations):
                    return Decimal('0.3'), {"status": "INSUFFICIENT_FUNDAMENTATION", "detail": "Faltan citas legales o normativas obligatorias."}

            score = (Decimal(str(citations_found / len(required_citations))) * real_sources_multiplier) if required_citations else Decimal('1.0')
            score = min(score, Decimal('1.0'))
            return score, {"status": "GRADED", "citations": citations_found, "real_sources_multiplier": float(real_sources_multiplier)}

        # --- MOTOR: PRM-STRIKE (Standard) ---
        elif block_type == 'PRM-STRIKE':
            correct_answer = logic.get('correct_answer')
            if str(student_input).strip() == str(correct_answer).strip():
                return Decimal('1.0'), {"status": "CORRECT"}
            # [HITO 6 FIX] Penalización dinámica según V06DOC_LEVELS
            penalty = logic.get('penalty', Decimal('-0.25'))
            return Decimal(str(penalty)), {"status": "INCORRECT", "penalty_applied": True}

        # --- MOTOR: JUDICIAL-SIM (Simulación de Juicio/Procedimiento) ---
        # Ref: V06DOC_BLOCKS (Incidencia 40)
        elif block_type == 'JUDICIAL-SIM':
            # Input esperado: { "procedural_stage": "...", "admitted_evidence": [...], "verdict": "..." }
            if not isinstance(student_input, dict):
                 return Decimal('0.0'), {"status": "FORMAT_ERROR"}
            
            # 1. Validación de Fase Procesal (20%)
            correct_stage = logic.get('correct_stage')
            student_stage = student_input.get('procedural_stage')
            score_stage = Decimal('0.2') if str(student_stage).lower() == str(correct_stage).lower() else Decimal('0.0')

            # 2. Admisibilidad de Prueba (40%)
            required_evidence = logic.get('admissible_evidence', [])
            student_evidence = student_input.get('admitted_evidence', [])
            matches = sum(1 for ev in required_evidence if ev in student_evidence)
            score_evidence = (Decimal(matches) / Decimal(len(required_evidence))) * Decimal('0.4') if required_evidence else Decimal('0.4')

            # 3. Veredicto/Fallo (40%)
            correct_verdict = logic.get('correct_verdict')
            student_verdict = student_input.get('verdict')
            is_verdict_correct = str(student_verdict).lower() == str(correct_verdict).lower()
            
            if is_verdict_correct:
                score_verdict = Decimal('0.4')
            else:
                score_verdict = Decimal('0.0')
                # Penalización crítica en Itinerario Profesional
                if self.itinerary_id == 'ITIN_PROF':
                    return Decimal('0.0'), {
                        "status": "WRONG_VERDICT",
                        "feedback_category": "FB_CONCEPT",
                        "detail": "Fallo judicial erróneo. Error fatal en simulación profesional."
                    }

            total_score = score_stage + score_evidence + score_verdict
            return total_score, {
                "status": "GRADED",
                "stage_ok": score_stage > 0,
                "evidence_ratio": f"{matches}/{len(required_evidence)}",
                "verdict_ok": is_verdict_correct
            }

        return Decimal('0.0'), {"status": "PENDING_MANUAL_REVIEW"}

    def get_section_plan(self):
        """
        Returns the mandatory section list for the orchestrator (SKELETON-FIRST).
        Ref: V06DOC_ARCHETYPES.
        """
        return [
            {
                "subdivision_id": "SD_FACT",
                "title": "Hechos y Datos Relevantes",
                "instructions": "Identifica y jerarquiza los hechos probados o datos clave del supuesto.",
                "time_limit": 600
            },
            {
                "subdivision_id": "SD_NORM",
                "title": "Encuadre Normativo / Legal",
                "instructions": "Localiza y cita la normativa, jurisprudencia o marco teórico aplicable.",
                "time_limit": 900
            },
            {
                "subdivision_id": "SD_PROC",
                "title": "Propuesta de Resolución / Trámite",
                "instructions": "Redacta la propuesta de resolución, dictamen o trámite procesal fundamentado.",
                "time_limit": 1200
            }
        ]

    def get_exam_skeleton(self):
        """
        Returns the structural skeleton for the 10 Social/Legal models.
        Ref: V06DOC_SUBARCHETYPES V5.0.
        Refactor: DRY & Prompt Binding implemented.
        """
        sid = self.sub_archetype_id
        skeleton = []

        # 1. INSTRUCCIONES BASE (DRY)
        I_PRM_GENERIC = "Genera una pregunta de opción múltiple (4 opciones) sobre conceptos fundamentales."
        I_CASO_GENERIC = "Genera un supuesto práctico detallado. El alumno debe redactar una solución fundamentada."
        I_LAW_NAV = "Genera un ejercicio de búsqueda legislativa o jurisprudencial simulada."

        # 2. DEFINICIONES ESPECÍFICAS (OVERRIDES)
        I_PRM = I_PRM_GENERIC
        I_CASO = I_CASO_GENERIC

        if sid in ["SUB-SOC-LAW-PROC", "SUB-SOC-LAW-DICT"]:
            I_PRM = "Genera una pregunta sobre plazos procesales, recursos o hechos probados."
            I_CASO = "Redacte un dictamen jurídico o propuesta de resolución citando normativa aplicable."
        elif sid in ["SUB-SOC-ECON-QUAN", "SUB-SOC-ECON-MGMT"]:
            I_PRM = "Genera una pregunta sobre interpretación de indicadores económicos o estructura organizativa."
            I_CASO = "Resuelva el supuesto contable, econométrico o de estrategia de mercado."
        elif sid in ["SUB-SOC-EDU-KIDS", "SUB-SOC-EDU-SEC"]:
            I_PRM = "Genera una pregunta sobre normativa educativa (LOMLOE), DUA o didáctica."
            I_CASO = "Diseñe una situación de aprendizaje o unidad didáctica justificando la metodología."
        elif sid == "SUB-SOC-COMM-JOUR":
            I_CASO = "Redacte una noticia, crónica o reportaje siguiendo las normas de estilo y deontología."

        # 3. CONSTRUCCIÓN DEL ESQUELETO

        # 1. SUB-SOC-LAW-PROC
        if sid == "SUB-SOC-LAW-PROC":
            skeleton = [
                {"subdivision_id": "SD_DEADLINES", "title": "Plazos y Recursos", "instructions": "Determine los plazos procesales aplicables.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": I_PRM}]},
                {"subdivision_id": "SD_PROC_STEP", "title": "Trámite Procesal", "instructions": "Identifique el siguiente paso en el procedimiento.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-LAW-NAV", "task_instruction": I_LAW_NAV}]}
            ]
        # 2. SUB-SOC-LAW-DICT
        elif sid == "SUB-SOC-LAW-DICT":
            skeleton = [
                {"subdivision_id": "SD_FACTS", "title": "Hechos Relevantes", "instructions": "Jerarquice los hechos del supuesto.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": I_PRM}]},
                {"subdivision_id": "SD_DICTAMEN", "title": "Dictamen Fundamentado", "instructions": "Redacte el dictamen citando jurisprudencia.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": I_CASO}]}
            ]
        # 3. SUB-SOC-ECON-QUAN
        elif sid == "SUB-SOC-ECON-QUAN":
            skeleton = [
                {"subdivision_id": "SD_DATA", "title": "Análisis de Datos", "instructions": "Interprete los indicadores económicos.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": I_PRM}]},
                {"subdivision_id": "SD_MODEL", "title": "Modelización", "instructions": "Resuelva el supuesto contable o econométrico.", "layout_mode": "STANDARD", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": I_CASO}]}
            ]
        # 4. SUB-SOC-ECON-MGMT
        elif sid == "SUB-SOC-ECON-MGMT":
            skeleton = [
                {"subdivision_id": "SD_STRATEGY", "title": "Análisis Estratégico", "instructions": "Proponga una estrategia de mercado.", "layout_mode": "STANDARD", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": I_CASO}]},
                {"subdivision_id": "SD_ORGANIZATION", "title": "Estructura Organizativa", "instructions": "Valore la eficiencia del modelo propuesto.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": I_PRM}]}
            ]
        # 5. SUB-SOC-EDU-KIDS
        elif sid == "SUB-SOC-EDU-KIDS":
            skeleton = [
                {"subdivision_id": "SD_DUA", "title": "Diseño Inclusivo (DUA)", "instructions": "Adapte la actividad para la diversidad.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": I_PRM}]},
                {"subdivision_id": "SD_SITUATION", "title": "Situación de Aprendizaje", "instructions": "Diseñe una secuencia didáctica original.", "layout_mode": "STANDARD", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": I_CASO}]}
            ]
        # 6. SUB-SOC-EDU-SEC
        elif sid == "SUB-SOC-EDU-SEC":
            skeleton = [
                {"subdivision_id": "SD_NORMATIVE", "title": "Marco Legal Educativo", "instructions": "Justifique según la LOMLOE.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": I_PRM}]},
                {"subdivision_id": "SD_DIDACTIC", "title": "Transposición Didáctica", "instructions": "Planifique el desarrollo de la unidad.", "layout_mode": "STANDARD", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": I_CASO}]}
            ]
        # 7. SUB-SOC-COMM-JOUR
        elif sid == "SUB-SOC-COMM-JOUR":
            skeleton = [
                {"subdivision_id": "SD_ETHICS", "title": "Ética y Deontología", "instructions": "Valore el tratamiento informativo del caso.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Genera una pregunta sobre ética periodística o verificación de fuentes."}]},
                {"subdivision_id": "SD_WRITING", "title": "Redacción Periodística", "instructions": "Redacte la noticia o reportaje solicitado.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": I_CASO}]}
            ]
        # 8. SUB-SOC-COMM-AV
        elif sid == "SUB-SOC-COMM-AV":
            skeleton = [
                {"subdivision_id": "SD_SCRIPT", "title": "Narrativa y Guion", "instructions": "Desarrolle la escaleta o guion literario.", "layout_mode": "STANDARD", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": "Genera un ejercicio de redacción de guion (literario o técnico) o escaleta."}]},
                {"subdivision_id": "SD_TECH_PROD", "title": "Técnica de Producción", "instructions": "Resuelva problemas de iluminación o sonido.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Genera una pregunta técnica sobre equipos, formatos, iluminación o sonido."}]}
            ]
        # 9. SUB-SOC-GEOG
        elif sid == "SUB-SOC-GEOG":
            skeleton = [
                {"subdivision_id": "SD_TERRITORY", "title": "Análisis Territorial", "instructions": "Interprete los datos del SIG o cartografía.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": "Genera un ejercicio de interpretación de mapa, pirámide poblacional o datos SIG."}]},
                {"subdivision_id": "SD_CLIMATE", "title": "Climatología y Medio", "instructions": "Explique los fenómenos geográficos.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Genera una pregunta sobre procesos climáticos, geomorfología o demografía."}]}
            ]
        # 10. SUB-SOC-WORK
        elif sid == "SUB-SOC-WORK":
            skeleton = [
                {"subdivision_id": "SD_DIAGNOSIS", "title": "Diagnóstico Social", "instructions": "Identifique los indicadores de exclusión.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Genera una pregunta sobre indicadores de riesgo social, leyes de dependencia o recursos comunitarios."}]},
                {"subdivision_id": "SD_PLAN", "title": "Plan de Intervención", "instructions": "Diseñe la estrategia de mediación.", "layout_mode": "STANDARD", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": "Genera un supuesto de intervención social familiar o comunitario. El alumno debe proponer el plan de acción."}]}
            ]
        else:
            skeleton = [
                {"subdivision_id": "SD_GEN", "title": "Análisis Social General", "instructions": "Resuelva el supuesto práctico.", "layout_mode": "STANDARD", "items": [{"block_type": "DRA-HOLO", "widget_id": "W-HUM-TEXT", "task_instruction": I_CASO}]},
                {"subdivision_id": "SD_ETHI", "title": "Deontología y Ética", "instructions": "Valore las implicaciones éticas.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Genera una pregunta sobre ética profesional o código deontológico."}]}
            ]

        return skeleton

    def get_system_prompt(self):
        """
        Generates roles based on the 10 Social/Legal Sub-Archetypes (V5.0).
        """
        roles = {
            'SUB-SOC-LAW-PROC': "Rol: Letrado de la Adm. de Justicia. Foco: Técnica Procesal, Plazos y Recursos.",
            'SUB-SOC-LAW-DICT': "Rol: Magistrado / Consultor Jurídico. Foco: Dictamen, Jurisprudencia y Ley.",
            'SUB-SOC-ECON-QUAN': "Rol: Econometrista / Analista Financiero. Foco: Contabilidad y Modelos Cuantitativos.",
            'SUB-SOC-ECON-MGMT': "Rol: Consultor de Estrategia (ADE). Foco: Organización, Marketing y Management.",
            'SUB-SOC-EDU-KIDS': "Rol: Maestro/a (Infantil/Primaria). Foco: DUA, Situaciones de Aprendizaje y Didáctica.",
            'SUB-SOC-EDU-SEC': "Rol: Catedrático de Secundaria. Foco: Didáctica Específica y Normativa Educativa.",
            'SUB-SOC-COMM-JOUR': "Rol: Redactor Jefe / Periodista. Foco: Ética Informativa, Géneros y Redacción.",
            'SUB-SOC-COMM-AV': "Rol: Realizador / Guionista AV. Foco: Narrativa visual y Técnica de Producción.",
            'SUB-SOC-GEOG': "Rol: Geógrafo / Analista SIG. Foco: Análisis Territorial y Climatología.",
            'SUB-SOC-WORK': "Rol: Trabajador Social. Foco: Intervención Social y Mediación Comunitaria."
        }
        base_role = roles.get(self.sub_archetype_id, "Rol: Especialista en Ciencias Sociales.")
        itin_ctx = "CONTEXTO PROFESIONAL: Exige rigor en la cita normativa y viabilidad técnica." if self.itinerary_id == 'ITIN_PROF' else ""

        return f"""{base_role}
{itin_ctx}
REGLA: Usa CASO-PRACTICO para supuestos de hecho con W-LAW-NAV o W-HUM-TEXT."""


    def get_user_prompt(self, context_text, topic, subdivision_id, generated_item_titles=None):
        """
        Atomic generation prompt for a specific subdivision (V06DOC_TEMPLATES).
        """
        memory = f"\nEvitar repetir estos conceptos: {', '.join(generated_item_titles)}" if generated_item_titles else ""
        return (
            f"GENERA 3 ÍTEMS para la sección: {subdivision_id}.\n"
            f"TEMA: {topic}. {memory}\n"
            f"REF: {context_text[:50000]}\n"
            f"CONFIG: Arquetipo={self.sub_archetype_id}, Itinerario={self.itinerary_id}, Nivel={self.pedagogical_level}.\n"
            f"REQUISITOS:\n"
            f"1. Crea un Caso Práctico que involucre datos reales o disputas legales.\n"
            f"2. Usa W-LAW-NAV para simulaciones de búsqueda legal si el sub-arquetipo es JUR.\n"
            f"3. Salida estrictamente JSON (Array 'items')."
        )

