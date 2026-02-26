# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/science.py
from .base import BaseExamStrategy
from decimal import Decimal

class ScienceStrategy(BaseExamStrategy):
    """
    Strategy for Pure Sciences (ARCH_SCI).
    Fully compliant with the Technical/Resolutive model for sciences and V06DOC_SUBARCHETYPES.
    
    COVERS:
    - 6 Sub-archetypes (BIO, CHEM, PHYS, GEOL, ENV, DATA).
    - Blocks: PRM-STRIKE (Objective), RPP-TRAZA (Multistep calculation), ILC-CONTEXT (Data interp).
    - Itineraries: MAI, MIN, PROF, INV.
    - Widgets: W-OBJ-STRIKE, W-TECH-CALC.
    """

    def grade_item(self, item, student_input):
        """
        Grades science items using deterministic/objective logic.
        """
        logic = item.grading_logic
        block_type = item.block_type

        # --- MOTOR 1: RPP-TRAZA (Cálculo Multietapa) ---
        if block_type == 'RPP-TRAZA':
            steps = student_input.get('steps', []) if isinstance(student_input, dict) else[]
            if not steps:
                return Decimal('0.0'), {"status": "NO_STEPS_PROVIDED"}
            return Decimal('0.0'), {"status": "PENDING_AI_EVALUATION", "detail": "Requiere IA para validar el arrastre de error lógico."}
        
        # --- MOTOR 2: PRM-STRIKE (Test Objetivo) ---
        elif block_type == 'PRM-STRIKE':
            correct = logic.get('correct_answer')
            if str(student_input).strip() == str(correct).strip():
                return Decimal('1.0'), {"status": "CORRECT"}
            return Decimal('-0.33'), {"status": "INCORRECT", "penalty_applied": True}

        # --- MOTOR 3: ILC-CONTEXT (Interpretación de Datos) ---
        elif block_type == 'ILC-CONTEXT':
            return Decimal('0.0'), {"status": "PENDING_AI_RUBRIC", "detail": "Evaluación cualitativa de interpretación de datos/gráficos."}

        return Decimal('0.0'), {"status": "PENDING_MANUAL_REVIEW"}

    def get_section_plan(self):
        """
        Returns the mandatory section list for the orchestrator (SKELETON-FIRST).
        Ref: V06DOC_ARCHETYPES.
        """
        return[
            {
                "subdivision_id": "SD_THEO",
                "title": "Fundamentos y Validación Teórica",
                "instructions": "Responda a las cuestiones teóricas y justifique los principios fundamentales de la disciplina.",
                "time_limit": 1200,
                "layout_mode": "STANDARD"
            },
            {
                "subdivision_id": "SD_CALC",
                "title": "Resolución de Problemas y Modelado",
                "instructions": "Desarrolle el cálculo paso a paso o interprete los datos del caso práctico. Se evaluará el planteamiento lógico.",
                "time_limit": 2400,
                "layout_mode": "SPLIT_TEXT"
            }
        ]

    def get_system_prompt(self):
        """
        Dynamic Role for Sciences (V06DOC_SUBARCHETYPES).
        """
        roles = {
            'SUB-SCI-BIO': "Rol: Catedrático de Biología. Foco: Taxonomía, Ecología, Genética.",
            'SUB-SCI-CHEM': "Rol: Catedrático de Química. Foco: Síntesis, Química inorgánica y orgánica pura.",
            'SUB-SCI-PHYS': "Rol: Catedrático de Física. Foco: Mecánica cuántica, Electromagnetismo, Rigor analítico.",
            'SUB-SCI-GEOL': "Rol: Geólogo/Catedrático. Foco: Mineralogía, Estratigrafía, Cartografía.",
            'SUB-SCI-ENV': "Rol: Ambientólogo/Ecólogo. Foco: Gestión de residuos, Contaminación, Impacto ambiental.",
            'SUB-SCI-DATA': "Rol: Data Scientist/Estadístico. Foco: IA, Big Data, Estadística computacional."
        }
        base_role = roles.get(self.sub_archetype_id, "Rol: Científico Senior.")

        # ITINERARY (V06DOC_SUBDIVISIONS)
        itin_ctx = ""
        if self.itinerary_id == 'ITIN_INV':
            itin_ctx = "ENFOQUE INVESTIGADOR: Exige rigor absoluto en el método científico, demostración formal y análisis de error."
        elif self.itinerary_id == 'ITIN_PROF':
            itin_ctx = "ENFOQUE PROFESIONAL: Prioriza la viabilidad, normativas y precisión de cálculo aplicado."

        return f"{base_role}\n{itin_ctx}\nESTRUCTURA: Usa subdivisiones SD_THEO y SD_CALC. Evalúa con PRM-STRIKE, RPP-TRAZA y ILC-CONTEXT."

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
            f"1. Si es SD_THEO, usa PRM-STRIKE (opción múltiple).\n"
            f"2. Si es SD_CALC, usa RPP-TRAZA (cálculo procedimental con W-TECH-CALC) o ILC-CONTEXT.\n"
            f"3. Salida estrictamente JSON (Array 'items')."
        )

    def get_output_schema(self):
        """
        Atomic JSON Schema for ARCH_SCI.
        """
        return {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "block_type": {"type": "string", "enum": ["PRM-STRIKE", "RPP-TRAZA", "ILC-CONTEXT"]},
                            "widget_id": {"type": "string", "enum":["W-OBJ-STRIKE", "W-TECH-CALC"]},
                            "content": {
                                "type": "object",
                                "properties": {
                                    "stem": {"type": "string"},
                                    "options": {"type": "array", "items": {"type": "string"}},
                                    "media_assets": {"type": "array", "items": {"type": "string"}}
                                },
                                "required": ["stem"]
                            },
                            "grading_logic": {
                                "type": "object",
                                "properties": {
                                    "correct_answer": {"type": "string"},
                                    "evaluation_criteria": {"type": "array", "items": {"type": "string"}}
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
