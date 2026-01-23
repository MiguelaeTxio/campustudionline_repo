# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/core/services/assessment_strategies/sciences_strategy.py
def generate_sciences_prompt(content_text: str, subject_name: str = "Asignatura Técnica") -> str:
    """ESTRATEGIA CIENCIAS (LOGIC_AND_TECH): Emulación UGR."""
    return f"""Actúa como Profesor de la UGR. Examen para '{subject_name}'.
FUENTE: {content_text[:45000]}
REGLA: Usa LaTeX obligatorio. Responde en JSON estricto."""

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    """Fase A: Ciencias (Esqueleto UGR)"""
    return {
        'skeleton': [{'label': 'Cálculo y Resolución', 'type': 'open_ended', 'widget': 'MATH_INPUT'}] * 4,
        'source_for_exam': content_text, 'metadata': {}
    }
