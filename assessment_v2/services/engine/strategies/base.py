# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/base.py
from abc import ABC, abstractmethod

class BaseAssessmentStrategy(ABC):
    def __init__(self, **kwargs):
        self.pedagogical_level = kwargs.get('pedagogical_level', 'LVL_B')

    @abstractmethod
    def generate_structure(self):
        pass

    @abstractmethod
    def get_system_prompt(self):
        pass
