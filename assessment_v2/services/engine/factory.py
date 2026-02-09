# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/factory.py
from .strategies.languages import LanguagesStrategy

class ExamFactory:
    ARCH_LANGUAGES = 'ARCH_LANGUAGES'

    @staticmethod
    def get_strategy(archetype_id, **kwargs):
        if archetype_id == ExamFactory.ARCH_LANGUAGES:
            return LanguagesStrategy(**kwargs)
        raise ValueError(f"Arquetipo {archetype_id} no implementado.")
