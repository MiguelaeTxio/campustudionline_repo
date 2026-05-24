# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/factory.py
"""
Factory for instantiating the appropriate exam strategy based on the archetype.
Routes each of the 6 certified archetypes to its dedicated strategy implementation.
Complies with V06DOC_ARCHETYPES, V06DOC_STRUCTURE (v5.9 — 2026-05-16).
---
Factoría para instanciar la estrategia de examen adecuada según el arquetipo.
Enruta cada uno de los 6 arquetipos certificados a su implementación de estrategia dedicada.
Cumple con V06DOC_ARCHETYPES, V06DOC_STRUCTURE (v5.9 — 2026-05-16).
"""
from .strategies.languages   import LanguagesStrategy
from .strategies.health      import HealthStrategy
from .strategies.tech        import TechnicalStrategy
from .strategies.social      import SocialStrategy
from .strategies.humanities  import HumanitiesStrategy
from .strategies.science     import ScienceStrategy
from .logic                  import AcademicDeductor


class ExamFactory:
    """
    Static factory that maps archetype IDs to their strategy implementations.
    All 6 certified archetypes are mapped explicitly.
    Unknown archetypes fall back to SocialStrategy (most generic casuistic model).
    ---
    Factoría estática que mapea IDs de arquetipo a sus implementaciones de estrategia.
    Los 6 arquetipos certificados están mapeados explícitamente.
    Los arquetipos desconocidos recurren a SocialStrategy (modelo casuístico más genérico).
    Ref: V06DOC_ARCHETYPES (Sección 1 — Árbol de Arquetipos v5.9).
    """

    # Archetype ID constants — mirror Exam.Archetype TextChoices
    # Constantes de ID de arquetipo — espejo de Exam.Archetype TextChoices
    ARCH_LANG   = 'ARCH_LANG'
    ARCH_HEALTH = 'ARCH_HEALTH'
    ARCH_TECH   = 'ARCH_TECH'
    ARCH_SOC    = 'ARCH_SOC'
    ARCH_HUM    = 'ARCH_HUM'
    ARCH_SCI    = 'ARCH_SCI'

    # Explicit mapping — all 6 archetypes / Mapeo explícito — los 6 arquetipos
    _STRATEGY_MAP = {
        ARCH_LANG:   LanguagesStrategy,
        ARCH_HEALTH: HealthStrategy,
        ARCH_TECH:   TechnicalStrategy,
        ARCH_SOC:    SocialStrategy,
        ARCH_HUM:    HumanitiesStrategy,
        ARCH_SCI:    ScienceStrategy,
    }

    @staticmethod
    def get_strategy_for_subject(subject, context_title=None, **kwargs):
        """
        High-level entry point: deduces academic metadata from a Subject instance
        using the hybrid classification protocol, then instantiates the strategy.
        Used when no pre-classified metadata is available (e.g. direct subject access).
        ---
        Punto de entrada de alto nivel: deduce los metadatos académicos desde una instancia Subject
        usando el protocolo de clasificación híbrido y luego instancia la estrategia.
        Usado cuando no hay metadatos pre-clasificados disponibles.
        Ref: V06DOC_LOGIC_MAPPING V1.3 (Protocolo Híbrido IA + Python).
        """
        metadata = AcademicDeductor.get_context_metadata(
            subject,
            context_title=context_title
        )

        return ExamFactory.get_strategy(
            archetype_id         = metadata['archetype_id'],
            sub_archetype_id     = metadata['sub_archetype_id'],
            pedagogical_level    = metadata['pedagogical_level'],
            itinerary_id         = metadata['itinerary_id'],
            target_language_code = metadata.get('target_language_code', 'es'),
            localized_sections   = metadata.get('localized_sections', {}),
            **kwargs
        )

    @staticmethod
    def get_strategy(
        archetype_id,
        sub_archetype_id  = 'DEFAULT',
        pedagogical_level = 'LVL_B',
        itinerary_id      = 'ITIN_MIN',
        **kwargs
    ):
        """
        Core factory method: returns a fully configured strategy instance
        based on the archetype_id. All keyword arguments are passed through
        to the strategy constructor (target_language_code, localized_sections, etc.).
        Unknown archetypes log a warning and fall back to SocialStrategy.
        ---
        Método de factoría principal: devuelve una instancia de estrategia completamente
        configurada basada en el archetype_id. Todos los kwargs se pasan al constructor
        de la estrategia (target_language_code, localized_sections, etc.).
        Los arquetipos desconocidos registran un aviso y recurren a SocialStrategy.
        Ref: V06DOC_ARCHETYPES (Sección 1).
        """
        import logging
        logger = logging.getLogger(__name__)

        strategy_class = ExamFactory._STRATEGY_MAP.get(archetype_id)

        if strategy_class is None:
            logger.warning(
                f"ExamFactory: arquetipo desconocido '{archetype_id}'. "
                f"Fallback a SocialStrategy."
            )
            strategy_class = SocialStrategy

        return strategy_class(
            sub_archetype_id  = sub_archetype_id,
            pedagogical_level = pedagogical_level,
            itinerary_id      = itinerary_id,
            **kwargs
        )
