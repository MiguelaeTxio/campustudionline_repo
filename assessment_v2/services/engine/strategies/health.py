# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/health.py
from .base import BaseExamStrategy
from decimal import Decimal
import json

class HealthStrategy(BaseExamStrategy):
    """
    Exam strategy for Health Sciences (ARCH_HEALTH).
    Fully compliant with ECOE model and V06DOC_SUBARCHETYPES.
    
    COVERS:
    - 5 Sub-archetypes (MED, CUID, BIO, PSY, VET).
    - Blocks: CDS-KILL (Fatal), PRM-STRIKE, ILC-CONTEXT.
    - Itineraries: ROT (Rotatorio - Strict Safety), MAI, MIN.
    - Widgets: W-PROC-ACTION, W-CLIN-SCAN, W-OBJ-STRIKE.
    """

    def grade_item(self, item, student_input):
        """
        Grades health items following V06DOC_BLOCKS.
        Prioritizes patient safety (KILL_SWITCH).
        """
        logic = item.grading_logic
        block_type = item.block_type
        
        # --- MOTOR 1: CDS-KILL (Checklist Dicotómico de Seguridad) ---
        # Ref: V06DOC_BLOCKS Section 2
        if block_type == 'CDS-KILL':
            # Expected input: bool or {"checked": bool}
            is_performed = student_input is True or (isinstance(student_input, dict) and student_input.get('checked'))
            correct_state = logic.get('correct_answer', True)

            if is_performed == correct_state:
                return Decimal('1.0'), {"status": "CORRECT", "safety": "SECURE"}
            else:
                # If the step is critical (KILL_SWITCH), score is 0 for the whole section
                if logic.get('kill_switch', False) or self.itinerary_id == 'ITIN_ROT':
                    return Decimal('0.0'), {
                        "status": "FATAL_ERROR", 
                        "kill_switch_activated": True,
                        "feedback_category": "FB_SAFETY",
                        "justification": "Violación de protocolo crítico de seguridad. El paciente está en riesgo."
                    }
                return Decimal('0.0'), {"status": "INCORRECT", "feedback_category": "FB_PROCEDURAL"}

        # --- MOTOR 2: PRM-STRIKE (Diagnóstico Diferencial) ---
        # Ref: V06DOC_BLOCKS Section 1
        elif block_type == 'PRM-STRIKE':
            correct_answer = logic.get('correct_answer')
            if str(student_input).strip() == str(correct_answer).strip():
                return Decimal('1.0'), {"status": "CORRECT"}
            elif not student_input:
                return Decimal('0.0'), {"status": "OMITTED"}
            else:
                # Higher penalty in Health (especially in ROT)
                num_options = len(item.content.get('options', []))
                penalty_base = Decimal('1.0') / Decimal(str(max(1, num_options - 1))) if num_options > 1 else Decimal('0.5')
                
                # Double penalty for wrong diagnosis in Rotatorio
                if self.itinerary_id == 'ITIN_ROT':
                    penalty_base = penalty_base * Decimal('1.5')
                
                return -penalty_base, {"status": "INCORRECT", "penalty": float(penalty_base)}

        # --- MOTOR 3: ILC-CONTEXT (Interpretación de Pruebas/Contexto) ---
        # Ref: V06DOC_BLOCKS Section 2
        elif block_type == 'ILC-CONTEXT':
            # Requires semantic comparison of diagnostic inference
            # For now, we use keyword matching + pending AI refinement
            keywords = logic.get('keywords', [])
            student_text = str(student_input).lower()
            hits = sum(1 for kw in keywords if kw.lower() in student_text)
            
            if not keywords: return Decimal('1.0'), {"status": "MANUAL_REVIEW"}
            
            score = Decimal(str(hits / len(keywords)))
            return score, {"status": "GRADED", "hits": hits}

        return Decimal('0.0'), {"status": "PENDING"}

    def get_section_plan(self):
        """
        Returns the mandatory section list for the orchestrator (SKELETON-FIRST).
        Ref: V06DOC_ARCHETYPES.
        """
        return [
            {
                "subdivision_id": "SD_FACT",
                "title": "Estación 1: Anamnesis y Hechos",
                "instructions": "Recopila los datos clínicos relevantes y antecedentes del paciente.",
                "time_limit": 300
            },
            {
                "subdivision_id": "SD_PROC",
                "title": "Estación 2: Procedimiento Clínico",
                "instructions": "Ejecuta la técnica o exploración requerida. Atención a la seguridad.",
                "time_limit": 600
            },
            {
                "subdivision_id": "SD_ETHI",
                "title": "Estación 3: Juicio Ético y Seguridad",
                "instructions": "Valora las implicaciones deontológicas y riesgos del caso.",
                "time_limit": 300
            }
        ]

    def get_system_prompt(self):
        """
        Generates clinical role based on Sub-Archetype (V06DOC_SUBARCHETYPES).
        """
        roles = {
            'SUB-SAN-MED': "Rol: Facultativo Especialista (UGR). Foco: Diagnóstico Diferencial, Fisiopatología.",
            'SUB-SAN-CUID': "Rol: Enfermero/a Clínico (NANDA). Foco: Planes de cuidados, Seguridad, Técnica.",
            'SUB-SAN-BIO': "Rol: Especialista en Laboratorio/Bioquímica. Foco: Farmacología, Analítica, Método.",
            'SUB-SAN-PSY': "Rol: Psicólogo/a Clínico (DSM-5). Foco: Evaluación conductual, Psicometría.",
            'SUB-SAN-VET': "Rol: Cirujano Veterinario. Foco: Patología comparada, Zoonosis, Clínica animal."
        }
        base_role = roles.get(self.sub_archetype_id, "Rol: Evaluador Clínico ECOE.")

        itin_ctx = ""
        if self.itinerary_id == 'ITIN_ROT':
            itin_ctx = "CONTEXTO ROTATORIO: Tolerancia CERO a errores de seguridad. Activa KILL_SWITCH en pasos críticos."

        return f"{base_role}\n{itin_ctx}\nUsa bloques CDS-KILL para protocolos obligatorios y ILC-CONTEXT para interpretación de pruebas (Analíticas/Rayos X)."

    def get_user_prompt(self, context_text, topic, subdivision_id, generated_item_titles=None):
        """
        Atomic generation prompt for a specific subdivision (V06DOC_TEMPLATES).
        """
        memory = f"\nÍtems ya generados: {', '.join(generated_item_titles)}" if generated_item_titles else ""
        return (
            f"GENERA 3 ÍTEMS para la sección: {subdivision_id}.\n"
            f"TEMA: {topic}. {memory}\n"
            f"REF: {context_text[:50000]}\n"
            f"CONFIG: Arquetipo={self.sub_archetype_id}, Itinerario={self.itinerary_id}, Nivel={self.pedagogical_level}.\n"
            f"REQUISITOS:\n"
            f"1. Si es SD_PROC, incluye al menos un bloque CDS-KILL con kill_switch: True para un paso vital.\n"
            f"2. Usa W-CLIN-SCAN para ítems que requieran interpretación de imágenes (Rayo X, ECG).\n"
            f"3. Salida estrictamente JSON (Array 'items')."
        )

    def get_output_schema(self):
        """
        Atomic JSON Schema for ARCH_HEALTH.
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
                            "block_type": {"type": "string", "enum": ["CDS-KILL", "PRM-STRIKE", "ILC-CONTEXT"]},
                            "widget_id": {"type": "string", "enum": ["W-PROC-ACTION", "W-OBJ-STRIKE", "W-CLIN-SCAN"]},
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
                                    "correct_answer": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "boolean"}
                                        ]
                                    },
                                    "kill_switch": {"type": "boolean"},
                                    "penalty_factor": {"type": "number"},
                                    "keywords": {"type": "array", "items": {"type": "string"}}
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
