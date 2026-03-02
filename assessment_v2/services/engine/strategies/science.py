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
            steps = student_input.get('steps',[]) if isinstance(student_input, dict) else[]
            if not steps:
                return Decimal('0.0'), {"status": "NO_STEPS_PROVIDED"}
            # [HITO 6 FIX] Incidencia 59: Implementación de Motor RPP-TRAZA
            step_matrix = logic.get('step_matrix',[])
            if not step_matrix:
                return Decimal('1.0'), {"status": "GRADED", "detail": "Sin pasos esperados."}
            earned_score = Decimal('0.0')
            total_weight = Decimal('0.0')
            for expected_step in step_matrix:
                step_weight = Decimal(str(expected_step.get('weight', 0.1)))
                total_weight += step_weight
                student_step = next((s for s in steps if str(s.get('id')) == str(expected_step.get('id'))), None)
                if student_step and str(student_step.get('value', '')).strip() == str(expected_step.get('value', '')).strip():
                    earned_score += step_weight
            final_score = (earned_score / total_weight) if total_weight > 0 else Decimal('0.0')
            return final_score, {"status": "GRADED"}
        
        # --- MOTOR 2: PRM-STRIKE (Test Objetivo) ---
        elif block_type == 'PRM-STRIKE':
            correct = logic.get('correct_answer')
            if str(student_input).strip() == str(correct).strip():
                return Decimal('1.0'), {"status": "CORRECT"}
            # [HITO 6 FIX] Penalización dinámica según V06DOC_LEVELS
            penalty = logic.get('penalty', Decimal('-0.33'))
            return Decimal(str(penalty)), {"status": "INCORRECT", "penalty_applied": True}

        # --- MOTOR 3: ILC-CONTEXT (Interpretación de Datos) ---
        elif block_type == 'ILC-CONTEXT':
            return Decimal('0.0'), {"status": "PENDING_AI_RUBRIC", "detail": "Evaluación cualitativa de interpretación de datos/gráficos."}

        return Decimal('0.0'), {"status": "PENDING_MANUAL_REVIEW"}

    def get_exam_skeleton(self):
        """
        Returns the structural skeleton for the 6 Science models.
        Ref: V06DOC_SUBARCHETYPES V5.0.
        Refactor: DRY & Prompt Binding implemented. (Replaces legacy get_section_plan)
        """
        sid = self.sub_archetype_id
        skeleton = []

        # 1. INSTRUCCIONES BASE (DRY)
        I_THEORY = "Genera una pregunta teórica de opción múltiple (4 opciones) sobre fundamentos."
        I_CALC = "Genera un problema de cálculo procedimental paso a paso. OBLIGATORIO: Define `step_matrix`."
        I_DATA = "Genera un ejercicio de interpretación de datos, gráficas o tablas experimentales."

        # 2. OVERRIDES ESPECÍFICOS
        if sid == "SUB-SCI-BIO":
            I_THEORY = "Genera una pregunta sobre taxonomía, genética, biología celular o ecología."
        elif sid == "SUB-SCI-CHEM":
            I_CALC = "Genera un problema de estequiometría, equilibrio químico o síntesis orgánica."
        elif sid == "SUB-SCI-PHYS":
            I_CALC = "Genera un problema de mecánica, electromagnetismo o termodinámica."
        elif sid == "SUB-SCI-GEOL":
            I_DATA = "Genera un ejercicio de interpretación de cortes geológicos, mapas estratigráficos o mineralogía."
        elif sid == "SUB-SCI-DATA":
            I_CALC = "Genera un problema de probabilidad, inferencia estadística o algoritmo de ML."

        # 3. CONSTRUCCIÓN DEL ESQUELETO
        # Estructura genérica para Ciencias: Teoría (Standard) + Resolución (Split)
        
        # 1. SUB-SCI-BIO
        if sid == "SUB-SCI-BIO":
            skeleton = [
                {"subdivision_id": "SD_THEO", "title": "Fundamentos Biológicos", "instructions": "Responda a las cuestiones teóricas.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": I_THEORY}]},
                {"subdivision_id": "SD_CALC", "title": "Genética y Evolución", "instructions": "Resuelva los problemas de herencia o población.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "RPP-TRAZA", "widget_id": "W-TECH-CALC", "task_instruction": "Resuelve un problema de genética mendeliana o poblacional."}]}
            ]
        # 2. SUB-SCI-CHEM
        elif sid == "SUB-SCI-CHEM":
            skeleton = [
                {"subdivision_id": "SD_THEO", "title": "Química Fundamental", "instructions": "Justifique las propiedades periódicas o enlace.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": I_THEORY}]},
                {"subdivision_id": "SD_CALC", "title": "Reactividad y Cálculo", "instructions": "Ajuste la reacción y calcule rendimientos.", "layout_mode": "STANDARD", "items": [{"block_type": "RPP-TRAZA", "widget_id": "W-TECH-CALC", "task_instruction": I_CALC}]}
            ]
        # 3. SUB-SCI-PHYS
        elif sid == "SUB-SCI-PHYS":
            skeleton = [
                {"subdivision_id": "SD_THEO", "title": "Principios Físicos", "instructions": "Aplique las leyes de conservación.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": I_THEORY}]},
                {"subdivision_id": "SD_CALC", "title": "Resolución de Problemas", "instructions": "Desarrolle la solución analítica.", "layout_mode": "STANDARD", "items": [{"block_type": "RPP-TRAZA", "widget_id": "W-TECH-CALC", "task_instruction": I_CALC}]}
            ]
        # 4. SUB-SCI-GEOL
        elif sid == "SUB-SCI-GEOL":
            skeleton = [
                {"subdivision_id": "SD_THEO", "title": "Procesos Geológicos", "instructions": "Identifique los agentes y procesos.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": I_THEORY}]},
                {"subdivision_id": "SD_CALC", "title": "Interpretación y Cartografía", "instructions": "Analice el corte o mapa.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "ILC-CONTEXT", "widget_id": "W-CLIN-SCAN", "task_instruction": I_DATA}]}
            ]
        # 5. SUB-SCI-ENV
        elif sid == "SUB-SCI-ENV":
            skeleton = [
                {"subdivision_id": "SD_THEO", "title": "Sistemas Ambientales", "instructions": "Evalúe el impacto o ciclo.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": I_THEORY}]},
                {"subdivision_id": "SD_CALC", "title": "Gestión y Análisis", "instructions": "Interprete los datos de contaminación o recursos.", "layout_mode": "SPLIT_TEXT", "items": [{"block_type": "ILC-CONTEXT", "widget_id": "W-CLIN-SCAN", "task_instruction": I_DATA}]}
            ]
        # 6. SUB-SCI-DATA
        elif sid == "SUB-SCI-DATA":
            skeleton = [
                {"subdivision_id": "SD_THEO", "title": "Teoría Estadística/IA", "instructions": "Seleccione el modelo o test adecuado.", "layout_mode": "STANDARD", "items": [{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": I_THEORY}]},
                {"subdivision_id": "SD_CALC", "title": "Análisis de Datos", "instructions": "Calcule probabilidades o métricas de error.", "layout_mode": "STANDARD", "items": [{"block_type": "RPP-TRAZA", "widget_id": "W-TECH-CALC", "task_instruction": I_CALC}]}
            ]
        else:
            # Fallback
            skeleton = [
                {"subdivision_id": "SD_MODEL", "title": "Modelización", "instructions": "Plantee el modelo matemático.", "layout_mode": "STANDARD", "items":[{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Plantee el modelo que rige el fenómeno."}]},
                {"subdivision_id": "SD_CALC", "title": "Ciencia General", "instructions": "Resuelva el problema científico.", "layout_mode": "STANDARD", "items":[{"block_type": "RPP-TRAZA", "widget_id": "W-TECH-CALC", "task_instruction": I_CALC}]},
                {"subdivision_id": "SD_VERIF", "title": "Verificación", "instructions": "Compruebe la coherencia del resultado.", "layout_mode": "STANDARD", "items":[{"block_type": "PRM-STRIKE", "widget_id": "W-OBJ-STRIKE", "task_instruction": "Verifique el resultado obtenido."}]}
            ]

        return skeleton

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
