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

        # --- MOTOR: CASO-PRÁCTICO (Exégesis Legal/Económica) ---
        if block_type == 'CASO-PRACTICO':
            # Requires citation of norms or data sources
            required_citations = logic.get('required_norms', [])
            student_text = str(student_input).lower()
            
            # Count valid citations (Rigor Factor)
            citations_found = sum(1 for norm in required_citations if norm.lower() in student_text)
            
            if self.itinerary_id == 'ITIN_PROF':
                # Professional level demands 100% citation accuracy
                if citations_found < len(required_citations):
                    return Decimal('0.3'), {"status": "INSUFFICIENT_FUNDAMENTATION", "detail": "Faltan citas legales o normativas obligatorias."}

            score = Decimal(str(citations_found / len(required_citations))) if required_citations else Decimal('1.0')
            return score, {"status": "GRADED", "citations": citations_found}

        # --- MOTOR: PRM-STRIKE (Standard) ---
        elif block_type == 'PRM-STRIKE':
            correct_answer = logic.get('correct_answer')
            if str(student_input).strip() == str(correct_answer).strip():
                return Decimal('1.0'), {"status": "CORRECT"}
            return Decimal('-0.25'), {"status": "INCORRECT"}

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
        """
        sid = self.sub_archetype_id
        skeleton = []

        # 1. SUB-SOC-LAW-PROC: Derecho Procesal
        if sid == 'SUB-SOC-LAW-PROC':
            skeleton = [
                {"subdivision_id": "SD_DEADLINES", "title": "Plazos y Recursos", "instructions": "Determine los plazos procesales aplicables.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE"}]},
                {"subdivision_id": "SD_PROC_STEP", "title": "Trámite Procesal", "instructions": "Identifique el siguiente paso en el procedimiento.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "CASO-PRACTICO", "widget_id": "W-LAW-NAV"}]}
            ]
        # 2. SUB-SOC-LAW-DICT: Dictamen Jurídico
        elif sid == 'SUB-SOC-LAW-DICT':
            skeleton = [
                {"subdivision_id": "SD_FACTS", "title": "Hechos Relevantes", "instructions": "Jerarquice los hechos del supuesto.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE"}]},
                {"subdivision_id": "SD_DICTAMEN", "title": "Dictamen Fundamentado", "instructions": "Redacte el dictamen citando jurisprudencia.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "CASO-PRACTICO", "widget_id": "W-HUM-TEXT"}]}
            ]
        # 3. SUB-SOC-ECON-QUAN: Economía Cuantitativa
        elif sid == 'SUB-SOC-ECON-QUAN':
            skeleton = [
                {"subdivision_id": "SD_DATA", "title": "Análisis de Datos", "instructions": "Interprete los indicadores económicos.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE"}]},
                {"subdivision_id": "SD_MODEL", "title": "Modelización", "instructions": "Resuelva el supuesto contable o econométrico.", "layout_mode": "STANDARD", "items": [{"block_type": "CASO-PRACTICO", "widget_id": "W-HUM-TEXT"}]}
            ]
        # 4. SUB-SOC-ECON-MGMT: Empresa / ADE
        elif sid == 'SUB-SOC-ECON-MGMT':
            skeleton = [
                {"subdivision_id": "SD_STRATEGY", "title": "Análisis Estratégico", "instructions": "Proponga una estrategia de mercado.", "layout_mode": "STANDARD", "items": [{"block_type": "CASO-PRACTICO", "widget_id": "W-HUM-TEXT"}]},
                {"subdivision_id": "SD_ORGANIZATION", "title": "Estructura Organizativa", "instructions": "Valore la eficiencia del modelo propuesto.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE"}]}
            ]
        # 5. SUB-SOC-EDU-KIDS: Magisterio (Infantil/Primaria)
        elif sid == 'SUB-SOC-EDU-KIDS':
            skeleton = [
                {"subdivision_id": "SD_DUA", "title": "Diseño Inclusivo (DUA)", "instructions": "Adapte la actividad para la diversidad.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE"}]},
                {"subdivision_id": "SD_SITUATION", "title": "Situación de Aprendizaje", "instructions": "Diseñe una secuencia didáctica original.", "layout_mode": "STANDARD", "items": [{"block_type": "CASO-PRACTICO", "widget_id": "W-HUM-TEXT"}]}
            ]
        # 6. SUB-SOC-EDU-SEC: Profesorado Secundaria
        elif sid == 'SUB-SOC-EDU-SEC':
            skeleton = [
                {"subdivision_id": "SD_NORMATIVE", "title": "Marco Legal Educativo", "instructions": "Justifique según la LOMLOE.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE"}]},
                {"subdivision_id": "SD_DIDACTIC", "title": "Transposición Didáctica", "instructions": "Planifique el desarrollo de la unidad.", "layout_mode": "STANDARD", "items": [{"block_type": "CASO-PRACTICO", "widget_id": "W-HUM-TEXT"}]}
            ]
        # 7. SUB-SOC-COMM-JOUR: Periodismo
        elif sid == 'SUB-SOC-COMM-JOUR':
            skeleton = [
                {"subdivision_id": "SD_ETHICS", "title": "Ética y Deontología", "instructions": "Valore el tratamiento informativo del caso.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE"}]},
                {"subdivision_id": "SD_WRITING", "title": "Redacción Periodística", "instructions": "Redacte la noticia o reportaje solicitado.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "CASO-PRACTICO", "widget_id": "W-HUM-TEXT"}]}
            ]
        # 8. SUB-SOC-COMM-AV: Audiovisual
        elif sid == 'SUB-SOC-COMM-AV':
            skeleton = [
                {"subdivision_id": "SD_SCRIPT", "title": "Narrativa y Guion", "instructions": "Desarrolle la escaleta o guion literario.", "layout_mode": "STANDARD", "items": [{"block_type": "CASO-PRACTICO", "widget_id": "W-HUM-TEXT"}]},
                {"subdivision_id": "SD_TECH_PROD", "title": "Técnica de Producción", "instructions": "Resuelva problemas de iluminación o sonido.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE"}]}
            ]
        # 9. SUB-SOC-GEOG: Geografía
        elif sid == 'SUB-SOC-GEOG':
            skeleton = [
                {"subdivision_id": "SD_TERRITORY", "title": "Análisis Territorial", "instructions": "Interprete los datos del SIG o cartografía.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "CASO-PRACTICO", "widget_id": "W-HUM-TEXT"}]},
                {"subdivision_id": "SD_CLIMATE", "title": "Climatología y Medio", "instructions": "Explique los fenómenos geográficos.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE"}]}
            ]
        # 10. SUB-SOC-WORK: Trabajo Social
        elif sid == 'SUB-SOC-WORK':
            skeleton = [
                {"subdivision_id": "SD_DIAGNOSIS", "title": "Diagnóstico Social", "instructions": "Identifique los indicadores de exclusión.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE"}]},
                {"subdivision_id": "SD_PLAN", "title": "Plan de Intervención", "instructions": "Diseñe la estrategia de mediación.", "layout_mode": "STANDARD", "items": [{"block_type": "CASO-PRACTICO", "widget_id": "W-HUM-TEXT"}]}
            ]
        else:
            skeleton = [
                {"subdivision_id": "SD_GEN", "title": "Análisis Social General", "instructions": "Resuelva el supuesto práctico.", "layout_mode": "STANDARD", "items": [{"block_type": "CASO-PRACTICO", "widget_id": "W-HUM-TEXT"}]}
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

        return f"{base_role}
{itin_ctx}
REGLA: Usa CASO-PRACTICO para supuestos de hecho con W-LAW-NAV o W-HUM-TEXT."


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

    def get_output_schema(self):
        """
        Atomic JSON Schema for ARCH_SOC.
        Uses anyOf for Union Types (Gemini 2.5 Safe).
        """
        return {
            "type": "object",
            "properties": {
                "section_stimulus": {"type": "string"},
                "items": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                "section_stimulus": {"type": "string"},
                "items": {
                            "block_type": {"type": "string", "enum": ["CASO-PRACTICO", "PRM-STRIKE"]},
                            "widget_id": {"type": "string", "enum": ["W-LAW-NAV", "W-OBJ-STRIKE", "W-HUM-TEXT"]},
                            "content": {
                                "type": "object",
                                "properties": {
                "section_stimulus": {"type": "string"},
                "items": {
                                    "stem": {"type": "string"},
                                    "case_data": {"type": "object"},
                                    "options": {"type": "array", "items": {"type": "string"}}
                                },
                                "required": ["stem"]
                            },
                            "grading_logic": {
                                "type": "object",
                                "properties": {
                "section_stimulus": {"type": "string"},
                "items": {
                                    "correct_answer": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "number"}
                                        ]
                                    },
                                    "required_norms": {"type": "array", "items": {"type": "string"}}
                                }
                            },
                            "metadata": {
                                "type": "object",
                                "properties": {
                "section_stimulus": {"type": "string"},
                "items": {
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
