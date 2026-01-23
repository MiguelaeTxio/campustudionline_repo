# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/core/services/assessment_strategies/health_strategy.py
def generate_health_prompt(content_text: str, subject_name: str = "Ciencias de la Salud") -> str:
    """ESTRATEGIA SALUD: Modelo UGR (ECOE)."""
    return f"""Actúa como Profesor de Salud UGR. Examen para '{subject_name}'.
FUENTE: {content_text[:50000]}
Responde en JSON estricto."""

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    """Fase A: Salud (Esqueleto UGR ECOE)"""
    return {
        'skeleton': [
            {'label': 'Protocolos Técnicos', 'type': 'multiple_choice', 'widget': 'RADIO_SELECT'},
            {'label': 'Protocolos Técnicos', 'type': 'multiple_choice', 'widget': 'RADIO_SELECT'},
            {'label': 'Juicio Diagnóstico', 'type': 'open_ended', 'widget': 'TEXT_AREA'},
            {'label': 'Plan Actuación ECOE', 'type': 'open_ended', 'widget': 'FILE_UPLOAD'}
        ],
        'source_for_exam': content_text, 'metadata': {}
    }
