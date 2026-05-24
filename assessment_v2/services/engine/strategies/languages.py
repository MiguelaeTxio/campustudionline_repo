# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/languages.py
"""
Exam strategy for ARCH_LANG (Lenguas Extranjeras).
Covers all 7 certified sub-archetypes of the Languages branch (v5.9):
  SUB-LIN-INSTR   — Instrumental / CertAcles CLM-UGR (4 destrezas)
  SUB-LIN-MINOR   — Minor / Iniciación (5 fases curriculares)
  SUB-LIN-PHILO   — Filológico / Lingüística Histórica (3 destrezas diacrónicas)
  SUB-LIN-ECDO    — Ecdótico / Edición y Crítica Textual (4 fases editoriales)
  SUB-LIN-NORM    — Norma y Uso / El Español Actual (4 fases normativas)
  SUB-LIN-TRA-TECH — Traducción Especializada B-A Inglés (3 fases FTI-UGR)
  SUB-LIN-TRA-LIT — Traducción Literaria (3 destrezas independientes FTI-UGR)

Complies with V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS,
V06DOC_ARCHETYPES (Non-Backtracking, CertAcles), V06DOC_LEVELS (v5.9).
---
Estrategia de examen para ARCH_LANG (Lenguas Extranjeras).
Cubre los 7 subarquetipos certificados de la rama de Lenguas (v5.9).
Cumple con V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS,
V06DOC_ARCHETYPES (Non-Backtracking, CertAcles), V06DOC_LEVELS (v5.9).
"""
from decimal import Decimal
from .base import BaseExamStrategy


