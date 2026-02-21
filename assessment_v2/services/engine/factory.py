# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/factory.py
from .strategies.languages import LanguagesStrategy
from .strategies.health import HealthStrategy
from .strategies.tech import TechnicalStrategy
from .strategies.social import SocialStrategy
from .strategies.humanities import HumanitiesStrategy
from .logic import AcademicDeductor

class ExamFactory:
    """
    Factory to instantiate the appropriate exam strategy based on the archetype.
    Factoría para instanciar la estrategia de examen adecuada según el arquetipo deducido.
    """
    ARCH_LANG = 'ARCH_LANG'
    ARCH_HEALTH = 'ARCH_HEALTH'
    ARCH_TECH = 'ARCH_TECH'
    ARCH_SOC = 'ARCH_SOC'
    ARCH_HUM = 'ARCH_HUM'

    @staticmethod
    def get_strategy_for_subject(subject, context_title=None, **kwargs):
        """
        Main entry point: Deduces metadata from Subject and returns the strategy.
        Punto de entrada: Deduce metadatos del sujeto y retorna la estrategia configurada.
        """
        # The Deductor extracts the full constellation: Archetype, Sub-archetype, Level, and Itinerary.
        # El Deductor extrae la constelación completa: Arquetipo, Sub-arquetipo, Nivel e Itinerario.
        metadata = AcademicDeductor.get_context_metadata(subject, context_title=context_title)
        
        return ExamFactory.get_strategy(
            archetype_id=metadata['archetype_id'],
            sub_archetype_id=metadata['sub_archetype_id'], # Inyección de Identidad / Identity Injection
            pedagogical_level=metadata['pedagogical_level'],
            itinerary_id=metadata['itinerary_id'],
            target_language_code=metadata.get('target_language_code', 'en'),
            localized_sections=metadata.get('localized_sections', {}),
            **kwargs
        )

    @staticmethod
    def get_strategy(archetype_id, sub_archetype_id='DEFAULT', pedagogical_level='LVL_B', itinerary_id='ITIN_MIN', **kwargs):
        """
        Returns a configured instance of the corresponding strategy.
        ---
        Devuelve una instancia configurada de la estrategia correspondiente.
        """
        strategy_kwargs = {
            'sub_archetype_id': sub_archetype_id, # Requirement for BaseExamStrategy / Requisito para BaseExamStrategy
            'pedagogical_level': pedagogical_level,
            'itinerary_id': itinerary_id,
            **kwargs
        }

        # Mapping for Milestone 6: All archetypes now route to their specific implementation.
        # Mapeo para el Hito 6: Todos los arquetipos ahora se dirigen a su implementación específica.
        mapping = {
            ExamFactory.ARCH_LANG: LanguagesStrategy,
            ExamFactory.ARCH_HEALTH: HealthStrategy,
            ExamFactory.ARCH_TECH: TechnicalStrategy,
            ExamFactory.ARCH_SOC: SocialStrategy,
            ExamFactory.ARCH_HUM: HumanitiesStrategy,
        }

        strategy_class = mapping.get(archetype_id, LanguagesStrategy)
        return strategy_class(**strategy_kwargs)
