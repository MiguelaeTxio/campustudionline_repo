# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/core/services/assessment_strategies/factory.py
from core.services.assessment_strategies import (
    sciences_strategy, 
    humanities_strategy, 
    health_strategy, 
    languages_strategy, 
    legal_strategy
)

class AssessmentStrategyFactory:
    """
    [PATRÓN FACTORY] Despachador centralizado de estrategias de evaluación.
    Elimina la lógica condicional dispersa en el orquestador.
    """
    
    _STRATEGY_MAP = {
        "LOGIC_AND_TECH": sciences_strategy,
        "CEFR_LANGUAGES": languages_strategy,
        "SOCIO_LEGAL": legal_strategy,
        "HEALTH_SCIENCES": health_strategy,
        "HUMANITIES_ARTS": humanities_strategy
    }

    @classmethod
    def get_strategy(cls, archetype: str):
        """
        Devuelve el módulo de estrategia correspondiente al arquetipo.
        Por defecto devuelve humanities_strategy si no hay coincidencia.
        """
        return cls._STRATEGY_MAP.get(archetype, humanities_strategy)
