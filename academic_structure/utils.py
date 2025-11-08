# /home/MiguelAeTxio/CampuStudiOnline/academic_structure/utils.py
# El namespace de la app es 'academic_structure'
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import re
import json # ADDED: Importación para normalizar JSON

def markdown_to_html_with_pygments(markdown_text):
    """
    Convierte texto Markdown a HTML, aplicando resaltado de sintaxis a los bloques de código.
    """
    code_blocks = {}

    def store_code_block(match):
        lang_match = re.search(r"```(\w+)", match.group(0))
        lang = lang_match.group(1) if lang_match else "text"
        code = match.group(0).replace(f"```{lang}", "", 1).rstrip("`").strip()

        placeholder = f"%%CODE_BLOCK_{len(code_blocks)}%%"
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter(
                style="default", full=False, noclasses=False, cssclass="codehilite"
            )
            highlighted_code = highlight(code, lexer, formatter)
            code_blocks[placeholder] = highlighted_code
        except Exception:
            # Si el lexer no se encuentra, o hay otro error, se trata como texto plano.
            highlighted_code = (
                f'<div class="codehilite"><pre><code>{code}</code></pre></div>'
            )
            code_blocks[placeholder] = highlighted_code
        return placeholder

    # Extraer y reemplazar bloques de código
    processed_text = re.sub(r"```(\w*)\n([\s\S]*?)```", store_code_block, markdown_text)

    # Convertir el resto del Markdown a HTML
    html = markdown.markdown(
        processed_text,
        extensions=[
            "fenced_code",
            "tables",
            "attr_list",
            "def_list",
            "sane_lists",
            "toc",
        ],
    )

    # Reinsertar los bloques de código resaltados
    for placeholder, highlighted_code in code_blocks.items():
        html = html.replace(f"<p>{placeholder}</p>", highlighted_code)

    return html


def generate_syllabus_prompt(subject_name: str, academic_context_str: str) -> str:
    """
    Genera un prompt específico para solicitar a la IA la creación de un temario en YAML.
    """
    prompt = (
        "**ROL Y MISIÓN:**\n"
        "Actúa como un experto diseñador instruccional y catedrático universitario. "
        "Tu ÚNICA misión es generar un temario detallado y exhaustivo para la "
        "asignatura indicada.\n\n"
        "**CONTEXTO ACADÉMICO:**\n"
        f"{academic_context_str}\n\n"
        "**INSTRUCCIONES DE FORMATO (OBLIGATORIAS):**\n"
        "1.  **FORMATO DE SALIDA:** Tu respuesta debe ser EXCLUSIVAMENTE un bloque "
        "de código YAML válido. No incluyas ningún saludo, explicación o "
        "comentario fuera del bloque YAML.\n"
        "2.  **ESTRUCTURA YAML:** La estructura debe seguir este esquema exacto:\n"
        "    - Una clave raíz llamada `temario`.\n"
        "    - `temario` contiene una lista de diccionarios.\n"
        "    - Cada diccionario representa un módulo principal y debe tener dos "
        "claves: `modulo` (el título) y `secciones`.\n"
        "    - `secciones` contiene una lista de diccionarios.\n"
        "    - Cada diccionario de sección representa un subtema y debe tener una "
        "única clave `seccion` (el título).\n"
        "3.  **REGLAS ADICIONALES:**\n"
        '    - NO incluyas numeración en los títulos (ej: "1. Introducción"). '
        "El orden de la lista es suficiente.\n"
        "    - El temario debe ser profundo y extenso, adecuado para un curso "
        "universitario. Cubre desde los fundamentos hasta los conceptos más "
        "avanzados.\n"
        "    - NO desarrolles ningún contenido, solo genera la estructura del temario.\n\n"
        "**EJEMPLO DE LA ESTRUCTURA ESPERADA:**\n"
        "```yaml\n"
        "temario:\n"
        '  - modulo: "Introducción a la Programación Orientada a Objetos"\n'
        "    secciones:\n"
        '      - seccion: "Paradigmas de programación"\n'
        '      - seccion: "Clases y Objetos"\n'
        '      - seccion: "Herencia y Polimorfismo"\n'
        '  - modulo: "Estructuras de Datos Fundamentales"\n'
        "    secciones:\n"
        '      - seccion: "Arrays y Listas Enlazadas"\n'
        '      - seccion: "Pilas y Colas"\n'
        '      - seccion: "Árboles y Grafos"\n'
        "```\n\n"
        "**ASIGNATURA A DESARROLLAR:**\n"
        f"{subject_name}\n\n"
        "**ORDEN FINAL:**\n"
        "Procede a generar el temario en formato YAML."
    )
    return prompt.strip()


