# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/tracking.py
import logging
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from assessment_v2.models.tracking import TokenUsage, CostLog

logger = logging.getLogger(__name__)

class TrackingService:
    """
    Servicio para el registro de consumo de IA y control de costes.
    Cumple con el estándar de auditoría definido en V06DOC_STRUCTURE.
    """

    @staticmethod
    def record_usage(user, exam, model_name, input_tokens, output_tokens, operation_type="EXAM_GEN"):
        """
        Registra el uso de tokens en el log diario y crea un log de coste detallado.
        """
        # Cálculo de coste estimado (Estandarizado para gemini-2.5-flash-lite)
        # Precios aproximados por millón de tokens (ajustar según realidad de la API)
        COST_PER_1K_INPUT = Decimal('0.0001') 
        COST_PER_1K_OUTPUT = Decimal('0.0004')
        
        cost_usd = (Decimal(input_tokens) / 1000 * COST_PER_1K_INPUT) + \
                   (Decimal(output_tokens) / 1000 * COST_PER_1K_OUTPUT)

        try:
            with transaction.atomic():
                # 1. Actualizar/Crear el acumulado diario del usuario
                usage, _ = TokenUsage.objects.get_or_create(
                    user=user,
                    date=timezone.now().date()
                )
                usage.input_tokens_total += input_tokens
                usage.output_tokens_total += output_tokens
                usage.estimated_cost_usd += cost_usd
                usage.save()

                # 2. Crear el log detallado vinculado al examen
                CostLog.objects.create(
                    exam=exam,
                    operation_type=operation_type,
                    model_name=model_name,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    cost_usd=cost_usd
                )
                
            logger.info(f"Usage recorded for user {user.username}: {input_tokens+output_tokens} tokens.")
        except Exception as e:
            logger.error(f"Failed to record token usage: {e}")

