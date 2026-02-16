# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/languages.py
from .base import BaseExamStrategy
from decimal import Decimal
import json

class LanguagesStrategy(BaseExamStrategy):
    """
    Exam strategy for languages based on international standards.
    Implements UGR-standard penalty formulas and high-fidelity AI prompts.
    
    ---
    
    Estrategia de examen para idiomas basada en estándares internacionales.
    Implementa fórmulas de penalización estándar UGR y prompts de IA de alta fidelidad.
    """

    def grade_item(self, item, student_input):
        """
        Implements objective grading (UGR formula) and prepares production items.
        ---
        Implementa calificación objetiva (fórmula UGR) y prepara ítems de producción.
        """
        logic = item.grading_logic
        block_type = item.block_type
        
        # 1. Bloques Objetivos: PRM-STRIKE, CLO-MULTI (Fórmula UGR: A - E/(N-1))
        if block_type in ['PRM-STRIKE', 'CLO-MULTI']:
            correct_answer = logic.get('correct_answer')
            penalty = Decimal(str(logic.get('penalty_factor', 0.33)))
            if student_input == correct_answer:
                return Decimal('1.0'), {"status": "CORRECT", "detail": "Match found."}
            elif student_input:
                return -penalty, {"status": "INCORRECT", "penalty_applied": float(penalty)}
            return Decimal('0.0'), {"status": "UNANSWERED"}

        # 2. Bloques de Producción: DRA-HOLO (Rúbrica Holística V06DOC_BLOCKS)
        if block_type == 'DRA-HOLO':
            return Decimal('0.0'), {
                "status": "REQUIRES_UNIVERSIA_GRADING",
                "engine": "DRA-HOLO_V1",
                "rubric": {
                    "rigor": "Evaluación del sesgo académico y precisión (V06DOC_LEVELS)",
                    "estructura": "Coherencia y organización del discurso",
                    "terminología": "Densidad de tecnicismos según nivel",
                    "forma": "Registro y corrección formal (Penalización hasta -2.5)"
                },
                "justification_role": "Catedrático UGR"
            }
        
        return Decimal('0.0'), {"status": "PENDING_AI_REVIEW"}

    def get_system_prompt(self):
        """
        Generates a high-fidelity system prompt based on V06DOC_LEVELS and V06DOC_METADATA.
        ---
        Genera un prompt de sistema de alta fidelidad basado en V06DOC_LEVELS y V06DOC_METADATA.
        """
        # Configuración de Rigor y Emulación (V06DOC_LEVELS)
        rigor_map = {
            'LVL_A': {'rigor': 0.8, 'density': 'Baja', 'distractors': 'Obvios', 'role': 'Tutor de Apoyo'},
            'LVL_B': {'rigor': 1.0, 'density': 'Media', 'distractors': 'Plausibles', 'role': 'Evaluador Competente'},
            'LVL_C': {'rigor': 1.6, 'density': 'Máxima', 'distractors': 'Lógica de error común', 'role': 'Catedrático Exigente'}
        }
        config = rigor_map.get(self.pedagogical_level, rigor_map['LVL_B'])
        
        return f"""
ROLE: {config['role']} especializado en Lingüística.
PEDAGOGICAL LEVEL: {self.pedagogical_level} (Rigor x{config['rigor']})
ITINERARY: {self.itinerary_id}

EMULATION PARAMETERS (V06DOC_LEVELS):
- DENSITY_INDEX: {config['density']} de tecnicismos.
- DISTRACTOR_QUALITY: {config['distractors']}.
- GRADING_BIAS: {'Constructivo' if 'MIN' in self.itinerary_id else 'Punitivo/Selectivo'}.

BLOCK MECHANICS (V06DOC_BLOCKS):
1. PRM-STRIKE: Penalty 0.33. Focus on conceptual errors.
2. CLO-OPEN/MULTI: Strict lexical validation.
3. DRA-HOLO: Grading in 4 ejes: Rigor, Estructura, Terminología, Forma.
   - FORM_PEN: Apply up to -2.5 for formal/syntax errors.

FEEDBACK TAXONOMY (V06DOC_METADATA):
All justifications must use:
- FB_CONCEPT: For base theoretical errors.
- FB_FORMAL: For register/syntax issues.
- FB_PROCEDURAL: For method/logic errors.
- FB_SAFETY: For critical security/protocol violations (if applicable).
"""


    def get_user_prompt(self, context_text, topic):
        """
        Generates the specific user instruction for Language Exams (CERTACCLES Model).
        ---
        Genera la instrucción específica de usuario para exámenes de idiomas (Modelo CERTACCLES).
        """
        return (
            f"TEMA: {topic}. "
            f"MATERIAL DE REFERENCIA: {context_text[:40000]} "
            f"INSTRUCCIÓN: Actúa como examinador oficial de idiomas de la UGR. Genera un examen "
            f"siguiendo las destrezas de Reading, Writing y Use of English basadas en el texto. "
            f"Nivel de rigor: {self.pedagogical_level}. Itinerario: {self.itinerary_id}."
        )

    def get_output_schema(self):
        """
        Defines the high-fidelity JSON structure for the Language Exam Contract.
        ---
        Define la estructura JSON de alta fidelidad para el Contrato de Examen de Idiomas.
        """
        return {
            "subdivision_sequence": [
                {
                    "subdivision_id": "SD_READ | SD_WRIT | SD_MEDI",
                    "title": "string",
                    "instructions": "string",
                    "items": [
                        {
                            "block_type": "PRM-STRIKE | CLO-OPEN | CLO-MULTI | MAT-LINK",
                            "widget_id": "W-OBJ-STRIKE | W-TXT-CLOZE | W-MIX-MATCH",
                            "content": {
                                "stem": "string",
                                "options": "list (if PRM/CLO-MULTI)",
                                "media_assets": []
                            },
                            "grading_logic": {
                                "correct_answer": "any",
                                "penalty_factor": 0.33,
                                "kill_switch": False
                            },
                            "metadata": {
                                "competency_tag": "COMP_GEN | COMP_ESP",
                                "cognitive_tag": "COG_REM | COG_UND | COG_APP"
                            }
                        }
                    ]
                }
            ]
        }

    def generate_structure(self, exam_uuid, sub_archetype_id='SUB-LIN-CERT'):
        """Creates the initial relational structure skeleton."""
        contract = self.generate_contract_skeleton(exam_uuid, 'ARCH_LANG', sub_archetype_id)
        contract["subdivision_sequence"] = [
            {"subdivision_id": "SD_READ", "title": "Reading & Use of English", "items": []},
            {"subdivision_id": "SD_LIST", "title": "Listening", "items": []},
            {"subdivision_id": "SD_WRIT", "title": "Writing", "items": []},
            {"subdivision_id": "SD_MEDI", "title": "Mediation", "items": []},
            {"subdivision_id": "SD_SPEAK", "title": "Speaking", "items": []}
        ]
        return contract