def generate_master_prompt(title, markdown_skeleton_with_yaml):
    """
    [LEGACY] Genera el prompt maestro y unificado para la IA. VERSIÓN FINAL ROBUSTA.
    """
    full_prompt = (
        "**ROL Y MISIÓN:**\n"
        "Actúa como un **catedrático universitario experto** en la materia, un "
        "diseñador instruccional de élite y un redactor técnico consumado. "
        "Tu misión es generar un curso completo, extenso y de **máxima "
        "profundidad teórica** en formato Markdown.\n\n"
        "**PÚBLICO OBJETIVO (CRÍTICO):**\n"
        "El contenido está dirigido a **estudiantes universitarios**, "
        "posiblemente de postgrado. Se espera un alto nivel de detalle, "
        "rigor académico y el uso de terminología técnica precisa y correcta. "
        "**Evita simplificaciones excesivas** o analogías propias de la "
        "divulgación para un público general.\n\n"
        "**INSTRUCCIONES DE CONTENIDO (MUY ESTRICTAS):**\n"
        "1.  **PROFUNDIDAD Y RIGOR:** Desarrolla cada tema y subtema con la "
        "mayor exhaustividad posible. Prioriza la densidad de información y "
        "la conexión entre conceptos. Cita teorías fundamentales y autores "
        "relevantes en el campo cuando sea apropiado.\n"
        "2.  **100% TEÓRICO:** El curso debe ser íntegramente teórico. "
        "Queda estrictamente PROHIBIDO incluir ejercicios, casos prácticos, "
        "proyectos, preguntas de examen o cualquier forma de contenido práctico. "
        "El objetivo es construir una base de conocimiento, no un manual de "
        "ejercicios.\n"
        "3.  **EXTENSIÓN:** El curso debe ser lo más extenso posible, "
        "superando los 60.000 tokens de contenido desarrollado.\n\n"
        "**INSTRUCCIONES DE FORMATO (OBLIGATORIAS):**\n"
        "1.  **METADATOS YAML:** Analiza el esqueleto proporcionado y completa "
        "TODOS los campos marcados como `[...COMPLETAR...]` en la cabecera YAML. "
        "La clasificación intelectual debe ser precisa y coherente.\n"
        "2.  **TABLA DE CONTENIDOS (TOC):** Crea un temario multinivel muy detallado. "
        "Usa enlaces de ancla: `[Título](#titulo-amigable-en-minusculas)`.\n"
        "3.  **CUERPO DEL CONTENIDO:**\n"
        "    *   **ANCLAS HTML:** INMEDIATAMENTE ANTES de CADA encabezado (`##`, `###`), "
        'inserta la etiqueta de ancla correspondiente: `<a id="titulo-amigable-en-minusculas"></a>`. '
        "El `id` debe coincidir EXACTAMENTE con el de la TOC.\n"
        "    *   **NAVEGACIÓN:** Al final de cada Módulo principal (`##`), "
        "añade el enlace `[⬆️ Volver al índice](#tabla-de-contenidos)`.\n"
        "4.  **SALIDA FINAL:** Tu respuesta debe ser EXCLUSIVAMENTE el código "
        "Markdown del archivo completo. NO incluyas ningún saludo, explicación "
        "o comentario antes del `---` inicial o después de la última línea "
        "de contenido.\n\n"
        "---\n"
        "**ESQUELETO DEL CURSO A COMPLETAR:**\n"
        f"{markdown_skeleton_with_yaml.strip()}\n\n"
        "**ORDEN FINAL IMPERATIVA:**\n"
        "Has analizado la estructura y la cabecera. Ahora, procede a desarrollar "
        "el **CUERPO COMPLETO DEL CONTENIDO** siguiendo todas las instrucciones "
        "de profundidad, rigor y extensión. La respuesta DEBE incluir el "
        "desarrollo íntegro de todos los puntos del temario. No te detengas "
        "hasta haber completado todo el curso."
    )
    return full_prompt.strip()

def normalize_json_for_hash(data: dict) -> str:
    """
    Normaliza un diccionario o lista Python a una cadena JSON consistente
    para la generación de hashes deterministas.
    
    Asegura:
    1. Ordenación de claves alfabética (sort_keys=True).
    2. Separadores compactos (separators=(',', ':')).
    3. Evita saltos de línea innecesarios.
    """
    if not data:
        return ""
    
    # Usamos json.dumps para serializar el objeto con una ordenación canónica
    # y sin espacios, lo que lo hace determinista.
    return json.dumps(
        data, 
        sort_keys=True, 
        indent=None, 
        separators=(',', ':')
    )
