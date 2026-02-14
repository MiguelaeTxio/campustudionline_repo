# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/base.py
from abc import ABC, abstractmethod

class BaseExamStrategy(ABC):
    """
    Clase abstracta que define el contrato común para todas las estrategias de examen.
    Garantiza que todos los arquetipos cumplan con el estándar UGR-LEVEL (V06DOC_TEMPLATES).
    """

    def __init__(self, pedagogical_level='LVL_B', itinerary_id='ITIN_GEN', **kwargs):
        self.pedagogical_level = pedagogical_level
        self.itinerary_id = itinerary_id
        self.config = kwargs

    @abstractmethod
    def get_system_prompt(self):
        """Devuelve el prompt de sistema específico para el arquetipo académico."""
        pass

    @abstractmethod
    def get_user_prompt(self, context_text, topic):
        """Genera el prompt de usuario inyectando el contexto del material de estudio."""
        pass

    @abstractmethod
    def get_output_schema(self):
        """Define el esquema JSON esperado para la respuesta del modelo de IA."""
        pass

    def get_common_metadata(self):
        """Genera los parámetros pedagógicos y de rigor del examen."""
        return {
            "pedagogical_level": self.pedagogical_level,
            "itinerary_id": self.itinerary_id,
            "grading_params": self._get_grading_params()
        }

    def _get_grading_params(self):
        """
        Calcula los pesos y umbrales de corrección basados en la matriz 
        de intersección pedagógica (V06DOC_LEVELS).
        """
        if self.pedagogical_level == 'LVL_C':
            return {"rigor_factor": 1.6, "penalty_threshold": 0.0}
        
        if self.itinerary_id == 'ITIN_MAI':
            return {"rigor_factor": 1.3, "penalty_threshold": 0.3}
            
        return {"rigor_factor": 1.0, "penalty_threshold": 0.5}

    def generate_structure(self, exam_uuid, archetype_id, sub_archetype_id):
        """
        Genera el esqueleto JSON completo del 'Exam Contract' (V06DOC_TEMPLATES).
        Recibe los identificadores de instancia para completar la cabecera.
        """
        return {
            "exam_header": {
                "exam_id": str(exam_uuid),
                "archetype_id": archetype_id,
                "sub_archetype_id": sub_archetype_id,
                "itinerary_id": self.itinerary_id,
                "pedagogical_level": self.pedagogical_level,
                "grading_params": self._get_grading_params()
            },
            "subdivision_sequence": [
                {
                    "subdivision_id": "SD_PLACEHOLDER",
                    "title": "Sección de Evaluación",
                    "instructions": "Instrucciones de la fase...",
                    "time_limit": 0,
                    "items": []
                }
            ],
            "student_submission": {},
            "grading_report": {}
        }
