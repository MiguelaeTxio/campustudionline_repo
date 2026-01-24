# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/core/services/assessment_strategies/humanities_strategy.py
def generate_humanities_prompt(content_text: str, subject_name: str, subject_type: str = "HUMANITIES_GENERIC") -> str:
    """ESTRATEGIA HUMANIDADES: Comentario y Ensayo (UGR)."""
    return f"""Actúa como Catedrático de la UGR. Examen para '{subject_name}'.
FUENTE: {content_text[:50000]}
Estructura: 1. Conceptos (Test), 2. Comentario (Abierta), 3. Ensayo (Desarrollo).
Responde en JSON estricto."""

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    """Fase A: Humanidades y Artes (Esqueleto UGR)"""
    return {
        'skeleton': [
            {'label': 'Terminología y Conceptos', 'type': 'multiple_choice', 'widget': 'RADIO_SELECT'},
            {'label': 'Terminología y Conceptos', 'type': 'multiple_choice', 'widget': 'RADIO_SELECT'},
            {'label': 'Comentario de Fuente', 'type': 'open_ended', 'widget': 'TEXT_AREA'},
            {'label': 'Ensayo Dialéctico', 'type': 'open_ended', 'widget': 'TEXT_AREA'}
        ],
        'source_for_exam': content_text, 'metadata': {}
    }