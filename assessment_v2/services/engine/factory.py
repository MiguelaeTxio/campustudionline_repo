# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/factory.py
from .strategies.languages import LanguagesStrategy
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
    def get_strategy_for_subject(subject, **kwargs):
        """
        Main entry point: Deduces metadata from Subject and returns the strategy.
        Punto de entrada: Deduce metadatos del sujeto y retorna la estrategia configurada.
        """
        metadata = AcademicDeductor.get_context_metadata(subject)
        
        return ExamFactory.get_strategy(
            archetype_id=metadata['archetype_id'],
            pedagogical_level=metadata['pedagogical_level'],
            itinerary_id=metadata['itinerary_id'],
            **kwargs
        )

    @staticmethod
    def get_strategy(archetype_id, pedagogical_level='LVL_B', itinerary_id='ITIN_MIN', **kwargs):
        """
        Returns a configured instance of the corresponding strategy.
        """
        strategy_kwargs = {
            'pedagogical_level': pedagogical_level,
            'itinerary_id': itinerary_id,
            **kwargs
        }

        # Currently, all archetypes route to LanguagesStrategy for initial V2 testing,
        # but configured with their specific pedagogical levels and itineraries.
        if archetype_id == ExamFactory.ARCH_LANG:
            return LanguagesStrategy(**strategy_kwargs)
        
        # Fallback for archetypes in development (Milestone 6)
        return LanguagesStrategy(**strategy_kwargs)
