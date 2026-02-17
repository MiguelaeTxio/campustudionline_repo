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
                    return Decimal('0.3'), {"status": "INSUFFICIENT_FUNDAMENTATION", "detail": "Missing mandatory legal/normative citations."}

            score = Decimal(str(citations_found / len(required_citations))) if required_citations else Decimal('1.0')
            return score, {"status": "GRADED", "citations": citations_found}

        # --- MOTOR: PRM-STRIKE (Standard) ---
        elif block_type == 'PRM-STRIKE':
            correct_answer = logic.get('correct_answer')
            if student_input == correct_answer:
                return Decimal('1.0'), {"status": "CORRECT"}
            return Decimal('-0.25'), {"status": "INCORRECT"}

        return Decimal('0.0'), {"status": "PENDING_MANUAL_REVIEW"}

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

    def get_user_prompt(self, context_text, topic):
        return (
            f"GENERATE SOCIAL/LEGAL EXAM.\n"
            f"TOPIC: {topic}\n"
            f"REF: {context_text[:50000]}\n"
            f"CONFIG: Sub-Arch={self.sub_archetype_id}, Itin={self.itinerary_id}, Level={self.pedagogical_level}.\n"
            f"REQUIREMENTS:\n"
            f"1. Create a Case Study involving real-world data or legal disputes.\n"
            f"2. Use W-LAW-NAV for legal search simulations if JUR.\n"
            f"3. Output JSON with subdivision_sequence."
        )

    def get_output_schema(self):
        return {
            "subdivision_sequence": [
                {
                    "subdivision_id": "SD_FACT | SD_NORM | SD_PROC | SD_ETHI",
                    "title": "string",
                    "items": [
                        {
                            "block_type": "CASO-PRACTICO | PRM-STRIKE",
                            "widget_id": "W-LAW-NAV | W-OBJ-STRIKE | W-HUM-TEXT",
                            "content": {"stem": "string", "case_data": "dict"},
                            "grading_logic": {"correct_answer": "any", "required_norms": ["list"]},
                            "metadata": {"competency_tag": "COMP_PROF | COMP_ESP"}
                        }
                    ]
                }
            ]
        }

    def generate_structure(self, exam_uuid, sub_archetype_id='SUB-SOC-JUR'):
        contract = self.generate_contract_skeleton(exam_uuid, 'ARCH_SOC', sub_archetype_id)
        contract["subdivision_sequence"] = [
            {"subdivision_id": "SD_FACT", "title": "Hechos y Datos Relevantes", "items": []},
            {"subdivision_id": "SD_NORM", "title": "Encuadre Normativo / Legal", "items": []},
            {"subdivision_id": "SD_PROC", "title": "Propuesta de Resolución / Trámite", "items": []}
        ]
        return contract
