# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/base.py
"""
Abstract base class for all exam strategies.
Defines the mandatory contract, shared grading motors, rigor matrix
and skeleton/prompt generation pipeline.
Complies with V06DOC_STRUCTURE, V06DOC_BLOCKS, V06DOC_LEVELS, V06DOC_TEMPLATES (v5.9).
---
Clase abstracta base para todas las estrategias de examen.
Define el contrato obligatorio, los motores de calificación compartidos, la matriz
de rigor y el pipeline de generación de esqueleto/prompt.
Cumple con V06DOC_STRUCTURE, V06DOC_BLOCKS, V06DOC_LEVELS, V06DOC_TEMPLATES (v5.9).
"""
from abc import ABC, abstractmethod
from decimal import Decimal
from assessment_v2.services.tracking import TrackingService


class BaseExamStrategy(ABC):
    """
    Abstract base class defining the common contract for all exam strategies.
    All archetypes must inherit from this class and implement the abstract methods.
    Sub-archetype identity is injected at construction time and governs all decisions.
    ---
    Clase abstracta base que define el contrato común para todas las estrategias de examen.
    Todos los arquetipos deben heredar de esta clase e implementar los métodos abstractos.
    La identidad del sub-arquetipo se inyecta en construcción y gobierna todas las decisiones.
    Ref: V06DOC_STRUCTURE (Sección 1 — SCHEMA-FIRST Protocol).
    """

    def __init__(
        self,
        sub_archetype_id,
        pedagogical_level='LVL_B',
        itinerary_id='ITIN_MIN',
        **kwargs
    ):
        """
        Initializes the strategy with the full academic context.
        Pre-calculates rigor parameters immediately for use throughout the session.
        ---
        Inicializa la estrategia con el contexto académico completo.
        Pre-calcula los parámetros de rigor inmediatamente para su uso en toda la sesión.
        """
        self.sub_archetype_id  = sub_archetype_id
        self.pedagogical_level = pedagogical_level
        self.itinerary_id      = itinerary_id
        self.config            = kwargs  # target_language_code, localized_sections, etc.

        # Pre-calculation of rigor parameters / Pre-cálculo de parámetros de rigor
        # Ref: V06DOC_LEVELS (Matriz de Intersección LVL × ITIN)
        self.rigor_params = self._get_grading_params()

    # ==========================================================================
    # ABSTRACT METHODS — Must be implemented by each archetype strategy
    # MÉTODOS ABSTRACTOS — Deben ser implementados por cada estrategia de arquetipo
    # ==========================================================================

    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Returns the AI system prompt specific to this archetype and sub-archetype.
        Defines the AI's role, academic register and generation constraints.
        ---
        Devuelve el prompt de sistema específico para este arquetipo y sub-arquetipo.
        Define el rol de la IA, el registro académico y las restricciones de generación.
        """
        pass

    @abstractmethod
    def get_user_prompt(
        self,
        context_text: str,
        topic: str,
        subdivision_id: str,
        generated_item_titles: list = None,
        skeleton_json: str = None
    ) -> str:
        """
        Generates the user prompt injecting the study material context and skeleton.
        Must include all information the AI needs to fill the section items correctly.
        ---
        Genera el prompt de usuario inyectando el contexto del material de estudio y el esqueleto.
        Debe incluir toda la información que la IA necesita para rellenar los ítems de la sección.
        """
        pass

    @abstractmethod
    def get_exam_skeleton(self) -> list:
        """
        Returns the full structural skeleton for the exam.
        Each entry is a section dict with: subdivision_id, title, instructions,
        layout_mode, time_limit, and items (list of item dicts with block_type,
        widget_id, task_instruction, weight, fail_logic, level_requisite).
        ---
        Devuelve el esqueleto estructural completo del examen.
        Cada entrada es un dict de sección con: subdivision_id, title, instructions,
        layout_mode, time_limit, e items (lista de dicts de ítem con block_type,
        widget_id, task_instruction, weight, fail_logic, level_requisite).
        Ref: V06DOC_STRUCTURE (Sección 2.2 — Skeleton-First Protocol).
        """
        pass

    @abstractmethod
    def grade_item(self, item, student_input) -> tuple:
        """
        Grades a single item and returns (score: Decimal, feedback: dict).
        Score must be in range [0.0, 1.0] before rigor adjustment.
        Feedback dict must contain at minimum: 'feedback_category', 'justification'.
        ---
        Califica un único ítem y devuelve (puntuación: Decimal, feedback: dict).
        La puntuación debe estar en rango [0.0, 1.0] antes del ajuste de rigor.
        El dict de feedback debe contener como mínimo: 'feedback_category', 'justification'.
        Ref: V06DOC_BLOCKS (Contrato de Motor de Calificación).
        """
        pass

    # ==========================================================================
    # SHARED GRADING MOTORS — Available to all strategies
    # MOTORES DE CALIFICACIÓN COMPARTIDOS — Disponibles para todas las estrategias
    # Ref: V06DOC_BLOCKS (Sección 1 — Motores Objetivos y Estructurales)
    # ==========================================================================

    def _grade_prm_strike(self, item, student_input) -> tuple:
        """
        PRM-STRIKE motor: Multiple choice with progressive penalty formula.
        Formula: A - E/(N-1) where A=aciertos, E=errores, N=opciones totales.
        NO_NEGATIVE_MARKING override applies when declared in grading_logic.
        ---
        Motor PRM-STRIKE: Opción múltiple con fórmula de penalización progresiva.
        Fórmula: A - E/(N-1) donde A=aciertos, E=errores, N=opciones totales.
        La anulación NO_NEGATIVE_MARKING se aplica cuando se declara en grading_logic.
        Ref: V06DOC_BLOCKS Sección 1.1 (PRM-STRIKE), V06DOC_METADATA Sec 5.
        """
        logic = item.grading_logic
        correct_answer = str(logic.get('correct_answer', '')).strip().upper()
        no_negative    = bool(logic.get('no_negative_marking', False))
        n_options      = len(item.content.get('options', [])) or 4

        student_answer = ''
        if isinstance(student_input, str):
            student_answer = student_input.strip().upper()
        elif isinstance(student_input, dict):
            student_answer = str(student_input.get('selected', student_input.get('value', ''))).strip().upper()

        if not student_answer:
            return Decimal('0.0'), {
                'status': 'OMITTED',
                'feedback_category': 'FB_CONCEPT',
                'justification': logic.get('feedback_justification', 'Pregunta no respondida.')
            }

        if student_answer == correct_answer:
            return Decimal('1.0'), {
                'status': 'CORRECT',
                'feedback_category': 'FB_CONCEPT',
                'justification': logic.get('feedback_justification', 'Respuesta correcta.')
            }

        # Wrong answer / Respuesta incorrecta
        if no_negative:
            # NO_NEGATIVE_MARKING: no penalty, simply 0 / Sin penalización, simplemente 0
            penalty = Decimal('0.0')
        else:
            # Standard UGR formula: A - E/(N-1) / Fórmula UGR estándar: A - E/(N-1)
            # Negative score is returned raw so GradingOrchestrator aggregates correctly.
            # El orquestador recorta a 0.0 a nivel de sección, no el motor por ítem.
            penalty = Decimal('1') / Decimal(str(n_options - 1))

        score = Decimal('0.0') - penalty
        return score, {
            'status': 'INCORRECT',
            'feedback_category': 'FB_CONCEPT',
            'justification': logic.get('feedback_justification', 'Respuesta incorrecta.'),
            'penalty_applied': float(penalty),
            'no_negative_marking': no_negative
        }

    def _grade_rbt_canon(self, item, student_input) -> tuple:
        """
        RBT-CANON motor: Short exact-match answer. No partial credit.
        Accepts pipe-separated variants in grading_logic.correct_answer.
        ---
        Motor RBT-CANON: Respuesta breve de coincidencia exacta. Sin crédito parcial.
        Acepta variantes separadas por '|' en grading_logic.correct_answer.
        Ref: V06DOC_BLOCKS Sección 1.2 (RBT-CANON).
        """
        logic = item.grading_logic
        raw_correct = str(logic.get('correct_answer', ''))
        valid_answers = [v.strip().lower() for v in raw_correct.split('|') if v.strip()]
        student_answer = str(student_input).strip().lower()

        if not student_answer:
            return Decimal('0.0'), {
                'status': 'OMITTED',
                'feedback_category': 'FB_CONCEPT',
                'justification': logic.get('feedback_justification', 'Término no proporcionado.')
            }

        if student_answer in valid_answers:
            return Decimal('1.0'), {
                'status': 'CORRECT',
                'feedback_category': 'FB_CONCEPT',
                'justification': logic.get('feedback_justification', 'Término correcto.')
            }

        return Decimal('0.0'), {
            'status': 'INCORRECT',
            'feedback_category': 'FB_FORMAL',
            'justification': logic.get('feedback_justification', 'El término no coincide con la respuesta canónica esperada.')
        }

    def _grade_rbt_short_lang(self, item, student_input) -> tuple:
        """
        RBT-SHORT-LANG motor: Short linguistic answer (≤4 words, CertAcles/CLM-UGR).
        Applies NO_NEGATIVE_MARKING per CLM-UGR protocol.
        Accepts pipe-separated variants. Case and accent insensitive.
        ---
        Motor RBT-SHORT-LANG: Respuesta lingüística breve (≤4 palabras, CertAcles/CLM-UGR).
        Aplica NO_NEGATIVE_MARKING según protocolo CLM-UGR.
        Acepta variantes separadas por '|'. Insensible a mayúsculas y acentos.
        Ref: V06DOC_BLOCKS Sección 1.3 (RBT-SHORT-LANG), V06DOC_METADATA Sec 5.
        """
        import unicodedata

        def normalize(text):
            # Remove accents and lowercase / Eliminar acentos y pasar a minúsculas
            nfkd = unicodedata.normalize('NFKD', text)
            return ''.join(c for c in nfkd if not unicodedata.combining(c)).lower().strip()

        logic = item.grading_logic
        raw_correct = str(logic.get('correct_answer', ''))
        valid_answers = [normalize(v) for v in raw_correct.split('|') if v.strip()]
        student_answer = normalize(str(student_input))

        if not student_answer:
            return Decimal('0.0'), {
                'status': 'OMITTED',
                'feedback_category': 'FB_CONCEPT',
                'justification': logic.get('feedback_justification', 'Respuesta no proporcionada.')
            }

        if student_answer in valid_answers:
            return Decimal('1.0'), {
                'status': 'CORRECT',
                'feedback_category': 'FB_CONCEPT',
                'justification': logic.get('feedback_justification', 'Respuesta correcta.')
            }

        # NO_NEGATIVE_MARKING always active for this motor / Siempre activo para este motor
        return Decimal('0.0'), {
            'status': 'INCORRECT',
            'feedback_category': 'FB_FORMAL',
            'justification': logic.get('feedback_justification', 'La respuesta no coincide con ninguna variante aceptada.'),
            'no_negative_marking': True
        }

    @staticmethod
    def _strip_gap_brackets(key) -> str:
        """
        Canonical form of a gap key: bare identifier, no surrounding brackets.
        The exam template writes data-gap-id straight from the regex match, which
        includes the brackets ('[HUECO_ID_1]'), while the AI emits the bare id
        ('HUECO_ID_1'). Both sides are canonicalised here before any comparison.
        ---
        Forma canónica de la clave de un hueco: identificador desnudo, sin corchetes.
        La plantilla del examen escribe data-gap-id directamente desde la coincidencia
        del regex, que incluye los corchetes ('[HUECO_ID_1]'), mientras que la IA emite
        el identificador desnudo ('HUECO_ID_1'). Ambos lados se canonizan aquí antes de
        cualquier comparación. Incidencia real S025: sin este saneado, todo ítem cloze
        se calificaba con 0 aunque el alumno acertase todos los huecos.
        """
        return str(key).strip().strip('[]').strip()

    @classmethod
    def _normalize_gap_solutions(cls, raw) -> dict:
        """
        Normalizes gap_solutions to {gap_id: accepted_answer} regardless of shape.
        Accepts the current AI contract (list of {gap_id, accepted_answer}) and the
        legacy dict shape stored in exams generated before the schema fix. Keys are
        canonicalised without brackets.
        ---
        Normaliza gap_solutions a {gap_id: respuesta_aceptada} sea cual sea su forma.
        Acepta el contrato actual de la IA (lista de {gap_id, accepted_answer}) y la
        forma dict antigua, presente en exámenes generados antes de la corrección del
        esquema. La lista es obligatoria en el schema porque la API de Gemini rechaza
        'additionalProperties', que Pydantic emite para cualquier dict sin parametrizar.
        Las claves se canonizan sin corchetes.
        """
        if not raw:
            return {}
        if isinstance(raw, dict):
            return {cls._strip_gap_brackets(k): v for k, v in raw.items()}
        if isinstance(raw, list):
            normalized = {}
            for entry in raw:
                if isinstance(entry, dict) and entry.get('gap_id') is not None:
                    normalized[cls._strip_gap_brackets(entry['gap_id'])] = entry.get('accepted_answer', '')
            return normalized
        return {}

    @classmethod
    def _normalize_student_gaps(cls, student_input) -> dict:
        """
        Canonicalises the keys of the student's cloze answers, so grading does not
        depend on whether the browser submitted bracketed or bare gap ids.
        ---
        Canoniza las claves de las respuestas de cloze del alumno, para que la
        calificación no dependa de si el navegador envió los identificadores con
        corchetes o sin ellos.
        """
        if not isinstance(student_input, dict):
            return {}
        return {cls._strip_gap_brackets(k): v for k, v in student_input.items()}

    def _grade_clo_open(self, item, student_input) -> tuple:
        """
        CLO-OPEN motor: Open gap-filling. Validates each gap independently.
        gap_solutions arrives as a list of {gap_id, accepted_answer} and is normalized
        to a dict before grading. Pipe-separated variants accepted per gap.
        ---
        Motor CLO-OPEN: Rellenado abierto de huecos. Valida cada hueco de forma independiente.
        gap_solutions llega como lista de {gap_id, accepted_answer} y se normaliza a dict
        antes de calificar. Se aceptan variantes separadas por '|' por hueco.
        Ref: V06DOC_BLOCKS Sección 3.1 (CLO-OPEN).
        """
        logic = item.grading_logic
        gap_solutions = self._normalize_gap_solutions(logic.get('gap_solutions'))
        no_negative   = bool(logic.get('no_negative_marking', False))

        if not gap_solutions:
            return Decimal('1.0'), {
                'status': 'NO_SOLUTION_DEFINED',
                'feedback_category': 'FB_CONCEPT',
                'justification': 'No se definieron soluciones para los huecos.'
            }

        # student_input is expected as {gap_id: student_value}
        # student_input se espera como {gap_id: valor_del_alumno}
        if not isinstance(student_input, dict):
            return Decimal('0.0'), {
                'status': 'INVALID_FORMAT',
                'feedback_category': 'FB_PROCEDURAL',
                'justification': 'Formato de respuesta de cloze incorrecto.'
            }

        student_input = self._normalize_student_gaps(student_input)

        total_gaps  = len(gap_solutions)
        correct_gaps = 0
        gap_detail  = {}

        for gap_id, correct_raw in gap_solutions.items():
            valid_variants  = [v.strip().lower() for v in str(correct_raw).split('|')]
            student_val     = str(student_input.get(gap_id, '')).strip().lower()
            is_correct      = student_val in valid_variants
            if is_correct:
                correct_gaps += 1
            gap_detail[gap_id] = {
                'student': student_val,
                'correct': is_correct
            }

        wrong_gaps = total_gaps - correct_gaps

        if no_negative:
            raw_score = Decimal(str(correct_gaps)) / Decimal(str(total_gaps))
        else:
            # Standard penalty: each wrong gap subtracts its share
            # Penalización estándar: cada hueco erróneo resta su fracción
            raw_score = max(
                Decimal('0.0'),
                (Decimal(str(correct_gaps)) - Decimal(str(wrong_gaps * 0.5))) / Decimal(str(total_gaps))
            )

        return raw_score, {
            'status': 'GRADED',
            'feedback_category': 'FB_FORMAL' if wrong_gaps > 0 else 'FB_CONCEPT',
            'justification': logic.get('feedback_justification', f'{correct_gaps}/{total_gaps} huecos correctos.'),
            'gap_detail': gap_detail,
            'correct_gaps': correct_gaps,
            'total_gaps': total_gaps
        }

    def _grade_clo_multi(self, item, student_input) -> tuple:
        """
        CLO-MULTI motor: Multiple-choice gap-filling. Each gap has predefined options.
        No penalty by default (distractors penalize implicitly via wrong selection).
        ---
        Motor CLO-MULTI: Rellenado de huecos con opciones predefinidas.
        Sin penalización por defecto (los distractores penalizan implícitamente).
        Ref: V06DOC_BLOCKS Sección 3.2 (CLO-MULTI).
        """
        # CLO-MULTI shares the same gap-resolution logic as CLO-OPEN
        # but always with no_negative_marking=True (options already constrain choices)
        # CLO-MULTI comparte la lógica de resolución de CLO-OPEN
        # pero siempre con no_negative_marking=True (las opciones ya restringen las elecciones)
        logic = item.grading_logic
        gap_solutions = self._normalize_gap_solutions(logic.get('gap_solutions'))

        if not gap_solutions:
            return Decimal('1.0'), {
                'status': 'NO_SOLUTION_DEFINED',
                'feedback_category': 'FB_CONCEPT',
                'justification': 'No se definieron soluciones para los huecos.'
            }

        if not isinstance(student_input, dict):
            return Decimal('0.0'), {
                'status': 'INVALID_FORMAT',
                'feedback_category': 'FB_PROCEDURAL',
                'justification': 'Formato de respuesta de cloze incorrecto.'
            }

        student_input = self._normalize_student_gaps(student_input)

        total_gaps   = len(gap_solutions)
        correct_gaps = 0
        gap_detail   = {}

        for gap_id, correct_raw in gap_solutions.items():
            valid_variants = [v.strip().lower() for v in str(correct_raw).split('|')]
            student_val    = str(student_input.get(gap_id, '')).strip().lower()
            is_correct     = student_val in valid_variants
            if is_correct:
                correct_gaps += 1
            gap_detail[gap_id] = {
                'student': student_val,
                'correct': is_correct
            }

        raw_score = Decimal(str(correct_gaps)) / Decimal(str(total_gaps))
        return raw_score, {
            'status': 'GRADED',
            'feedback_category': 'FB_FORMAL' if correct_gaps < total_gaps else 'FB_CONCEPT',
            'justification': logic.get('feedback_justification', f'{correct_gaps}/{total_gaps} huecos correctos.'),
            'gap_detail': gap_detail,
            'correct_gaps': correct_gaps,
            'total_gaps': total_gaps
        }

    @classmethod
    def _normalize_pairs(cls, raw) -> dict:
        """
        Normalizes matching pairs to {left: right} regardless of shape.
        The AI contract is a list of {izquierdo, derecho}; the legacy shape was a
        plain dict. Grading always works on the dict form.
        ---
        Normaliza los pares de vinculacion a {izquierdo: derecho} sea cual sea su
        forma. El contrato de la IA es una lista de {izquierdo, derecho}, igual que
        gap_solutions y por la misma razon (Gemini rechaza 'additionalProperties',
        que Pydantic emite para cualquier dict sin parametrizar). La forma antigua
        era un dict plano. La calificacion trabaja siempre sobre el dict.
        Incidencia real S025: sin esta normalizacion, _grade_mat_link llamaba a
        .items() sobre una lista y la correccion entera del examen reventaba con
        "'list' object has no attribute 'items'", visible para el alumno.
        """
        if not raw:
            return {}
        if isinstance(raw, dict):
            return raw
        if isinstance(raw, list):
            normalized = {}
            for entry in raw:
                if isinstance(entry, dict) and entry.get('izquierdo') is not None:
                    normalized[str(entry['izquierdo'])] = entry.get('derecho', '')
            return normalized
        return {}

    def _grade_mat_link(self, item, student_input) -> tuple:
        """
        MAT-LINK motor: Drag & drop matching. Scores proportionally by correct pairs.
        pairs in grading_logic arrives as a list of {izquierdo, derecho} and is
        normalized to {left: right} before grading.
        student_input expected as {source_text: student_target}.
        ---
        Motor MAT-LINK: Emparejamiento por arrastre. Califica proporcionalmente por pares correctos.
        pairs en grading_logic llega como lista de {izquierdo, derecho} y se normaliza
        a {izquierdo: derecho} antes de calificar.
        student_input se espera como {texto_fuente: destino_del_alumno}.
        Ref: V06DOC_BLOCKS Sección 3.3 (MAT-LINK).
        """
        logic  = item.grading_logic
        pairs  = self._normalize_pairs(logic.get('pairs'))

        if not pairs:
            return Decimal('1.0'), {
                'status': 'NO_PAIRS_DEFINED',
                'feedback_category': 'FB_CONCEPT',
                'justification': 'No se definieron pares de vinculación.'
            }

        if not isinstance(student_input, dict):
            return Decimal('0.0'), {
                'status': 'INVALID_FORMAT',
                'feedback_category': 'FB_PROCEDURAL',
                'justification': 'Formato de respuesta de emparejamiento incorrecto.'
            }

        total_pairs   = len(pairs)
        correct_pairs = sum(
            1 for source, correct_target in pairs.items()
            if str(student_input.get(source, '')).strip().lower() == str(correct_target).strip().lower()
        )

        raw_score = Decimal(str(correct_pairs)) / Decimal(str(total_pairs))
        return raw_score, {
            'status': 'GRADED',
            'feedback_category': 'FB_PROCEDURAL' if correct_pairs < total_pairs else 'FB_CONCEPT',
            'justification': logic.get('feedback_justification', f'{correct_pairs}/{total_pairs} pares correctos.'),
            'correct_pairs': correct_pairs,
            'total_pairs': total_pairs
        }

    def _grade_cds_kill(self, item, student_input) -> tuple:
        """
        CDS-KILL motor: Safety-critical dichotomous checklist.
        A wrong answer (False when True expected, or vice versa) triggers KILL_SWITCH.
        If kill_switch is declared True in grading_logic, wrong answers annul the section.
        ---
        Motor CDS-KILL: Checklist dicotómico de seguridad crítica.
        Una respuesta incorrecta activa el KILL_SWITCH si kill_switch=True en grading_logic.
        Ref: V06DOC_BLOCKS Sección 2.4 (CDS-KILL).
        """
        logic         = item.grading_logic
        correct_raw   = str(logic.get('correct_answer', 'True')).strip().lower()
        correct_bool  = correct_raw in ('true', '1', 'yes', 'sí', 'si')
        is_kill_switch = bool(logic.get('kill_switch', False))

        # Parse student input / Parsear entrada del alumno
        if isinstance(student_input, dict):
            student_bool = bool(student_input.get('checked', False))
        elif isinstance(student_input, bool):
            student_bool = student_input
        else:
            student_bool = str(student_input).strip().lower() in ('true', '1', 'yes', 'sí', 'si', 'checked')

        is_correct = (student_bool == correct_bool)

        if is_correct:
            return Decimal('1.0'), {
                'status': 'CORRECT',
                'feedback_category': 'FB_PROCEDURAL',
                'justification': logic.get('feedback_justification', 'Paso crítico ejecutado correctamente.'),
                'kill_switch_activated': False
            }

        # Wrong answer / Respuesta incorrecta
        feedback = {
            'status': 'INCORRECT',
            'feedback_category': 'FB_SAFETY',
            'justification': (
                'ERROR DE SEGURIDAD CRÍTICA: ' +
                logic.get('feedback_justification', 'El paso crítico no se ejecutó correctamente.')
            ),
            'kill_switch_activated': is_kill_switch
        }
        return Decimal('0.0'), feedback

    def _grade_dra_holo(self, item, student_input) -> tuple:
        """
        DRA-HOLO motor: Holistic analytical rubric — 4 axes (UGR/CertAcles standard).
        Axes: adecuacion_encargo (0.25), coherencia_cohesion (0.25),
              riqueza_lexica (0.25), correccion_gramatical (0.25).
        Word count check from grading_logic.word_count_range.
        Requires AI evaluation call — returns PENDING_AI_ANALYSIS for async grading.
        Without AI: falls back to formal quality heuristics.
        ---
        Motor DRA-HOLO: Rúbrica analítica holística — 4 ejes (estándar UGR/CertAcles).
        Ejes: adecuacion_encargo (0.25), coherencia_cohesion (0.25),
              riqueza_lexica (0.25), correccion_gramatical (0.25).
        Comprobación de recuento de palabras desde grading_logic.word_count_range.
        Requiere llamada de evaluación por IA — devuelve PENDING_AI_ANALYSIS para calificación asíncrona.
        Sin IA: recurre a heurísticas de calidad formal.
        Ref: V06DOC_BLOCKS Sección 2.2 (DRA-HOLO).
        """
        logic = item.grading_logic

        student_text = ''
        formal_penalty = Decimal('0.0')

        if isinstance(student_input, dict):
            student_text   = str(student_input.get('text', '')).strip()
            formal_penalty = Decimal(str(student_input.get('formal_penalty', 0.0)))
        else:
            student_text = str(student_input).strip()

        if not student_text:
            return Decimal('0.0'), {
                'status': 'OMITTED',
                'feedback_category': 'FB_FORMAL',
                'justification': 'No se ha proporcionado ningún texto para evaluar.'
            }

        word_count = len(student_text.split())

        # Word count range check / Comprobación del rango de extensión
        word_range = logic.get('word_count_range', {})
        min_words  = word_range.get('min', 0)
        max_words  = word_range.get('max', 99999)

        if word_count < min_words:
            # Severe penalty for texts below minimum / Penalización severa por texto bajo mínimo
            length_penalty = Decimal('0.3')
        elif word_count > max_words:
            # Moderate penalty for texts above maximum / Penalización moderada por exceso
            length_penalty = Decimal('0.1')
        else:
            length_penalty = Decimal('0.0')

        # Rubric axes / Ejes de la rúbrica
        # Default weights if not declared in grading_logic
        # Pesos por defecto si no se declaran en grading_logic
        rubric_axes = logic.get('rubric_axes', {
            'adecuacion_encargo':     0.25,
            'coherencia_cohesion':    0.25,
            'riqueza_lexica':         0.25,
            'correccion_gramatical':  0.25
        })

        # Heuristic evaluation pending full AI scoring
        # Evaluación heurística pendiente de la calificación completa por IA
        # This score will be refined by the async AI evaluation pass
        # Esta nota será refinada por el paso de evaluación asíncrona por IA
        heuristic_score = Decimal('0.6')  # Base competent score / Nota base competente

        # Apply formal penalty from frontend quality metric
        # Aplicar penalización formal de la métrica de calidad del frontend
        heuristic_score = max(Decimal('0.0'), heuristic_score + formal_penalty)

        # Apply length penalty / Aplicar penalización por extensión
        heuristic_score = max(Decimal('0.0'), heuristic_score - length_penalty)

        return heuristic_score, {
            'status': 'PENDING_AI_ANALYSIS',
            'feedback_category': 'FB_FORMAL',
            'justification': logic.get(
                'feedback_justification',
                f'Texto recibido ({word_count} palabras). Evaluación holística pendiente de análisis por IA.'
            ),
            'word_count': word_count,
            'word_count_range': word_range,
            'rubric_axes': rubric_axes,
            'heuristic_score': float(heuristic_score),
            'pending_ai_refinement': True
        }

    def _grade_dra_holo_lit(self, item, student_input) -> tuple:
        """
        DRA-HOLO-LIT motor: Literary holistic rubric for TRA-LIT (FTI-UGR).
        Axes: adecuacion_skopos (0.30), gestion_culturemas (0.25),
              calidad_literaria (0.25), rigor_comentario (0.20).
        Turnitin submission required — without file_uploaded=True returns PENDING.
        ---
        Motor DRA-HOLO-LIT: Rúbrica holística literaria para TRA-LIT (FTI-UGR).
        Ejes: adecuacion_skopos (0.30), gestion_culturemas (0.25),
              calidad_literaria (0.25), rigor_comentario (0.20).
        Requiere envío por Turnitin — sin file_uploaded=True devuelve PENDING.
        Ref: V06DOC_BLOCKS Sección 2.2.1 (DRA-HOLO-LIT), V06DOC_SUBARCHETYPES SUB-LIN-TRA-LIT.
        """
        logic = item.grading_logic

        student_text   = ''
        formal_penalty = Decimal('0.0')
        file_uploaded  = False

        if isinstance(student_input, dict):
            student_text   = str(student_input.get('text', '')).strip()
            formal_penalty = Decimal(str(student_input.get('formal_penalty', 0.0)))
            file_uploaded  = bool(student_input.get('file_uploaded', False))
        else:
            student_text = str(student_input).strip()

        if not student_text and not file_uploaded:
            return Decimal('0.0'), {
                'status': 'OMITTED',
                'feedback_category': 'FB_FORMAL',
                'justification': 'No se ha proporcionado ninguna traducción literaria para evaluar.'
            }

        word_count = len(student_text.split()) if student_text else 0

        rubric_axes = logic.get('rubric_axes', {
            'adecuacion_skopos':   0.30,
            'gestion_culturemas':  0.25,
            'calidad_literaria':   0.25,
            'rigor_comentario':    0.20
        })

        heuristic_score = Decimal('0.6')
        heuristic_score = max(Decimal('0.0'), heuristic_score + formal_penalty)

        return heuristic_score, {
            'status': 'PENDING_AI_ANALYSIS',
            'feedback_category': 'FB_FORMAL',
            'justification': logic.get(
                'feedback_justification',
                f'Traducción literaria recibida ({word_count} palabras). '
                f'Evaluación holística literaria pendiente de análisis por IA.'
            ),
            'word_count': word_count,
            'rubric_axes': rubric_axes,
            'file_uploaded': file_uploaded,
            'turnitin_required': True,
            'pending_ai_refinement': True
        }

    def _grade_bmt_shift(self, item, student_input) -> tuple:
        """
        BMT-SHIFT motor: Mediation and register transfer.
        Evaluates informative fidelity (50%) and register adequacy (50%).
        Requires AI evaluation for full scoring — returns heuristic pending AI.
        ---
        Motor BMT-SHIFT: Mediación y transferencia de registro.
        Evalúa fidelidad informativa (50%) y adecuación de registro (50%).
        Requiere evaluación por IA para calificación completa — devuelve heurística pendiente de IA.
        Ref: V06DOC_BLOCKS Sección 2.3 (BMT-SHIFT).
        """
        logic = item.grading_logic

        student_text = str(student_input).strip() if not isinstance(student_input, dict) \
            else str(student_input.get('text', '')).strip()

        if not student_text:
            return Decimal('0.0'), {
                'status': 'OMITTED',
                'feedback_category': 'FB_FORMAL',
                'justification': 'No se ha proporcionado ningún texto de mediación.'
            }

        word_count = len(student_text.split())

        return Decimal('0.6'), {
            'status': 'PENDING_AI_ANALYSIS',
            'feedback_category': 'FB_FORMAL',
            'justification': logic.get(
                'feedback_justification',
                f'Texto de mediación recibido ({word_count} palabras). '
                f'Evaluación de fidelidad y registro pendiente de análisis por IA.'
            ),
            'word_count': word_count,
            'axes': {
                'fidelidad_informativa': 0.50,
                'adecuacion_registro':   0.50
            },
            'pending_ai_refinement': True
        }

    def _grade_ilc_context(self, item, student_input) -> tuple:
        """
        ILC-CONTEXT motor: Interpretation of context and raw data.
        Requires AI evaluation for full clinical/contextual reasoning assessment.
        Markers (coordinates) from W-CLIN-SCAN are preserved in feedback for AI pass.
        ---
        Motor ILC-CONTEXT: Interpretación de contexto y datos brutos.
        Requiere evaluación por IA para la evaluación completa del razonamiento clínico/contextual.
        Los marcadores (coordenadas) de W-CLIN-SCAN se preservan en el feedback para el paso de IA.
        Ref: V06DOC_BLOCKS Sección 2.5 (ILC-CONTEXT).
        """
        logic = item.grading_logic

        student_text = ''
        markers      = []

        if isinstance(student_input, dict):
            student_text = str(student_input.get('text', '')).strip()
            markers      = student_input.get('markers', [])
        else:
            student_text = str(student_input).strip()

        if not student_text:
            return Decimal('0.0'), {
                'status': 'OMITTED',
                'feedback_category': 'FB_CONCEPT',
                'justification': 'No se ha proporcionado ninguna interpretación clínica o contextual.'
            }

        word_count = len(student_text.split())

        return Decimal('0.6'), {
            'status': 'PENDING_AI_ANALYSIS',
            'feedback_category': 'FB_CONCEPT',
            'justification': logic.get(
                'feedback_justification',
                f'Interpretación recibida ({word_count} palabras). '
                f'Análisis de razonamiento clínico/contextual pendiente de evaluación por IA.'
            ),
            'word_count': word_count,
            'markers_received': markers,
            'pending_ai_refinement': True
        }

    def _grade_ev_pale(self, item, student_input) -> tuple:
        """
        EV-PALE motor: Transcription and exegesis of primary sources (Palaeography).
        Validates grapheme accuracy and abbreviation resolution against correct_transcription.
        ---
        Motor EV-PALE: Transcripción y exégesis de fuentes primarias (Paleografía).
        Valida la precisión grafemática y la resolución de braquigrafías frente a correct_transcription.
        Ref: V06DOC_BLOCKS Sección 2.6 (EV-PALE).
        """
        logic = item.grading_logic
        correct_transcription = str(logic.get('correct_transcription', '')).strip().lower()
        student_text = str(student_input).strip().lower() if not isinstance(student_input, dict) \
            else str(student_input.get('text', '')).strip().lower()

        if not student_text:
            return Decimal('0.0'), {
                'status': 'OMITTED',
                'feedback_category': 'FB_PROCEDURAL',
                'justification': 'No se ha proporcionado ninguna transcripción paleográfica.'
            }

        if not correct_transcription:
            return Decimal('0.6'), {
                'status': 'PENDING_AI_ANALYSIS',
                'feedback_category': 'FB_PROCEDURAL',
                'justification': 'Transcripción recibida. Cotejo paleográfico pendiente de evaluación por IA.',
                'pending_ai_refinement': True
            }

        # Character-level similarity / Similaridad a nivel de carácter
        # Uses a simple common-prefix heuristic; full Levenshtein requires async AI pass
        # Usa una heurística de prefijo común; el Levenshtein completo requiere el paso asíncrono de IA
        student_words  = set(student_text.split())
        correct_words  = set(correct_transcription.split())
        if not correct_words:
            return Decimal('0.0'), {
                'status': 'NO_REFERENCE_TRANSCRIPTION',
                'feedback_category': 'FB_PROCEDURAL',
                'justification': 'La transcripción de referencia está vacía.'
            }

        intersection = student_words & correct_words
        recall       = len(intersection) / len(correct_words)
        precision    = len(intersection) / len(student_words) if student_words else 0.0
        f1_score     = (2 * recall * precision / (recall + precision)) if (recall + precision) > 0 else 0.0

        raw_score = Decimal(str(round(f1_score, 4)))

        feedback_cat = 'FB_CONCEPT' if f1_score >= 0.8 else 'FB_FORMAL'
        return raw_score, {
            'status': 'GRADED',
            'feedback_category': feedback_cat,
            'justification': logic.get(
                'feedback_justification',
                f'Precisión paleográfica (F1): {f1_score:.2%}. '
                f'Coincidencia de grafemas: {len(intersection)}/{len(correct_words)} palabras.'
            ),
            'f1_score': float(f1_score),
            'recall': float(recall),
            'precision': float(precision)
        }

    def _grade_ev_tra_precision(self, item, student_input) -> tuple:
        """
        EV-TRA-PRECISION motor: Terminological precision validation in specialized translation.
        Validates lexical equivalences in technical/specialized domains against authority glossaries.
        Evaluates univocity in the target language and register adequacy.
        Full AI evaluation required — returns heuristic pending AI.
        ---
        Motor EV-TRA-PRECISION: Validación de precisión terminológica en traducción especializada.
        Valida equivalencias léxicas en dominios técnico/especializados contra glosarios de autoridad.
        Evalúa la univocidad en la lengua de llegada y la adecuación al registro meta.
        Requiere evaluación completa por IA — devuelve heurística pendiente de IA.
        Ref: V06DOC_BLOCKS Sección 3 (EV-TRA-PRECISION).
        """
        logic = item.grading_logic

        student_text = str(student_input).strip() if not isinstance(student_input, dict) \
            else str(student_input.get('text', '')).strip()

        if not student_text:
            return Decimal('0.0'), {
                'status': 'OMITTED',
                'feedback_category': 'FB_PROCEDURAL',
                'justification': 'No se ha proporcionado ninguna traducción para evaluar.'
            }

        word_count = len(student_text.split())

        # Keyword heuristic: validates presence of expected technical equivalences
        # Heurística de keywords: valida la presencia de equivalencias técnicas esperadas
        keywords = logic.get('keywords', [])
        keyword_hits = sum(1 for kw in keywords if kw.lower() in student_text.lower())
        keyword_ratio = (keyword_hits / len(keywords)) if keywords else 0.5

        heuristic_score = Decimal(str(round(min(keyword_ratio, 1.0), 4)))

        return heuristic_score, {
            'status': 'PENDING_AI_ANALYSIS',
            'feedback_category': 'FB_PROCEDURAL',
            'justification': logic.get(
                'feedback_justification',
                f'Traducción especializada recibida ({word_count} palabras). '
                f'Validación de precisión terminológica y univocidad en lengua meta pendiente de IA.'
            ),
            'word_count': word_count,
            'keyword_hits': keyword_hits,
            'total_keywords': len(keywords),
            'heuristic_score': float(heuristic_score),
            'pending_ai_refinement': True
        }

    def _grade_rpp_traza(self, item, student_input) -> tuple:
        """
        RPP-TRAZA motor: Multi-step procedural resolution with error propagation.
        Evaluates each step independently against step_matrix in grading_logic.
        A correct logical approach (correct first step) preserves 50% of the score.
        A critical step marked with 'critical': True triggers FATAL if wrong (ITIN_PROF only).
        ---
        Motor RPP-TRAZA: Resolución procedimental multietapa con propagación de error.
        Evalúa cada paso de forma independiente frente a step_matrix en grading_logic.
        Un planteamiento lógico correcto (primer paso correcto) preserva el 50% de la nota.
        Un paso crítico marcado con 'critical': True activa FATAL si falla (solo ITIN_PROF).
        Ref: V06DOC_BLOCKS Sección 1.4 (RPP-TRAZA).
        """
        logic       = item.grading_logic
        step_matrix = logic.get('step_matrix', [])

        steps = []
        if isinstance(student_input, dict):
            steps = student_input.get('steps', [])
        elif isinstance(student_input, list):
            steps = student_input

        if not steps:
            return Decimal('0.0'), {
                'status': 'NO_STEPS_PROVIDED',
                'feedback_category': 'FB_PROCEDURAL',
                'justification': logic.get(
                    'feedback_justification',
                    'No se han registrado pasos de resolución.'
                )
            }

        if not step_matrix:
            # No expected matrix defined — minimal score for attempt
            # No se definió matriz esperada — puntuación mínima por intento
            return Decimal('0.3'), {
                'status': 'NO_MATRIX_DEFINED',
                'feedback_category': 'FB_PROCEDURAL',
                'justification': 'No se definió la matriz de pasos esperados.'
            }

        earned_score     = Decimal('0.0')
        total_weight     = Decimal('0.0')
        kill_switch_hit  = False
        step_trace       = []

        # Build student step map by id / Construir mapa de pasos del alumno por id
        student_step_map = {str(s.get('id', '')): str(s.get('value', '')).strip().lower() for s in steps}

        for expected in step_matrix:
            step_id         = str(expected.get('id', ''))
            step_weight     = Decimal(str(expected.get('weight', 0.1)))
            step_critical   = bool(expected.get('critical', False))
            expected_value  = str(expected.get('value', '')).strip().lower()
            student_value   = student_step_map.get(step_id, '')
            total_weight   += step_weight

            # Accept pipe-separated variants / Aceptar variantes separadas por '|'
            valid_values = [v.strip().lower() for v in expected_value.split('|')]
            is_correct   = student_value in valid_values

            if is_correct:
                earned_score += step_weight
                step_trace.append({'id': step_id, 'status': 'CORRECT', 'weight': float(step_weight)})
            else:
                step_trace.append({
                    'id': step_id,
                    'status': 'INCORRECT',
                    'student': student_value,
                    'expected': expected_value,
                    'weight': float(step_weight)
                })
                if step_critical and self.itinerary_id == 'ITIN_PROF':
                    kill_switch_hit = True

        # Normalize score / Normalizar puntuación
        raw_score = (earned_score / total_weight) if total_weight > 0 else Decimal('0.0')

        # Correct logical approach (first step correct) preserves 50% minimum
        # Planteamiento lógico correcto (primer paso correcto) preserva el 50% mínimo
        first_step_id = str(step_matrix[0].get('id', '')) if step_matrix else ''
        first_correct = student_step_map.get(first_step_id, '') in [
            v.strip().lower() for v in str(step_matrix[0].get('value', '')).split('|')
        ] if step_matrix else False

        if first_correct and raw_score < Decimal('0.5'):
            raw_score = Decimal('0.5')

        return raw_score, {
            'status': 'GRADED',
            'feedback_category': 'FB_PROCEDURAL',
            'justification': logic.get(
                'feedback_justification',
                f'Resolución procedimental: {float(raw_score):.2%} de la puntuación total.'
            ),
            'trace': step_trace,
            'kill_switch_activated': kill_switch_hit,
            'first_step_correct': first_correct
        }

    def _grade_dia_interact(self, item, student_input) -> tuple:
        """
        DIA-INTERACT motor: Dialectical interaction evaluated by UniversIA AI.
        Returns PENDING_AI_ANALYSIS with the full chat log preserved for async evaluation.
        ---
        Motor DIA-INTERACT: Interacción dialéctica evaluada por la IA UniversIA.
        Devuelve PENDING_AI_ANALYSIS con el log de chat completo preservado para evaluación asíncrona.
        Ref: V06DOC_BLOCKS Sección 3.4 (DIA-INTERACT).
        """
        logic = item.grading_logic

        chat_log = []
        if isinstance(student_input, list):
            chat_log = student_input
        elif isinstance(student_input, dict):
            chat_log = student_input.get('log', [])

        if not chat_log:
            return Decimal('0.0'), {
                'status': 'OMITTED',
                'feedback_category': 'FB_FORMAL',
                'justification': 'No se registró ninguna interacción dialéctica.'
            }

        turn_count = len([e for e in chat_log if isinstance(e, dict) and e.get('sender') == 'user'])

        return Decimal('0.6'), {
            'status': 'PENDING_AI_ANALYSIS',
            'feedback_category': 'FB_FORMAL',
            'justification': logic.get(
                'feedback_justification',
                f'Interacción dialéctica recibida ({turn_count} turnos del alumno). '
                f'Evaluación de registro y competencia oral pendiente de análisis por IA.'
            ),
            'turn_count': turn_count,
            'chat_log_preserved': chat_log,
            'pending_ai_refinement': True
        }

    # ==========================================================================
    # RIGOR AND SCORING INFRASTRUCTURE
    # INFRAESTRUCTURA DE RIGOR Y PUNTUACIÓN
    # Ref: V06DOC_LEVELS (Matriz de Intersección LVL × ITIN)
    # ==========================================================================

    def _get_grading_params(self) -> dict:
        """
        Calculates rigor_factor and penalty_threshold from the pedagogical
        intersection matrix (LVL × ITIN). Called once at strategy construction.
        Specific sub-archetype overrides must be implemented in each strategy's
        own _get_grading_params() if V06DOC_LEVELS declares divergent values.
        ---
        Calcula rigor_factor y penalty_threshold desde la matriz de intersección
        pedagógica (LVL × ITIN). Se llama una vez en la construcción de la estrategia.
        Las anulaciones específicas por sub-arquetipo deben implementarse en el
        _get_grading_params() de cada estrategia si V06DOC_LEVELS declara valores divergentes.
        Ref: V06DOC_LEVELS Sección 2 (Matriz de Rigor LVL × ITIN).
        """
        # Full intersection matrix / Matriz de intersección completa
        # Ref: V06DOC_LEVELS Sección 2
        matrix = {
            'LVL_A': {
                'ITIN_MIN':  0.8,
                'ITIN_DOC':  0.9,
                'DEFAULT':   1.0
            },
            'LVL_B': {
                'ITIN_MAI':  1.3,
                'ITIN_PROF': 1.3,
                'ITIN_INV':  1.4,
                'ITIN_ROT':  1.2,
                'ITIN_DOC':  1.1,
                'DEFAULT':   1.0
            },
            'LVL_C': {
                'ITIN_MAI':  1.7,
                'ITIN_INV':  1.8,
                'ITIN_PROF': 1.6,
                'ITIN_ROT':  1.5,
                'DEFAULT':   1.6
            }
        }

        lvl_data     = matrix.get(self.pedagogical_level, {'DEFAULT': 1.0})
        rigor_factor = lvl_data.get(self.itinerary_id, lvl_data.get('DEFAULT', 1.0))

        # Penalty threshold: zero tolerance at LVL_C or ITIN_MAI/INV
        # Umbral de penalización: tolerancia cero en LVL_C o ITIN_MAI/INV
        penalty_threshold = 0.0 if (
            self.pedagogical_level == 'LVL_C' or
            self.itinerary_id in ('ITIN_MAI', 'ITIN_INV')
        ) else 0.5

        return {
            'rigor_factor':       float(rigor_factor),
            'penalty_threshold':  float(penalty_threshold)
        }

    def apply_rigor_adjustment(self, raw_score: Decimal) -> Decimal:
        """
        Applies the rigor_factor to the raw score and caps the result at 1.0.
        Must be called by GradingOrchestrator after grade_item.
        ---
        Aplica el rigor_factor a la nota bruta y limita el resultado a 1.0.
        Debe ser llamado por GradingOrchestrator tras grade_item.
        Ref: V06DOC_LEVELS Sección 3 (Ajuste de Rigor).
        """
        factor        = Decimal(str(self.rigor_params.get('rigor_factor', 1.0)))
        adjusted      = Decimal(str(raw_score)) * factor
        return min(adjusted, Decimal('1.0'))

    # ==========================================================================
    # SHARED GENERATION INFRASTRUCTURE
    # INFRAESTRUCTURA DE GENERACIÓN COMPARTIDA
    # Ref: V06DOC_STRUCTURE (Sección 2 — Skeleton-First Protocol)
    # ==========================================================================

    def get_output_schema(self):
        """
        Returns the Pydantic schema used for AI structured output validation.
        Centralized to avoid divergence between strategies.
        ---
        Devuelve el esquema Pydantic usado para la validación de salida estructurada de la IA.
        Centralizado para evitar divergencias entre estrategias.
        Ref: V06DOC_STRUCTURE (SCHEMA-FIRST Protocol).
        """
        from core.services.gemini_schemas import ExamSectionSchema
        return ExamSectionSchema

    def get_immersion_mode(self) -> str:
        """
        Default immersion mode for non-language archetypes: VEHICULAR.
        Overridden by LanguagesStrategy with MCER-based heuristics.
        ---
        Modo de inmersión por defecto para arquetipos no lingüísticos: VEHICULAR.
        Sobrescrito por LanguagesStrategy con heurísticas basadas en el MCER.
        """
        return 'VEHICULAR'

    def record_engine_usage(self, user, exam, model_name, input_tokens, output_tokens, op_type='EXAM_GEN'):
        """
        Wrapper for TrackingService to register AI consumption per exam.
        ---
        Wrapper de TrackingService para registrar el consumo de IA por examen.
        """
        TrackingService.record_usage(
            user           = user,
            exam           = exam,
            model_name     = model_name,
            input_tokens   = input_tokens,
            output_tokens  = output_tokens,
            operation_type = op_type
        )

    def generate_contract_skeleton(self, exam_uuid, archetype_id, sub_archetype_id) -> dict:
        """
        Generates the complete JSON skeleton of the Exam Contract header.
        Used by generate_exam_task to initialize the exam metadata block.
        ---
        Genera el esqueleto JSON completo de la cabecera del Contrato de Examen.
        Usado por generate_exam_task para inicializar el bloque de metadatos del examen.
        Ref: V06DOC_TEMPLATES (Sección 1 — EXAM_HEADER).
        """
        return {
            'exam_header': {
                'exam_id':           str(exam_uuid),
                'archetype_id':      archetype_id,
                'sub_archetype_id':  sub_archetype_id,
                'itinerary_id':      self.itinerary_id,
                'pedagogical_level': self.pedagogical_level,
                'grading_params':    self.rigor_params
            },
            'subdivision_sequence': [],
            'student_submission':   {},
            'grading_report':       {}
        }
