# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/base.py
from abc import ABC, abstractmethod
from decimal import Decimal
from assessment_v2.services.tracking import TrackingService

class BaseExamStrategy(ABC):
    """
    Abstract base class defining the common contract for all exam strategies.
    Ensures all archetypes comply with the platform's UGR-inspired quality standards.
    V06DOC_STRUCTURE: Mandatory sub_archetype_id and Tracking integration.
    
    ---
    
    Clase abstracta base que define el contrato común para todas las estrategias de examen.
    Garantiza que todos los arquetipos cumplan con los estándares de calidad de la plataforma.
    V06DOC_STRUCTURE: sub_archetype_id obligatorio e integración de Tracking.
    """

    def __init__(self, sub_archetype_id, pedagogical_level='LVL_B', itinerary_id='ITIN_MIN', **kwargs):
        """
        Initializes the strategy with academic context and pre-calculates rigor.
        ---
        Inicializa la estrategia con el contexto académico y pre-calcula el rigor.
        """
        self.sub_archetype_id = sub_archetype_id
        self.pedagogical_level = pedagogical_level
        self.itinerary_id = itinerary_id
        self.config = kwargs
        
        # Pre-calculation of Rigor Parameters / Pre-cálculo de Parámetros de Rigor
        self.rigor_params = self._get_grading_params()

    @abstractmethod
    def get_system_prompt(self):
        """
        Returns the specific system prompt for the academic archetype.
        ---
        Devuelve el prompt de sistema específico para el arquetipo académico.
        """
        pass

    @abstractmethod
    def get_user_prompt(self, context_text, topic):
        """
        Generates the user prompt injecting the study material context.
        ---
        Genera el prompt de usuario inyectando el contexto del material de estudio.
        """
        pass

    @abstractmethod
    def get_output_schema(self):
        """
        Defines the expected JSON schema for the AI model response.
        ---
        Define el esquema JSON esperado para la respuesta del modelo de IA.
        """
        pass
    
    @abstractmethod
    def grade_item(self, item, student_input):
        """
        Grades an individual item returning (points, feedback_dict).
        Must be implemented by each archetype according to V06DOC_BLOCKS.
        ---
        Califica un ítem individual devolviendo (puntos, feedback_dict).
        Debe ser implementado por cada arquetipo según V06DOC_BLOCKS.
        """
        pass

    def apply_rigor_adjustment(self, raw_score):
        """
        Applies the Rigor Factor (0.8, 1.0, 1.6) to the raw score.
        Ref: V06DOC_LEVELS.
        ---
        Aplica el Factor de Rigor (0.8, 1.0, 1.6) a la nota bruta.
        Ref: V06DOC_LEVELS.
        """
        factor = Decimal(str(self.rigor_params.get('rigor_factor', 1.0)))
        adjusted_score = Decimal(str(raw_score)) * factor
        
        # Cap score at 1.0 (Maximum excellence) / Limitar nota a 1.0 (Máxima excelencia)
        return min(adjusted_score, Decimal('1.0'))

    def record_engine_usage(self, user, exam, model_name, input_tokens, output_tokens, op_type="EXAM_GEN"):
        """
        Wraps TrackingService to record AI consumption.
        ---
        Envuelve TrackingService para registrar el consumo de IA.
        """
        TrackingService.record_usage(
            user=user,
            exam=exam,
            model_name=model_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            operation_type=op_type
        )

    def _get_grading_params(self):
        """
        Calculates weights and thresholds based on the pedagogical intersection matrix.
        ---
        Calcula los pesos y umbrales basados en la matriz de intersección pedagógica.
        """
        # Rigor mapping according to V06DOC_LEVELS / Mapeo de rigor según V06DOC_LEVELS
        rigor_map = {'LVL_A': 0.8, 'LVL_B': 1.0, 'LVL_C': 1.6}
        rigor_factor = rigor_map.get(self.pedagogical_level, 1.0)
        
        # Penalty: Zero tolerance in LVL_C or Major itinerary (Ref: V06DOC_LEVELS)
        # Penalización: Tolerancia cero en LVL_C o itinerario Maior.
        penalty_threshold = 0.0 if (self.pedagogical_level == 'LVL_C' or self.itinerary_id == 'ITIN_MAI') else 0.5
        
        return {
            "rigor_factor": float(rigor_factor), 
            "penalty_threshold": float(penalty_threshold)
        }

    def generate_contract_skeleton(self, exam_uuid, archetype_id, sub_archetype_id):
        """
        Generates the complete JSON skeleton of the 'Exam Contract'.
        ---
        Genera el esqueleto JSON completo del 'Exam Contract'.
        """
        return {
            "exam_header": {
                "exam_id": str(exam_uuid),
                "archetype_id": archetype_id,
                "sub_archetype_id": sub_archetype_id,
                "itinerary_id": self.itinerary_id,
                "pedagogical_level": self.pedagogical_level,
                "grading_params": self.rigor_params
            },
            "subdivision_sequence": [],
            "student_submission": {},
            "grading_report": {}
        }
