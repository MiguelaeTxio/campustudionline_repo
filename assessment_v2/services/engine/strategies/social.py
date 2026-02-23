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

    def get_system_prompt(self):
        """
        Dynamic Role for Social/Legal (V06DOC_SUBARCHETYPES).
        """
        roles = {
            'SUB-SOC-JUR': "Rol: Magistrado/Abogado Senior. Foco: Exégesis legal, Jurisprudencia, Técnica procesal.",
            'SUB-SOC-ECON': "Rol: Auditor/Economista. Foco: Análisis cuantitativo, Contabilidad, Modelos econométricos.",
            'SUB-SOC-BEHAV': "Rol: Sociólogo/Analista Político. Foco: Teoría del estado, Análisis de datos sociales.",
            'SUB-SOC-COMM': "Rol: Consultor de Comunicación/SEO. Foco: Estrategia de medios, Gestión de información."
        }
        base_role = roles.get(self.sub_archetype_id, "Rol: Académico de Ciencias Sociales.")

        # ITINERARY (V06DOC_SUBDIVISIONS)
        if self.itinerary_id == 'ITIN_PROF':
            context = "OBJETIVO: Dictamen Profesional. Exige rigor en la cita de la norma (BOE/Jurisprudencia) o viabilidad económica."
        else:
            context = "OBJETIVO: Especialización Académica. Foco en fundamentos teóricos y análisis crítico."

        return f"{base_role}\n{context}\nESTRUCTURA: Usa subdivisiones SD_FACT, SD_NORM y SD_PROC."

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
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "block_type": {"type": "string", "enum": ["CASO-PRACTICO", "PRM-STRIKE"]},
                            "widget_id": {"type": "string", "enum": ["W-LAW-NAV", "W-OBJ-STRIKE", "W-HUM-TEXT"]},
                            "content": {
                                "type": "object",
                                "properties": {
                                    "stem": {"type": "string"},
                                    "case_data": {"type": "object"},
                                    "options": {"type": "array", "items": {"type": "string"}}
                                },
                                "required": ["stem"]
                            },
                            "grading_logic": {
                                "type": "object",
                                "properties": {
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
