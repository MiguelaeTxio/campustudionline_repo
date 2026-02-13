from django.utils.translation import gettext_lazy as _
from .base import BaseAssessmentStrategy
import json

class LanguagesStrategy(BaseAssessmentStrategy):
    def generate_structure(self):
        """
        Define el esqueleto COMPLETO para Lenguas (CertAccles/MCER).
        Utiliza los nuevos bloques documentados en V06DOC_BLOCKS (V1.1).
        """
        return {
            "subdivision_sequence": [
                {
                    "subdivision_id": "SD_READ",
                    "title": "Comprensión Lectora (Reading & Use of English)",
                    "instructions": "Lea los textos y complete los ejercicios de gramática y vocabulario.",
                    "time_limit": 3600,
                    "items": [] 
                    # IA TARGET: 
                    # 1. MAT-LINK (Matching Headings)
                    # 2. PRM-STRIKE (Multiple Choice Reading)
                    # 3. CLO-MULTI (Multiple Choice Cloze)
                },
                {
                    "subdivision_id": "SD_LIST",
                    "title": "Comprensión Auditiva (Listening)",
                    "instructions": "Escuche los audios y responda.",
                    "time_limit": 2400,
                    "items": []
                    # IA TARGET:
                    # 1. MAT-LINK (Matching Speakers)
                    # 2. PRM-STRIKE (Interview/Conversation)
                },
                {
                    "subdivision_id": "SD_WRIT",
                    "title": "Expresión Escrita (Writing)",
                    "instructions": "Redacte los textos solicitados.",
                    "time_limit": 3600,
                    "items": []
                    # IA TARGET:
                    # 1. DRA-HOLO (Short Essay / Email)
                    # 2. DRA-HOLO (Report / Article)
                },
                {
                    "subdivision_id": "SD_MEDI",
                    "title": "Mediación Lingüística",
                    "instructions": "Transfiera la información al idioma destino o registro adecuado.",
                    "time_limit": 1800,
                    "items": []
                    # IA TARGET:
                    # 1. BMT-SHIFT (Text Mediation)
                },
                {
                    "subdivision_id": "SD_SPEAK",
                    "title": "Expresión Oral (Speaking)",
                    "instructions": "Interactúe con el examinador (UniversIA).",
                    "time_limit": 900,
                    "items": []
                    # IA TARGET:
                    # 1. INTERACTION (Prompt for W-COMM-DIALOG)
                }
            ]
        }

    def get_system_prompt(self):
        """
        Prompt de Sistema conforme a V06DOC_TEMPLATES y V06DOC_METADATA.
        Instruye el uso de los widgets W-TXT-CLOZE, W-MIX-MATCH, etc.
        """
        return f"""
ROLE: Eres 'UniversIA', arquitecto pedagógico de certificación de idiomas (MCER).
OBJECTIVE: Generar examen completo (5 destrezas) nivel {self.pedagogical_level}.
OUTPUT FORMAT: JSON estricto rellenando la estructura base.

MANDATORY JSON SCHEMA FOR ITEMS (V06DOC_TEMPLATES):
{{
  "block_type": "PRM-STRIKE | CLO-MULTI | CLO-OPEN | MAT-LINK | DRA-HOLO | BMT-SHIFT",
  "widget_id": "W-OBJ-STRIKE | W-TXT-CLOZE | W-MIX-MATCH | W-HUM-TEXT | W-COMM-DIALOG",
  "content": {{
    "stem": "Enunciado...",
    "media_assets": ["url_audio_placeholder"], 
    "text_body": "Texto con huecos {{1}} para Cloze...",
    "options": [ ... ],
    "matches": [ {{ "left": "A", "right": "1" }} ] // Para Matching
  }},
  "grading_logic": {{ ... }},
  "metadata": {{ "competency_tag": "COMP_GEN", "cognitive_tag": "COG_..." }}
}}

RULES (V06DOC_ARCHETYPES):
1. SD_READ:
   - 1x MAT-LINK (Matching Headings/Paragraphs).
   - 1x PRM-STRIKE (Reading Comprehension).
   - 1x CLO-MULTI (Use of English - Multiple Choice Cloze).
2. SD_LIST:
   - 1x MAT-LINK (Matching Speakers).
   - 1x PRM-STRIKE (Multiple Choice).
3. SD_WRIT: 2x DRA-HOLO (Essay + Report/Email).
4. SD_MEDI: 1x BMT-SHIFT (Mediación).
5. SD_SPEAK: 1x INTERACTION (Prompt para W-COMM-DIALOG).

LEVEL ADJUSTMENT ({self.pedagogical_level}):
- Ajusta vocabulario y complejidad gramatical estrictamente al nivel.
"""
