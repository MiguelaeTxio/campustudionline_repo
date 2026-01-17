def generate_sciences_prompt(content_text: str) -> str:
    """
    ESTRATEGIA CIENCIAS: Resolución de Problemas.
    """
    return f"""
Actúa como Catedrático de Ingeniería/Matemáticas.
TEMARIO:
{content_text[:40000]}

Genera un EXAMEN FINAL DE PROBLEMAS (4 Problemas).
Usa LaTeX para fórmulas.

ESTRUCTURA:
1. Problema de Cálculo/Base.
2. Problema de Aplicación Práctica.
3. Problema Complejo.
4. Problema de Integración.

FORMATO JSON:
{{
  "questions": [
    {{
      "question_text": "Enunciado...",
      "question_type": "open_ended",
      "model_answer": "Solución paso a paso..."
    }}
  ]
}}
"""
