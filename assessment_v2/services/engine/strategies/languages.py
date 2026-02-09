# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/languages.py
from .base import BaseAssessmentStrategy

class LanguagesStrategy(BaseAssessmentStrategy):
    def generate_structure(self):
        return {
            "subdivision_sequence": [
                {"subdivision_id": "SD_READ", "title": "Reading", "time_limit": 1200, "items": []},
                {"subdivision_id": "SD_LIST", "title": "Listening", "time_limit": 900, "items": []},
                {"subdivision_id": "SD_WRIT", "title": "Writing", "time_limit": 1800, "items": []}
            ]
        }

    def get_system_prompt(self):
        return f"Estándar: Máxima Calidad. Nivel: {self.pedagogical_level}. Generar evaluación de idiomas CertAccles."