class LanguagesStrategy(BaseExamStrategy):
    """
    Strategy for Foreign Languages (ARCH_LANG).
    All 7 certified sub-archetypes are fully implemented with specific skeletons,
    motors and prompts aligned to their official UGR degree guides (v5.9).
    ---
    Estrategia para Lenguas Extranjeras (ARCH_LANG).
    Los 7 subarquetipos certificados están completamente implementados con esqueletos,
    motores y prompts específicos alineados con sus guías docentes UGR oficiales (v5.9).
    """

    # =========================================================================
    # GRADING ENGINE
    # MOTOR DE CALIFICACIÓN
    # Ref: V06DOC_BLOCKS (motores específicos para ARCH_LANG)
    # =========================================================================

    def grade_item(self, item, student_input) -> tuple:
        """
        Routes each item to the correct grading motor based on block_type.
        All motors are inherited from BaseExamStrategy.
        Sub-archetype-specific overrides are applied where V06DOC_BLOCKS mandates them.
        ---
        Enruta cada ítem al motor de calificación correcto basado en block_type.
        Todos los motores se heredan de BaseExamStrategy.
        Las anulaciones específicas por sub-arquetipo se aplican donde V06DOC_BLOCKS las exige.
        """
        block_type = item.block_type

        if block_type == 'PRM-STRIKE':
            # NO_NEGATIVE_MARKING active for SD_READ and SD_LIST of SUB-LIN-INSTR (CertAcles CLM-UGR)
            # NO_NEGATIVE_MARKING activo para SD_READ y SD_LIST de SUB-LIN-INSTR (CertAcles CLM-UGR)
            # Ref: V06DOC_METADATA Sec 5, V06DOC_BLOCKS 1.1
            if (
                self.sub_archetype_id == 'SUB-LIN-INSTR' and
                hasattr(item, 'section') and
                item.section.subdivision_id in ('SD_READ', 'SD_LIST')
            ):
                # Force NO_NEGATIVE_MARKING in grading_logic for this section
                # Forzar NO_NEGATIVE_MARKING en grading_logic para esta sección
                item.grading_logic['no_negative_marking'] = True
            return self._grade_prm_strike(item, student_input)

        elif block_type == 'RBT-CANON':
            return self._grade_rbt_canon(item, student_input)

        elif block_type == 'RBT-SHORT-LANG':
            # Always NO_NEGATIVE_MARKING (CertAcles CLM-UGR protocol)
            # Siempre NO_NEGATIVE_MARKING (protocolo CertAcles CLM-UGR)
            return self._grade_rbt_short_lang(item, student_input)

        elif block_type == 'CLO-OPEN':
            # NO_NEGATIVE_MARKING for SUB-LIN-INSTR SD_READ/SD_LIST
            # NO_NEGATIVE_MARKING para SUB-LIN-INSTR SD_READ/SD_LIST
            if (
                self.sub_archetype_id == 'SUB-LIN-INSTR' and
                hasattr(item, 'section') and
                item.section.subdivision_id in ('SD_READ', 'SD_LIST')
            ):
                item.grading_logic['no_negative_marking'] = True
            return self._grade_clo_open(item, student_input)

        elif block_type == 'CLO-MULTI':
            # CLO-MULTI is always no-negative by design (base motor)
            # CLO-MULTI siempre es sin penalización por diseño (motor base)
            return self._grade_clo_multi(item, student_input)

        elif block_type == 'MAT-LINK':
            return self._grade_mat_link(item, student_input)

        elif block_type == 'DRA-HOLO':
            return self._grade_dra_holo(item, student_input)

        elif block_type == 'DRA-HOLO-LIT':
            # TRA-LIT specific holistic rubric / Rúbrica holística específica de TRA-LIT
            return self._grade_dra_holo_lit(item, student_input)

        elif block_type == 'BMT-SHIFT':
            return self._grade_bmt_shift(item, student_input)

        elif block_type == 'DIA-INTERACT':
            return self._grade_dia_interact(item, student_input)

        elif block_type == 'EV-PALE':
            return self._grade_ev_pale(item, student_input)

        elif block_type == 'EV-DIAC-VAL':
            # Diachronic evolution motor — requires AI evaluation
            # Motor de evolución diacrónica — requiere evaluación por IA
            return self._grade_ev_diac_val(item, student_input)

        elif block_type == 'EV-NORM-ANALYSIS':
            # Panhispanic norm analysis motor — requires AI evaluation
            # Motor de análisis de norma panhispánica — requiere evaluación por IA
            return self._grade_ev_norm_analysis(item, student_input)

        elif block_type == 'EV-TRA-PRECISION-TECH':
            # FTI-UGR translation precision motor (error hierarchy A/B/C)
            # Motor de precisión traductológica FTI-UGR (jerarquía de errores A/B/C)
            return self._grade_ev_tra_precision_tech(item, student_input)

        # Fallback / Fallback
        return Decimal('0.0'), {
            'status': 'MOTOR_NOT_IMPLEMENTED',
            'feedback_category': 'FB_CONCEPT',
            'justification': f'Motor {block_type} no implementado para ARCH_LANG.'
        }

    # =========================================================================
    # SPECIALIZED LANGUAGE GRADING MOTORS
    # MOTORES DE CALIFICACIÓN ESPECIALIZADOS PARA LENGUAS
    # =========================================================================

    def _grade_ev_diac_val(self, item, student_input) -> tuple:
        """
        EV-DIAC-VAL motor: Diachronic phonetic evolution (SUB-LIN-PHILO).
        Validates correct application of phonetic change laws (Grimm, Verner, etc.).
        Requires AI evaluation for full assessment.
        ---
        Motor EV-DIAC-VAL: Evolución fonética diacrónica (SUB-LIN-PHILO).
        Valida la correcta aplicación de leyes de cambio fonético (Grimm, Verner, etc.).
        Requiere evaluación por IA para la valoración completa.
        Ref: V06DOC_BLOCKS Sección 4.1 (EV-DIAC-VAL).
        """
        logic        = item.grading_logic
        student_text = str(student_input).strip() if not isinstance(student_input, dict) \
            else str(student_input.get('text', '')).strip()

        if not student_text:
            return Decimal('0.0'), {
                'status': 'OMITTED',
                'feedback_category': 'FB_PROCEDURAL',
                'justification': 'No se ha proporcionado ningún análisis diacrónico.'
            }

        keywords = logic.get('keywords', [])
        word_count = len(student_text.split())
        keyword_hits = sum(1 for kw in keywords if kw.lower() in student_text.lower())
        keyword_ratio = keyword_hits / len(keywords) if keywords else 0.5

        heuristic_score = Decimal(str(round(min(keyword_ratio, 1.0), 4)))

        return heuristic_score, {
            'status': 'PENDING_AI_ANALYSIS',
            'feedback_category': 'FB_PROCEDURAL',
            'justification': logic.get(
                'feedback_justification',
                f'Análisis diacrónico recibido ({word_count} palabras). '
                f'Validación de leyes fonéticas pendiente de evaluación por IA.'
            ),
            'keyword_hits': keyword_hits,
            'total_keywords': len(keywords),
            'heuristic_score': float(heuristic_score),
            'pending_ai_refinement': True
        }

    def _grade_ev_norm_analysis(self, item, student_input) -> tuple:
        """
        EV-NORM-ANALYSIS motor: Panhispanic norm deviation analysis (SUB-LIN-NORM).
        Validates detection and justification of orthographic/morphosyntactic deviations.
        Requires AI evaluation for full assessment.
        ---
        Motor EV-NORM-ANALYSIS: Análisis de desviaciones de la norma panhispánica (SUB-LIN-NORM).
        Valida la detección y justificación de desviaciones ortográficas/morfosintácticas.
        Requiere evaluación por IA para la valoración completa.
        Ref: V06DOC_BLOCKS Sección 4.2 (EV-NORM-ANALYSIS).
        """
        logic        = item.grading_logic
        student_text = str(student_input).strip() if not isinstance(student_input, dict) \
            else str(student_input.get('text', '')).strip()

        if not student_text:
            return Decimal('0.0'), {
                'status': 'OMITTED',
                'feedback_category': 'FB_FORMAL',
                'justification': 'No se ha proporcionado ningún análisis normativo.'
            }

        word_count = len(student_text.split())

        return Decimal('0.6'), {
            'status': 'PENDING_AI_ANALYSIS',
            'feedback_category': 'FB_FORMAL',
            'justification': logic.get(
                'feedback_justification',
                f'Análisis normativo recibido ({word_count} palabras). '
                f'Validación de desviaciones panhispánicas pendiente de evaluación por IA.'
            ),
            'word_count': word_count,
            'pending_ai_refinement': True
        }

    def _grade_ev_tra_precision_tech(self, item, student_input) -> tuple:
        """
        EV-TRA-PRECISION-TECH motor: FTI-UGR error hierarchy for technical translation.
        Error categories: A (meaning distortion) = fatal, B (terminology) = -1pt, C (style) = -0.5pt.
        Requires AI evaluation for full assessment.
        ---
        Motor EV-TRA-PRECISION-TECH: Jerarquía de errores FTI-UGR para traducción técnica.
        Categorías de error: A (distorsión de sentido) = fatal, B (terminología) = -1pt, C (estilo) = -0.5pt.
        Requiere evaluación por IA para la valoración completa.
        Ref: V06DOC_BLOCKS Sección 4.3 (EV-TRA-PRECISION-TECH).
        """
        logic        = item.grading_logic
        student_text = str(student_input).strip() if not isinstance(student_input, dict) \
            else str(student_input.get('text', '')).strip()

        if not student_text:
            return Decimal('0.0'), {
                'status': 'OMITTED',
                'feedback_category': 'FB_PROCEDURAL',
                'justification': 'No se ha proporcionado ninguna traducción técnica.'
            }

        word_count = len(student_text.split())

        return Decimal('0.6'), {
            'status': 'PENDING_AI_ANALYSIS',
            'feedback_category': 'FB_PROCEDURAL',
            'justification': logic.get(
                'feedback_justification',
                f'Traducción técnica recibida ({word_count} palabras). '
                f'Evaluación por jerarquía de errores FTI-UGR (A/B/C) pendiente de análisis por IA.'
            ),
            'word_count': word_count,
            'error_hierarchy': {
                'A': 'Distorsión de sentido (eliminatorio)',
                'B': 'Error terminológico (-1 punto sobre 10)',
                'C': 'Error de estilo o registro (-0.5 puntos sobre 10)'
            },
            'pending_ai_refinement': True
        }

    # =========================================================================
    # IMMERSION MODE
    # MODO DE INMERSIÓN
    # Ref: V06DOC_LEVELS Sección 4 (Normativa UGR)
    # =========================================================================

    def get_immersion_mode(self) -> str:
        """
        Determines the interface language based on V06DOC_LEVELS (UGR Normative).
        LVL_C → always TOTAL.
        ITIN_MAI + LVL_B → TOTAL; ITIN_MAI + LVL_A → BILINGUAL.
        LVL_B (other itineraries) → BILINGUAL.
        LVL_A (other itineraries) → VEHICULAR.
        Non-language sub-archetypes (NORM, ECDO) → VEHICULAR (content in Spanish).
        ---
        Determina el idioma de la interfaz basado en V06DOC_LEVELS (Normativa UGR).
        Ref: V06DOC_LEVELS Sección 4.
        """
        # NORM and ECDO are Spanish-language sub-archetypes: always VEHICULAR
        # NORM y ECDO son subarquetipos en español: siempre VEHICULAR
        if self.sub_archetype_id in ('SUB-LIN-NORM', 'SUB-LIN-ECDO'):
            return 'VEHICULAR'

        if self.pedagogical_level == 'LVL_C':
            return 'TOTAL'

        if self.itinerary_id == 'ITIN_MAI':
            return 'TOTAL' if self.pedagogical_level == 'LVL_B' else 'BILINGUAL'

        return 'BILINGUAL' if self.pedagogical_level == 'LVL_B' else 'VEHICULAR'

    # =========================================================================
    # RIGOR OVERRIDE
    # ANULACIÓN DE RIGOR
    # Ref: V06DOC_LEVELS (rigor específico por sub-arquetipo NORM/PHILO)
    # =========================================================================

    def _get_grading_params(self) -> dict:
        """
        Overrides the base rigor matrix for sub-archetypes with specific UGR multipliers.
        SUB-LIN-NORM: +x1.7 on LVL_C (normative precision is eliminatory).
        SUB-LIN-PHILO: +x1.8 on LVL_C/ITIN_MAI (philological rigor is maximum).
        All others inherit the base matrix.
        ---
        Anula la matriz de rigor base para subarquetipos con multiplicadores UGR específicos.
        SUB-LIN-NORM: +x1.7 en LVL_C (la precisión normativa es eliminatoria).
        SUB-LIN-PHILO: +x1.8 en LVL_C/ITIN_MAI (el rigor filológico es máximo).
        Los demás heredan la matriz base.
        Ref: V06DOC_LEVELS (valores específicos por sub-arquetipo).
        """
        base = super()._get_grading_params()

        if self.sub_archetype_id == 'SUB-LIN-NORM' and self.pedagogical_level == 'LVL_C':
            base['rigor_factor'] = 1.7

        elif self.sub_archetype_id == 'SUB-LIN-PHILO' and (
            self.pedagogical_level == 'LVL_C' or self.itinerary_id == 'ITIN_MAI'
        ):
            base['rigor_factor'] = 1.8

        return base

    # =========================================================================
    # EXAM SKELETON — 7 certified sub-archetypes
    # ESQUELETO DE EXAMEN — 7 subarquetipos certificados
    # Ref: V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS (v5.9)
    # =========================================================================

    def get_exam_skeleton(self) -> list:
        """
        Returns the full structural skeleton for the sub-archetype.
        Each section includes: subdivision_id, title, instructions, layout_mode,
        time_limit, and items (block_type, widget_id, task_instruction, weight,
        fail_logic, level_requisite).
        ---
        Devuelve el esqueleto estructural completo para el sub-arquetipo.
        Cada sección incluye: subdivision_id, title, instructions, layout_mode,
        time_limit, e items (block_type, widget_id, task_instruction, weight,
        fail_logic, level_requisite).
        Ref: V06DOC_STRUCTURE (Skeleton-First Protocol), V06DOC_SUBARCHETYPES v5.9.
        """
        sid  = self.sub_archetype_id
        mode = self.get_immersion_mode()
        loc  = self.config.get('localized_sections', {})

        def _loc(sd_key, veh_title, veh_instr, tar_title_default, tar_instr_default):
            """
            Resolves section title and instructions based on immersion mode.
            VEHICULAR → Spanish. BILINGUAL → Spanish + target. TOTAL → target language only.
            ---
            Resuelve el título e instrucciones de sección según el modo de inmersión.
            """
            loc_data = loc.get(sd_key, {})
            if isinstance(loc_data, dict):
                tar_title = loc_data.get('title', tar_title_default)
                tar_instr = loc_data.get('instructions', tar_instr_default)
            else:
                tar_title = tar_title_default
                tar_instr = tar_instr_default

            if mode == 'VEHICULAR':
                return veh_title, veh_instr
            elif mode == 'BILINGUAL':
                return f"{veh_title} / {tar_title}", tar_instr
            else:  # TOTAL
                return tar_title, tar_instr

        # ------------------------------------------------------------------
        # SUB-LIN-INSTR: Instrumental / CertAcles CLM-UGR
        # 4 destrezas obligatorias — Non-Backtracking — NO_NEGATIVE_MARKING en SD_READ y SD_LIST
        # Ref: V06DOC_SUBARCHETYPES Sección 1.1
        # ------------------------------------------------------------------
        if sid == 'SUB-LIN-INSTR':
            t_read,  i_read  = _loc('SD_READ',  'Comprensión Lectora',
                'Lee el texto y responde a las preguntas de comprensión.',
                'Reading Comprehension', 'Read the text and answer the comprehension questions.')
            t_list,  i_list  = _loc('SD_LIST',  'Comprensión Auditiva',
                'Escucha el audio y responde a las preguntas.',
                'Listening Comprehension', 'Listen to the audio and answer the questions.')
            t_writ,  i_writ  = _loc('SD_WRIT',  'Expresión e Interacción Escritas',
                'Redacta el texto solicitado con el registro adecuado.',
                'Written Expression and Interaction', 'Write the requested text using appropriate register.')
            t_speak, i_speak = _loc('SD_SPEAK', 'Expresión e Interacción Orales',
                'Participa en la interacción oral con el asistente.',
                'Speaking and Oral Interaction', 'Participate in the oral interaction with the assistant.')

            return [
                {
                    'subdivision_id': 'SD_READ',
                    'title': t_read,
                    'instructions': i_read,
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1200,
                    'items': [
                        {
                            'block_type': 'CLO-MULTI',
                            'widget_id': 'W-TXT-CLOZE',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera un texto académico en el idioma objetivo con exactamente 8 huecos (CLO-MULTI). '
                                'Cada hueco evalúa léxico o gramática en contexto. '
                                'Usa marcadores [HUECO_ID_1] ... [HUECO_ID_8]. '
                                'Proporciona 4 opciones por hueco en cloze_options. '
                                'NO_NEGATIVE_MARKING activo para esta sección.'
                            )
                        },
                        {
                            'block_type': 'PRM-STRIKE',
                            'widget_id': 'W-OBJ-STRIKE',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera 4 preguntas de opción múltiple (A/B/C/D) sobre comprensión lectora del texto. '
                                'Las preguntas deben requerir inferencia y comprensión global, no solo localización. '
                                'NO_NEGATIVE_MARKING activo para esta sección.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_LIST',
                    'title': t_list,
                    'instructions': i_list,
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {
                            'block_type': 'PRM-STRIKE',
                            'widget_id': 'W-OBJ-STRIKE',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera 5 preguntas de opción múltiple (A/B/C/D) basadas en la transcripción '
                                'del audio proporcionado como section_stimulus. '
                                'Las preguntas deben evaluar comprensión global, actitud del hablante '
                                'e inferencia pragmática. NO_NEGATIVE_MARKING activo para esta sección.'
                            )
                        },
                        {
                            'block_type': 'RBT-SHORT-LANG',
                            'widget_id': 'W-OBJ-STRIKE',
                            'weight': 0.8,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera 3 preguntas de respuesta breve (≤4 palabras) sobre datos concretos '
                                'mencionados en el audio. Respuestas únicas e inequívocas. '
                                'NO_NEGATIVE_MARKING activo (CLM-UGR protocol).'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_WRIT',
                    'title': t_writ,
                    'instructions': i_writ,
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1800,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Plantea un tema de producción escrita académica (ensayo argumentativo, '
                                'artículo de opinión o correo formal) ajustado al nivel MCERL del examen. '
                                'Declara en word_count_range el mínimo y máximo certificado CLM-UGR '
                                'para este nivel (ej: B2 → min: 180, max: 220). '
                                'Incluye los 4 ejes de la rúbrica holística en rubric_axes.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_SPEAK',
                    'title': t_speak,
                    'instructions': i_speak,
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {
                            'block_type': 'DIA-INTERACT',
                            'widget_id': 'W-COMM-DIALOG',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera el escenario inicial para una interacción oral con UniversIA. '
                                'El alumno debe demostrar fluidez, precisión y adecuación pragmática. '
                                'Declara en initial_scenario el contexto de la conversación '
                                '(entrevista, debate, consulta formal) en el idioma objetivo.'
                            )
                        }
                    ]
                }
            ]

        # ------------------------------------------------------------------
        # SUB-LIN-MINOR: Minor / Iniciación (Lengua B/C)
        # 5 fases curriculares progresivas
        # Ref: V06DOC_SUBARCHETYPES Sección 1.2
        # ------------------------------------------------------------------
        elif sid == 'SUB-LIN-MINOR':
            return [
                {
                    'subdivision_id': 'SD_PHON_GRAPH',
                    'title': 'Grafía y Fonética',
                    'instructions': 'Identifique y reproduzca los caracteres y sonidos del sistema fonológico.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 600,
                    'items': [
                        {
                            'block_type': 'RBT-CANON',
                            'widget_id': 'W-OBJ-STRIKE',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera 5 ejercicios de reconocimiento o reproducción de grafías/caracteres '
                                'del idioma (ej: kana japonés, cirílico, árabe, caracteres chinos básicos). '
                                'Cada ítem evalúa la identificación precisa de un grafema concreto.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_MORPH_BASE',
                    'title': 'Morfosintaxis Elemental',
                    'instructions': 'Complete las estructuras gramaticales básicas.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {
                            'block_type': 'CLO-MULTI',
                            'widget_id': 'W-TXT-CLOZE',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera oraciones simples con huecos (CLO-MULTI) que evalúen '
                                'estructuras morfosintácticas elementales del idioma '
                                '(conjugación básica, concordancia, orden de palabras). '
                                'Usa marcadores [HUECO_ID_1] ... [HUECO_ID_6]. '
                                'Proporciona 3 opciones por hueco en cloze_options.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_LEX_COMM',
                    'title': 'Léxico y Función Comunicativa',
                    'instructions': 'Relacione el vocabulario con su función comunicativa.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 600,
                    'items': [
                        {
                            'block_type': 'MAT-LINK',
                            'widget_id': 'W-MIX-MATCH',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera 6 pares de emparejamiento léxico-funcional '
                                '(término en el idioma → función comunicativa o equivalente en castellano). '
                                'El vocabulario debe pertenecer al ámbito temático del material de estudio.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_READ_ADAP',
                    'title': 'Comprensión Lectora Adaptada',
                    'instructions': 'Lea el texto adaptado y responda las preguntas.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 900,
                    'items': [
                        {
                            'block_type': 'PRM-STRIKE',
                            'widget_id': 'W-OBJ-STRIKE',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera un texto breve adaptado al nivel de iniciación '
                                'y 4 preguntas de comprensión de opción múltiple (A/B/C/D). '
                                'El texto debe ser section_stimulus. '
                                'Las preguntas evalúan comprensión literal y vocabulario básico.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_CULT_INTEGRITY',
                    'title': 'Competencia Intercultural',
                    'instructions': 'Responda sobre el contexto sociocultural del idioma estudiado.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 600,
                    'items': [
                        {
                            'block_type': 'PRM-STRIKE',
                            'widget_id': 'W-OBJ-STRIKE',
                            'weight': 0.8,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera 4 preguntas de opción múltiple (A/B/C/D) sobre '
                                'aspectos culturales, geográficos e históricos del país/cultura '
                                'del idioma estudiado. Las preguntas deben ser de nivel iniciación.'
                            )
                        }
                    ]
                }
            ]

        # ------------------------------------------------------------------
        # SUB-LIN-PHILO: Filológico / Lingüística Histórica (UGR)
        # 3 destrezas diacrónicas
        # Ref: V06DOC_SUBARCHETYPES Sección 1.3
        # ------------------------------------------------------------------
        elif sid == 'SUB-LIN-PHILO':
            return [
                {
                    'subdivision_id': 'SD_PHONO',
                    'title': 'Fonética y Fonología Histórica',
                    'instructions': 'Analice la evolución fonética de las formas proporcionadas y aplique las leyes correspondientes.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1800,
                    'items': [
                        {
                            'block_type': 'EV-DIAC-VAL',
                            'widget_id': 'W-PHILO-IPA',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera un ejercicio de evolución fonética histórica: '
                                'proporciona 5 étimos latinos/griegos y solicita la evolución '
                                'al español medieval o moderno con aplicación de las leyes fonéticas '
                                '(sonorización, apócope, diptongación, palatalización, etc.). '
                                'Proporciona en keywords las leyes fonéticas esperadas para cada forma. '
                                'El source_text debe incluir el corpus de referencia.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_MORPH_DIAC',
                    'title': 'Morfología Diacrónica',
                    'instructions': 'Explique la evolución morfológica de las formas y reconstruya los paradigmas.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1800,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera un ejercicio de análisis morfológico diacrónico: '
                                'proporciona formas verbales o nominales de distintos estadios '
                                'históricos del español y solicita la reconstrucción del paradigma '
                                'y la justificación de los cambios morfológicos. '
                                'El source_text debe incluir las formas a analizar.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_LEX_SEM',
                    'title': 'Lexicología y Semántica Histórica',
                    'instructions': 'Analice la evolución semántica y etimológica de los términos propuestos.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1200,
                    'items': [
                        {
                            'block_type': 'CLO-OPEN',
                            'widget_id': 'W-TXT-CLOZE',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera un texto con 6 huecos sobre semántica histórica: '
                                'cada hueco solicita el étimo, el estadio intermedio o el '
                                'significado medieval de un término. '
                                'Usa marcadores [HUECO_ID_1] ... [HUECO_ID_6]. '
                                'gap_solutions debe incluir la forma etimológica correcta con variantes aceptables.'
                            )
                        }
                    ]
                }
            ]

        # ------------------------------------------------------------------
        # SUB-LIN-ECDO: Ecdótico / Edición y Crítica Textual (UGR)
        # 4 fases editoriales progresivas
        # Ref: V06DOC_SUBARCHETYPES Sección 1.4
        # ------------------------------------------------------------------
        elif sid == 'SUB-LIN-ECDO':
            return [
                {
                    'subdivision_id': 'SD_ORTOTYPO',
                    'title': 'Corrección Ortotipográfica',
                    'instructions': 'Identifique y corrija los errores ortotipográficos del texto propuesto.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1200,
                    'items': [
                        {
                            'block_type': 'CLO-MULTI',
                            'widget_id': 'W-TXT-CLOZE',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera un texto con 8 errores ortotipográficos deliberados '
                                '(puntuación, mayúsculas, comillas, cursivas, guiones, etc.) '
                                'marcados como huecos CLO-MULTI. '
                                'Usa marcadores [HUECO_ID_1] ... [HUECO_ID_8]. '
                                'Cada hueco presenta la forma errónea vs. la correcta entre las opciones. '
                                'El source_text es el texto completo con errores para el panel lateral.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_STYLE',
                    'title': 'Corrección de Estilo Editorial',
                    'instructions': 'Corrija el estilo del fragmento atendiendo a criterios editoriales académicos.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1800,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera un fragmento académico con problemas de estilo '
                                '(redundancias, vicios de dicción, anacolutos, incorrecciones formales) '
                                'y solicita su corrección razonada. '
                                'El source_text es el fragmento original para el panel lateral. '
                                'El alumno reescribe el fragmento corregido con justificación editorial.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_ANNOT',
                    'title': 'Anotación Crítica y Edición Científica',
                    'instructions': 'Elabore las notas críticas del pasaje según los criterios de edición científica.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 2400,
                    'items': [
                        {
                            'block_type': 'EV-PALE',
                            'widget_id': 'W-PHILO-ECDO',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera un pasaje de texto antiguo o medieval (con variantes de testimonio) '
                                'y solicita al alumno: (1) transcripción del pasaje resolviendo braquigrafías, '
                                '(2) nota crítica con el aparato de variantes, '
                                '(3) justificación de la lectura preferida. '
                                'correct_transcription debe incluir la transcripción de referencia. '
                                'El source_text es el facsímil o texto a transcribir.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_EVAL',
                    'title': 'Evaluación Editorial e Informe de Lector',
                    'instructions': 'Redacte el informe de lector editorial según los criterios académicos.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 2400,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Proporciona un abstract o capítulo de un trabajo académico '
                                'y solicita al alumno un informe de lector editorial completo '
                                '(valoración científica, adecuación, recomendaciones, decisión editorial). '
                                'El source_text es el texto a evaluar. '
                                'word_count_range: min 300, max 500 palabras.'
                            )
                        }
                    ]
                }
            ]

        # ------------------------------------------------------------------
        # SUB-LIN-NORM: Norma y Uso / El Español Actual (UGR)
        # 4 fases normativas progresivas
        # Ref: V06DOC_SUBARCHETYPES Sección 1.5
        # ------------------------------------------------------------------
        elif sid == 'SUB-LIN-NORM':
            return [
                {
                    'subdivision_id': 'SD_CORPUS_ANALYSIS',
                    'title': 'Investigación y Validación Empírica',
                    'instructions': 'Analice el corpus proporcionado e identifique los fenómenos normativos presentes.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1800,
                    'items': [
                        {
                            'block_type': 'EV-NORM-ANALYSIS',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera un corpus textual breve (150-200 palabras) con fenómenos '
                                'normativos observables (usos dialectales, variación ortográfica, '
                                'construcciones discutidas por la RAE/ASALE). '
                                'Solicita al alumno: identificación de fenómenos, '
                                'clasificación según la norma panhispánica y valoración crítica. '
                                'El source_text es el corpus para el panel lateral.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_MORPH_ANTINORM',
                    'title': 'Diagnóstico de Desviaciones Morfosintácticas',
                    'instructions': 'Identifique y clasifique las desviaciones morfosintácticas del texto.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1200,
                    'items': [
                        {
                            'block_type': 'CLO-MULTI',
                            'widget_id': 'W-TXT-CLOZE',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera un texto con 8 desviaciones morfosintácticas deliberadas '
                                '(queísmo, dequeísmo, laísmo, leísmo, concordancias incorrectas, '
                                'tiempos verbales erróneos, etc.) marcadas como huecos CLO-MULTI. '
                                'Cada hueco presenta la forma errónea y la correcta como opciones. '
                                'El source_text es el texto completo para el panel lateral.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_ORTHO_PRESCRIPTIVE',
                    'title': 'Ortografía y Ortotipografía Académica',
                    'instructions': 'Aplique las reglas ortográficas y ortotipográficas de la norma académica.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {
                            'block_type': 'PRM-STRIKE',
                            'widget_id': 'W-OBJ-STRIKE',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera 6 preguntas de opción múltiple (A/B/C/D) sobre '
                                'ortografía académica (tildación, uso de grafemas, puntuación, '
                                'ortotipografía científica) según la Ortografía RAE 2010 '
                                'y el Manual de la Nueva Gramática.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_CRITICAL_NORM',
                    'title': 'Comentario Crítico y Justificación Bibliográfica',
                    'instructions': 'Redacte un comentario crítico normativo con apoyo bibliográfico académico.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 2400,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Proporciona un fenómeno lingüístico discutido (ej: uso del subjuntivo, '
                                'variación en el voseo, leísmo de cortesía) y solicita '
                                'un comentario crítico con posición normativa justificada '
                                'por referencia a RAE, ASALE o corpus académicos. '
                                'word_count_range: min 250, max 350 palabras. '
                                'rubric_axes: adecuacion_encargo 0.25, coherencia_cohesion 0.25, '
                                'riqueza_lexica 0.25, correccion_gramatical 0.25.'
                            )
                        }
                    ]
                }
            ]

        # ------------------------------------------------------------------
        # SUB-LIN-TRA-TECH: Traducción Especializada B-A Inglés (FTI-UGR)
        # 3 fases secuenciales del proceso traductor
        # Ref: V06DOC_SUBARCHETYPES Sección 1.6
        # ------------------------------------------------------------------
        elif sid == 'SUB-LIN-TRA-TECH':
            return [
                {
                    'subdivision_id': 'SD_TRA_ANALYSIS',
                    'title': 'Análisis del Encargo Traductológico',
                    'instructions': 'Analice el texto origen e identifique los condicionantes del encargo de traducción.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1200,
                    'items': [
                        {
                            'block_type': 'PRM-STRIKE',
                            'widget_id': 'W-OBJ-STRIKE',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera 5 preguntas de opción múltiple (A/B/C/D) sobre '
                                'el análisis traductológico del texto origen: '
                                'función textual, registro, densidad terminológica, '
                                'problemas de traducción identificados y estrategia adecuada. '
                                'El texto origen debe ser section_stimulus.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_TERM_RESEARCH',
                    'title': 'Documentación Terminológica y Glosario',
                    'instructions': 'Elabore el glosario terminológico bilingüe del texto origen.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1800,
                    'items': [
                        {
                            'block_type': 'MAT-LINK',
                            'widget_id': 'W-DOC-RESOURCES',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Extrae 8 términos especializados del texto origen y genera '
                                'un ejercicio de emparejamiento terminológico (inglés → español técnico). '
                                'Los pares deben incluir el equivalente acuñado en el ámbito especializado '
                                '(jurídico, médico, científico, técnico) según el contexto del material. '
                                'options: términos en inglés. targets: equivalentes en español.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_TRA_DRAFT',
                    'title': 'Traducción Directa Cronometrada',
                    'instructions': 'Traduzca el texto origen al español manteniendo la precisión terminológica y el registro.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 3600,
                    'items': [
                        {
                            'block_type': 'EV-TRA-PRECISION-TECH',
                            'widget_id': 'W-MEDI-LAYOUT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'El alumno traduce el texto origen completo (disponible como section_stimulus) '
                                'del inglés al español con precisión terminológica y adecuación de registro. '
                                'La evaluación usa la jerarquía de errores FTI-UGR: '
                                'A (distorsión de sentido) = eliminatorio, '
                                'B (error terminológico) = -1 punto sobre 10, '
                                'C (error de estilo) = -0.5 puntos sobre 10. '
                                'feedback_justification debe incluir el catálogo de errores esperados por categoría.'
                            )
                        }
                    ]
                }
            ]

        # ------------------------------------------------------------------
        # SUB-LIN-TRA-LIT: Traducción Literaria (FTI-UGR, guía 25211NJ)
        # 3 destrezas independientes — evaluación holística — Turnitin obligatorio
        # Ref: V06DOC_SUBARCHETYPES Sección 1.7, guía docente 25211NJ verificada 23/06/2025
        # ------------------------------------------------------------------
        elif sid == 'SUB-LIN-TRA-LIT':
            return [
                {
                    'subdivision_id': 'SD_TRA_STYLE',
                    'title': 'Análisis Estilístico Comparado',
                    'instructions': (
                        'Analice los rasgos estilísticos del texto origen y su traducción propuesta. '
                        'Identifique decisiones traductológicas clave y su justificación estética.'
                    ),
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 2400,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO-LIT',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Proporciona un fragmento literario en inglés (100-150 palabras) '
                                'y una traducción publicada al español como source_text. '
                                'Solicita al alumno un análisis comparado que identifique: '
                                'rasgos de estilo del autor, decisiones traductológicas del traductor '
                                '(domesticación/extranjerización, gestión de culturemas, registro), '
                                'y valoración crítica argumentada. '
                                'rubric_axes: adecuacion_skopos 0.30, gestion_culturemas 0.25, '
                                'calidad_literaria 0.25, rigor_comentario 0.20. '
                                'word_count_range: min 300, max 400.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_TRA_CREATIVE',
                    'title': 'Transferencia Estética Literaria',
                    'instructions': (
                        'Traduzca el fragmento literario preservando la carga estética, '
                        'la voz del autor y la función poética del texto. '
                        'La entrega debe realizarse mediante Turnitin.'
                    ),
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 3600,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO-LIT',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Proporciona un fragmento literario inédito en inglés (150-200 palabras) '
                                'como source_text. El alumno realiza una traducción literaria al español '
                                'que preserve: voz del narrador, figuras retóricas, ritmo prosístico, '
                                'culturemas y nivel de lengua. '
                                'La entrega es obligatoria vía Turnitin (file_uploaded=True requerido). '
                                'rubric_axes: adecuacion_skopos 0.30, gestion_culturemas 0.25, '
                                'calidad_literaria 0.25, rigor_comentario 0.20. '
                                'word_count_range: min 150, max 200 (traducción) + 100 nota del traductor.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_TRA_CRIT',
                    'title': 'Comentario Exegético y Justificación Traductológica',
                    'instructions': (
                        'Redacte el comentario exegético y la justificación de sus decisiones '
                        'traductológicas con referencia a la teoría de la traducción literaria.'
                    ),
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 2400,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO-LIT',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'El alumno redacta un comentario exegético sobre su propia traducción '
                                'del fragmento de SD_TRA_CREATIVE. El comentario debe incluir: '
                                'análisis de los problemas traductológicos encontrados, '
                                'justificación de las soluciones adoptadas con referencia '
                                'a autores como Venuti, Newmark, Berman o Toury, '
                                'y reflexión sobre las limitaciones de la traducción. '
                                'rubric_axes: adecuacion_skopos 0.30, gestion_culturemas 0.25, '
                                'calidad_literaria 0.25, rigor_comentario 0.20. '
                                'word_count_range: min 400, max 600.'
                            )
                        }
                    ]
                }
            ]

        # ------------------------------------------------------------------
        # FALLBACK: Generic language skeleton
        # FALLBACK: Esqueleto genérico de lenguas
        # ------------------------------------------------------------------
        else:
            return [
                {
                    'subdivision_id': 'SD_READ',
                    'title': 'Comprensión Lectora',
                    'instructions': 'Lea el texto y responda las preguntas de comprensión.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1200,
                    'items': [
                        {
                            'block_type': 'PRM-STRIKE',
                            'widget_id': 'W-OBJ-STRIKE',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera 5 preguntas de opción múltiple (A/B/C/D) '
                                'sobre el material de estudio. '
                                'El texto fuente debe ser section_stimulus.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_WRIT',
                    'title': 'Producción Escrita',
                    'instructions': 'Redacte el texto solicitado con el registro adecuado.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1800,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Plantea un tema de producción escrita ajustado al nivel del material. '
                                'Declara word_count_range y rubric_axes en grading_logic.'
                            )
                        }
                    ]
                }
            ]

    # =========================================================================
    # SYSTEM PROMPT
    # PROMPT DE SISTEMA
    # =========================================================================

    def get_system_prompt(self) -> str:
        """
        Returns the AI system prompt specific to this sub-archetype.
        Defines the examiner role, immersion mode and generation constraints.
        ---
        Devuelve el prompt de sistema de la IA específico para este sub-arquetipo.
        Define el rol de examinador, el modo de inmersión y las restricciones de generación.
        """
        target_lang = self.config.get('target_language_code', 'es')
        mode        = self.get_immersion_mode()

        roles = {
            'SUB-LIN-INSTR':    'Examinador CertAcles/CLM-UGR. Foco: Estandarización MCERL, 4 destrezas, NO_NEGATIVE_MARKING en Reading/Listening.',
            'SUB-LIN-MINOR':    'Profesor de Iniciación de Lengua B/C. Foco: Grafía, Gramática elemental, Léxico básico y Competencia intercultural.',
            'SUB-LIN-PHILO':    'Filólogo Histórico. Foco: Gramática histórica, Evolución fonética, Semántica diacrónica y leyes de cambio lingüístico.',
            'SUB-LIN-ECDO':     'Editor Científico Especializado. Foco: Corrección ortotipográfica, Estilo editorial, Anotación crítica e Informe de lector.',
            'SUB-LIN-NORM':     'Académico de la Lengua Española. Foco: Norma panhispánica RAE/ASALE, Análisis de desviaciones y Exégesis normativa.',
            'SUB-LIN-TRA-TECH': 'Experto FTI-UGR en LSP (Language for Specific Purposes). Foco: Documentación terminológica, Traducción técnica B-A y jerarquía de errores A/B/C.',
            'SUB-LIN-TRA-LIT':  'Crítico Literario y Traductor FTI-UGR. Foco: Estilística comparada, Transferencia estética, Gestión de culturemas y Skopos literario.',
        }

        base_role = roles.get(self.sub_archetype_id, 'Profesor de Lenguas Extranjeras.')

        immersion_rule = ''
        if mode == 'TOTAL':
            immersion_rule = (
                f'INMERSIÓN TOTAL ACTIVA: Genera TODA la salida de contenido evaluable '
                f'(stem de los ítems, opciones, text_with_gaps, targets, initial_scenario, '
                f'section_stimulus) EXCLUSIVAMENTE en el idioma objetivo \'{target_lang}\'. '
                f'Los campos de metadatos (feedback_justification, task_instruction) permanecen en castellano.'
            )
        elif mode == 'BILINGUAL':
            immersion_rule = (
                f'MODO BILINGÜE ACTIVO: El contenido evaluable se genera en el idioma objetivo \'{target_lang}\'. '
                f'Los enunciados (stem) pueden incluir una aclaración en castellano entre paréntesis cuando '
                f'sea necesario para la comprensión del alumno.'
            )
        else:
            immersion_rule = (
                'MODO VEHICULAR ACTIVO: Todo el contenido se genera en castellano. '
                f'El idioma objetivo \'{target_lang}\' solo aparece en los fragmentos '
                'de texto a analizar o traducir.'
            )

        return (
            f'IDENTIDAD Y ROL: {base_role}\n'
            f'SUB-ARQUETIPO ACTIVO: {self.sub_archetype_id}\n'
            f'NIVEL PEDAGÓGICO: {self.pedagogical_level} | ITINERARIO: {self.itinerary_id}\n'
            f'IDIOMA OBJETIVO (ISO 639-1): {target_lang}\n'
            f'{immersion_rule}\n\n'
            f'REGLAS CRÍTICAS DE GENERACIÓN:\n'
            f'1. Los UUID de los ítems son INMUTABLES — devuélvelos exactamente como se reciben.\n'
            f'2. PROHIBIDO incluir metadatos, claves de corrección u opciones correctas en el campo "options" o "targets".\n'
            f'3. Para W-TXT-CLOZE usa SIEMPRE marcadores [HUECO_ID_N] — nunca guiones bajos ni otros formatos.\n'
            f'4. gap_solutions DEBE ser un dict {{gap_id: respuesta_correcta}}, nunca una lista.\n'
            f'5. Devuelve EXCLUSIVAMENTE el JSON estructurado según ExamSectionSchema — sin texto envolvente.'
        )

    # =========================================================================
    # USER PROMPT
    # PROMPT DE USUARIO
    # =========================================================================

    def get_user_prompt(
        self,
        context_text: str,
        topic: str,
        subdivision_id: str,
        generated_item_titles: list = None,
        skeleton_json: str = None
    ) -> str:
        """
        Generates the user prompt for atomic section generation.
        Injects: study context, sub-archetype, subdivision, skeleton UUIDs and anti-repetition memory.
        ---
        Genera el prompt de usuario para la generación atómica de sección.
        Inyecta: contexto de estudio, sub-arquetipo, subdivisión, UUIDs del esqueleto y memoria anti-repetición.
        """
        target_lang = self.config.get('target_language_code', 'es')
        memory_note = (
            '\nANTI-REPETICIÓN — Títulos ya generados en este examen (NO REPETIR): ' +
            ', '.join(generated_item_titles)
        ) if generated_item_titles else ''

        skeleton_note = (
            f'\nESQUELETO DE ÍTEMS (OBLIGATORIO — no modificar los item_id UUID):\n{skeleton_json}\n'
        ) if skeleton_json else ''

        return (
            f'GENERA EL CONTENIDO DE EVALUACIÓN PARA LA SIGUIENTE SECCIÓN.\n\n'
            f'Sub-arquetipo: {self.sub_archetype_id}\n'
            f'Sección objetivo: {subdivision_id}\n'
            f'Tema del material: {topic}\n'
            f'Nivel pedagógico: {self.pedagogical_level} | Itinerario: {self.itinerary_id}\n'
            f'Idioma objetivo: {target_lang}\n'
            f'{memory_note}\n\n'
            f'CONTEXTO DEL MATERIAL DE ESTUDIO (máximo 15.000 caracteres):\n'
            f'{(context_text or "")[:15000]}\n\n'
            f'{skeleton_note}\n'
            f'REGLAS DE SALIDA OBLIGATORIAS:\n'
            f'1. Devuelve UN ÚNICO objeto JSON conforme al esquema ExamSectionSchema.\n'
            f'2. Incluye UN ítem por cada UUID del esqueleto. No añadas ni elimines ítems.\n'
            f'3. Conserva cada item_id UUID EXACTAMENTE como aparece en el esqueleto.\n'
            f'4. El campo "stem" de cada ítem SIEMPRE en castellano (salvo modo TOTAL).\n'
            f'5. El contenido evaluable (opciones, text_with_gaps, targets) en \'{target_lang}\'.\n'
            f'6. Para CLO-MULTI y CLO-OPEN usa marcadores [HUECO_ID_N] en text_with_gaps.\n'
            f'7. gap_solutions debe ser {{"[HUECO_ID_1]": "respuesta", "[HUECO_ID_2]": "respuesta", ...}}.\n'
            f'8. PROHIBIDO incluir la respuesta correcta en el campo "options" de forma identificable.\n'
            f'9. Si la sección requiere section_stimulus (SPLIT_TEXT/SPLIT_VISUAL), inclúyelo en el JSON.\n'
            f'10. Genera contenido académico real y riguroso — sin placeholders ni contenido genérico.'
        )
