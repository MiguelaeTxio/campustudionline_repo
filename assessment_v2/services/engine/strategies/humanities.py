# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/humanities.py
"""
Exam strategy for ARCH_HUM (Artes y Humanidades).
Covers all 6 certified sub-archetypes of the Humanities branch (v5.9):
  SUB-HUM-HIST     — Historiográfico (Historia UGR)
  SUB-HUM-PHIL     — Dialéctico (Filosofía UGR)
  SUB-HUM-ART-HIST — Iconográfico (Historia del Arte UGR)
  SUB-HUM-ART-CREA — Bellas Artes (Emulación Parcial Certificada)
  SUB-HUM-MUS      — Musicológico (Historia y Ciencias de la Música UGR)
  SUB-HUM-ANTH     — Antropológico (Subarquetipo Transversal)

Complies with V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS,
V06DOC_ARCHETYPES (Hermeneutic model, Non-Compensation formal errors),
V06DOC_LEVELS (v5.9).
---
Estrategia de examen para ARCH_HUM (Artes y Humanidades).
Cubre los 6 subarquetipos certificados de la rama de Humanidades (v5.9).
Cumple con V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS,
V06DOC_ARCHETYPES (modelo Hermenéutico, No-Compensación de errores formales),
V06DOC_LEVELS (v5.9).
"""
from decimal import Decimal
from .base import BaseExamStrategy


class HumanitiesStrategy(BaseExamStrategy):
    """
    Strategy for Arts and Humanities (ARCH_HUM).
    Formal errors carry a mandatory -0.2 deduction (applied by GradingOrchestrator).
    DRA-HOLO is the primary evaluation motor — AI evaluation required for full scoring.
    EV-PALE uses F1 similarity for paleographic/musical transcription.
    EV-ICON-ART is the motor for iconographic identification (ART-HIST).
    EV-MUS-ANAL is the motor for musical score analysis (HUM-MUS).
    ---
    Estrategia para Artes y Humanidades (ARCH_HUM).
    Los errores formales conllevan una deducción obligatoria de -0.2 (aplicada por GradingOrchestrator).
    DRA-HOLO es el motor de evaluación principal — se requiere evaluación por IA para la calificación completa.
    EV-PALE usa similitud F1 para transcripciones paleográficas/musicales.
    EV-ICON-ART es el motor para identificación iconográfica (ART-HIST).
    EV-MUS-ANAL es el motor para análisis en partitura (HUM-MUS).
    """

    # =========================================================================
    # GRADING ENGINE
    # MOTOR DE CALIFICACIÓN
    # Ref: V06DOC_BLOCKS (motores específicos para ARCH_HUM)
    # =========================================================================

    def grade_item(self, item, student_input) -> tuple:
        """
        Routes each item to the correct grading motor based on block_type.
        The GradingOrchestrator applies the -0.2 formal penalty on top of this result.
        ---
        Enruta cada ítem al motor de calificación correcto basado en block_type.
        El GradingOrchestrator aplica la penalización formal de -0.2 sobre este resultado.
        """
        block_type = item.block_type

        if block_type == 'DRA-HOLO':
            return self._grade_dra_holo(item, student_input)

        elif block_type == 'EV-PALE':
            return self._grade_ev_pale(item, student_input)

        elif block_type == 'EV-ICON-ART':
            return self._grade_ev_icon_art(item, student_input)

        elif block_type == 'EV-MUS-ANAL':
            return self._grade_ev_mus_anal(item, student_input)

        elif block_type == 'PRM-STRIKE':
            return self._grade_prm_strike(item, student_input)

        elif block_type == 'RBT-CANON':
            return self._grade_rbt_canon(item, student_input)

        elif block_type == 'MAT-LINK':
            return self._grade_mat_link(item, student_input)

        elif block_type == 'CLO-MULTI':
            return self._grade_clo_multi(item, student_input)

        # Fallback / Fallback
        return Decimal('0.0'), {
            'status': 'MOTOR_NOT_IMPLEMENTED',
            'feedback_category': 'FB_CONCEPT',
            'justification': f'Motor {block_type} no implementado para ARCH_HUM.'
        }

    # =========================================================================
    # SPECIALIZED HUMANITIES GRADING MOTORS
    # MOTORES DE CALIFICACIÓN ESPECIALIZADOS PARA HUMANIDADES
    # =========================================================================

    def _grade_ev_icon_art(self, item, student_input) -> tuple:
        """
        EV-ICON-ART motor: Iconographic identification + Panofsky analysis (ART-HIST).
        Phase 1: formal identification of the work (artist, period, technique).
        Phase 2: iconographic and iconological analysis.
        Full AI evaluation required — returns heuristic pending AI.
        ---
        Motor EV-ICON-ART: Identificación iconográfica + análisis Panofsky (ART-HIST).
        Fase 1: identificación formal de la obra (autor, periodo, técnica).
        Fase 2: análisis iconográfico e iconológico.
        Se requiere evaluación completa por IA — devuelve heurística pendiente de IA.
        Ref: V06DOC_BLOCKS Sección 4.4 (EV-ICON-ART).
        """
        logic = item.grading_logic

        student_text = ''
        if isinstance(student_input, dict):
            student_text = str(student_input.get('text', '')).strip()
        else:
            student_text = str(student_input).strip()

        if not student_text:
            return Decimal('0.0'), {
                'status': 'OMITTED',
                'feedback_category': 'FB_CONCEPT',
                'justification': 'No se ha proporcionado ningún análisis iconográfico.'
            }

        word_count = len(student_text.split())

        # Keyword heuristic for formal identification
        # Heurística de keywords para identificación formal
        keywords = logic.get('keywords', [])
        keyword_hits = sum(1 for kw in keywords if kw.lower() in student_text.lower())
        keyword_ratio = (keyword_hits / len(keywords)) if keywords else 0.5

        heuristic_score = Decimal(str(round(min(keyword_ratio * 0.6 + 0.3, 1.0), 4)))

        return heuristic_score, {
            'status': 'PENDING_AI_ANALYSIS',
            'feedback_category': 'FB_CONCEPT',
            'justification': logic.get(
                'feedback_justification',
                f'Análisis iconográfico recibido ({word_count} palabras). '
                f'Evaluación Panofsky (preiconográfico/iconográfico/iconológico) pendiente de IA.'
            ),
            'word_count': word_count,
            'keyword_hits': keyword_hits,
            'heuristic_score': float(heuristic_score),
            'pending_ai_refinement': True
        }

    def _grade_ev_mus_anal(self, item, student_input) -> tuple:
        """
        EV-MUS-ANAL motor: Musical score analysis — harmonic and formal (HUM-MUS).
        Evaluates: harmonic identification (chord types, functions), formal structure,
        cadences and historical period recognition.
        Full AI evaluation required — returns heuristic pending AI.
        ---
        Motor EV-MUS-ANAL: Análisis en partitura — armónico y formal (HUM-MUS).
        Evalúa: identificación armónica (tipos de acordes, funciones), estructura formal,
        cadencias y reconocimiento del período histórico.
        Se requiere evaluación completa por IA — devuelve heurística pendiente de IA.
        Ref: V06DOC_BLOCKS Sección 4.5 (EV-MUS-ANAL).
        """
        logic = item.grading_logic

        student_text = ''
        if isinstance(student_input, dict):
            student_text = str(student_input.get('text', '')).strip()
        else:
            student_text = str(student_input).strip()

        if not student_text:
            return Decimal('0.0'), {
                'status': 'OMITTED',
                'feedback_category': 'FB_CONCEPT',
                'justification': 'No se ha proporcionado ningún análisis musical.'
            }

        word_count = len(student_text.split())
        keywords   = logic.get('keywords', [])
        keyword_hits = sum(1 for kw in keywords if kw.lower() in student_text.lower())
        keyword_ratio = (keyword_hits / len(keywords)) if keywords else 0.5

        heuristic_score = Decimal(str(round(min(keyword_ratio * 0.6 + 0.3, 1.0), 4)))

        return heuristic_score, {
            'status': 'PENDING_AI_ANALYSIS',
            'feedback_category': 'FB_CONCEPT',
            'justification': logic.get(
                'feedback_justification',
                f'Análisis musical recibido ({word_count} palabras). '
                f'Evaluación armónico-formal pendiente de análisis por IA.'
            ),
            'word_count': word_count,
            'keyword_hits': keyword_hits,
            'heuristic_score': float(heuristic_score),
            'pending_ai_refinement': True
        }

    # =========================================================================
    # EXAM SKELETON — 6 certified sub-archetypes
    # ESQUELETO DE EXAMEN — 6 subarquetipos certificados
    # Ref: V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS (v5.9)
    # =========================================================================

    def get_exam_skeleton(self) -> list:
        """
        Returns the full structural skeleton for the sub-archetype.
        Each sub-archetype has its specific subdivision sequence per V06DOC_SUBDIVISIONS.
        ---
        Devuelve el esqueleto estructural completo para el sub-arquetipo.
        Cada sub-arquetipo tiene su secuencia de subdivisiones específica según V06DOC_SUBDIVISIONS.
        Ref: V06DOC_STRUCTURE (Skeleton-First Protocol), V06DOC_SUBARCHETYPES v5.9.
        """
        sid  = self.sub_archetype_id
        itin = self.itinerary_id

        # ==============================================================
        # 1. SUB-HUM-HIST — Historiográfico (Historia UGR)
        # 2 fases: desarrollo escrito + análisis de fuentes
        # Ref: V06DOC_SUBARCHETYPES Sección 2.1
        # ==============================================================
        if sid == 'SUB-HUM-HIST':
            return [
                {
                    'subdivision_id': 'SD_HIST_DEV',
                    'title': 'Desarrollo Historiográfico — Prueba Escrita',
                    'instructions': (
                        'Desarrolle el tema histórico con rigor historiográfico. '
                        'Incluya cronología, actores, contexto y consecuencias. '
                        'Cite las corrientes historiográficas pertinentes.'
                    ),
                    'layout_mode': 'STANDARD',
                    'time_limit': 3600,
                    'items': [
                        {
                            'block_type': 'PRM-STRIKE',
                            'widget_id': 'W-OBJ-STRIKE',
                            'weight': 0.8,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera 5 preguntas de opción múltiple (A/B/C/D) sobre '
                                'cronología, actores históricos, causas y consecuencias '
                                'del período o evento del material de estudio.'
                            )
                        },
                        {
                            'block_type': 'DRA-HOLO',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera un tema de desarrollo historiográfico relacionado '
                                'con el material de estudio. '
                                'El alumno debe: contextualizar el período, analizar las causas, '
                                'desarrollar el proceso histórico con sus fases y evaluar las consecuencias. '
                                'Exige cita de corrientes historiográficas (ITIN_MAI/INV). '
                                'rubric_axes: adecuacion_encargo 0.25, coherencia_cohesion 0.25, '
                                'riqueza_lexica 0.25, correccion_gramatical 0.25. '
                                f'word_count_range: {"min: 500, max: 800" if itin in ("ITIN_MAI", "ITIN_INV") else "min: 300, max: 500"}.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_HIST_PRAC',
                    'title': 'Análisis de Fuentes y Comentario Documental',
                    'instructions': (
                        'Analice la fuente histórica primaria proporcionada. '
                        'Determine su naturaleza, datación, contexto de producción, '
                        'fiabilidad y valor historiográfico.'
                    ),
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
                                'Proporciona una fuente histórica primaria (documento, inscripción, '
                                'fotografía, mapa histórico o fragmento de crónica) como source_text. '
                                'Solicita al alumno el comentario de texto histórico según el método '
                                'estándar: clasificación, contexto, análisis del contenido, '
                                'relación con el proceso histórico y valoración crítica. '
                                'word_count_range: min 300, max 500. '
                                'rubric_axes: adecuacion_encargo 0.30, coherencia_cohesion 0.25, '
                                'riqueza_lexica 0.20, correccion_gramatical 0.25.'
                            )
                        }
                    ]
                }
            ]

        # ==============================================================
        # 2. SUB-HUM-PHIL — Dialéctico (Filosofía UGR)
        # 4 fases: test + desarrollo + texto + ensayo
        # Ref: V06DOC_SUBARCHETYPES Sección 2.2
        # ==============================================================
        elif sid == 'SUB-HUM-PHIL':
            return [
                {
                    'subdivision_id': 'SD_PHIL_TEST',
                    'title': 'Test de Precisión Conceptual',
                    'instructions': 'Identifique el concepto, autor o tesis filosófica correcta.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {
                            'block_type': 'PRM-STRIKE',
                            'widget_id': 'W-OBJ-STRIKE',
                            'weight': 0.8,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera 6 preguntas de opción múltiple (A/B/C/D) sobre '
                                'conceptos filosóficos nucleares, autores, obras y tesis del material. '
                                'Las preguntas deben requerir precisión terminológica y distinción conceptual.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_PHIL_DEV',
                    'title': 'Preguntas de Desarrollo Filosófico',
                    'instructions': 'Desarrolle con precisión y rigor los conceptos filosóficos solicitados.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera 2 preguntas de desarrollo filosófico breve (150-200 palabras cada una) '
                                'sobre conceptos nucleares del temario: '
                                'definición precisa, origen doctrinal, relación con otros conceptos '
                                'y posición del filósofo. '
                                'rubric_axes: adecuacion_encargo 0.30, coherencia_cohesion 0.25, '
                                'riqueza_lexica 0.20, correccion_gramatical 0.25. '
                                'word_count_range: min 280, max 450.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_PHIL_TEXT',
                    'title': 'Comentario de Texto Filosófico',
                    'instructions': (
                        'Analice el fragmento filosófico. '
                        'Identifique la tesis, la estructura argumentativa, '
                        'el contexto doctrinal y la posición del autor.'
                    ),
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
                                'Proporciona un fragmento filosófico del corpus del material de estudio '
                                'como source_text (100-200 palabras). '
                                'Solicita al alumno el comentario filosófico según el método UGR: '
                                '1) Análisis de la tesis principal, '
                                '2) Reconstrucción del argumento lógico, '
                                '3) Contextualización en la obra y período del autor, '
                                '4) Relación con el debate filosófico del período. '
                                'word_count_range: min 400, max 600. '
                                'rubric_axes: adecuacion_encargo 0.30, coherencia_cohesion 0.25, '
                                'riqueza_lexica 0.20, correccion_gramatical 0.25.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_PHIL_ESSAY',
                    'title': 'Ensayo Filosófico Argumentado',
                    'instructions': (
                        'Redacte un ensayo filosófico argumentado que confronte '
                        'las posiciones filosóficas relevantes sobre el problema propuesto.'
                    ),
                    'layout_mode': 'STANDARD',
                    'time_limit': 3600,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera un problema filosófico o cuestión dialéctica relacionada '
                                'con el material de estudio que admita posiciones enfrentadas. '
                                'El alumno debe redactar un ensayo argumentado con: '
                                'tesis propia, argumentación con referencia a autores del temario, '
                                'consideración de la antítesis y síntesis conclusiva. '
                                f'word_count_range: {"min: 600, max: 900" if itin in ("ITIN_MAI", "ITIN_INV") else "min: 400, max: 650"}. '
                                'rubric_axes: adecuacion_encargo 0.30, coherencia_cohesion 0.25, '
                                'riqueza_lexica 0.20, correccion_gramatical 0.25.'
                            )
                        }
                    ]
                }
            ]

        # ==============================================================
        # 3. SUB-HUM-ART-HIST — Iconográfico (Historia del Arte UGR)
        # 2 fases no compensables: identificación + análisis
        # Ref: V06DOC_SUBARCHETYPES Sección 2.3
        # ==============================================================
        elif sid == 'SUB-HUM-ART-HIST':
            return [
                {
                    'subdivision_id': 'SD_ART_IDENT',
                    'title': 'Reconocimiento Iconográfico de Imágenes',
                    'instructions': (
                        'Identifique la obra, autor, período, estilo y técnica. '
                        'Proporcione la localización actual y la fecha aproximada de creación.'
                    ),
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 1800,
                    'items': [
                        {
                            'block_type': 'EV-ICON-ART',
                            'widget_id': 'W-ART-IDENT',
                            'weight': 1.0,
                            'fail_logic': 'FATAL',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera el stem invitando al alumno a identificar y analizar '
                                'la obra de arte del período o movimiento del material de '
                                'estudio que se muestra en la imagen adjunta. No incluyas '
                                'ninguna URL en media_assets: el sistema adjunta una imagen '
                                'real verificada, de una unica obra, por separado. '
                                'El alumno debe identificar: titulo, autor, fecha aproximada, '
                                'estilo/movimiento, tecnica y soporte, y localizacion actual, '
                                'y despues redactar el analisis en los tres niveles Panofsky. '
                                'Proporciona en keywords los atributos de identificacion esperados. '
                                'fail_logic=FATAL: la no identificación anula el análisis posterior.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_ART_ANAL',
                    'title': 'Análisis Formal e Iconológico — Método Panofsky',
                    'instructions': (
                        'Realice el análisis formal e iconológico completo de la obra seleccionada '
                        'siguiendo el método de Panofsky (niveles preiconográfico, iconográfico e iconológico).'
                    ),
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 3600,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'El alumno realiza el análisis completo de una de las obras identificadas '
                                'siguiendo el método Panofsky en sus tres niveles: '
                                '1) Preiconográfico: descripción formal (línea, color, composición, espacio), '
                                '2) Iconográfico: identificación de temas, personajes, símbolos y narrativa, '
                                '3) Iconológico: significado intrínseco, contexto sociocultural y función. '
                                'word_count_range: min 500, max 800. '
                                'rubric_axes: adecuacion_encargo 0.30, coherencia_cohesion 0.25, '
                                'riqueza_lexica 0.20, correccion_gramatical 0.25.'
                            )
                        }
                    ]
                }
            ]

        # ==============================================================
        # 4. SUB-HUM-ART-CREA — Bellas Artes (Emulación Parcial Certificada)
        # 2 fases: portafolio + memoria de proceso
        # Ref: V06DOC_SUBARCHETYPES Sección 2.4
        # ==============================================================
        elif sid == 'SUB-HUM-ART-CREA':
            return [
                {
                    'subdivision_id': 'SD_CREA_PORT',
                    'title': 'Portafolio Digital de Proceso Creativo',
                    'instructions': (
                        'Presente el portafolio digital de su proceso creativo. '
                        'Incluya bocetos, versiones intermedias, referentes visuales '
                        'y la obra final documentada.'
                    ),
                    'layout_mode': 'STANDARD',
                    'time_limit': 0,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO',
                            'widget_id': 'W-PORTFOLIO',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera la descripción del ejercicio plástico solicitado '
                                '(técnica, formato, tema, restricciones formales) basado en el material. '
                                'El alumno entrega el portafolio digital via file_uploaded. '
                                'La evaluación analiza: coherencia del proceso creativo, '
                                'dominio técnico, originalidad y adecuación al encargo. '
                                'rubric_axes: adecuacion_encargo 0.30, coherencia_cohesion 0.20, '
                                'riqueza_lexica 0.20, correccion_gramatical 0.30.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_CREA_MEM',
                    'title': 'Memoria de Proceso y Análisis Crítico',
                    'instructions': (
                        'Redacte la memoria de proceso artístico. '
                        'Justifique las decisiones técnicas, formales y conceptuales '
                        'adoptadas durante la creación de la obra.'
                    ),
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Solicita al alumno una memoria de proceso artístico que incluya: '
                                '1) Planteamiento conceptual e intención expresiva, '
                                '2) Referentes artísticos y justificación de su influencia, '
                                '3) Proceso técnico (materiales, herramientas, fases), '
                                '4) Análisis crítico del resultado y posibles mejoras. '
                                'word_count_range: min 400, max 650. '
                                'rubric_axes: adecuacion_encargo 0.30, coherencia_cohesion 0.25, '
                                'riqueza_lexica 0.20, correccion_gramatical 0.25.'
                            )
                        }
                    ]
                }
            ]

        # ==============================================================
        # 5. SUB-HUM-MUS — Musicológico (Historia y Ciencias de la Música UGR)
        # 2 fases bipartitas: auditiva + análisis en partitura
        # Ref: V06DOC_SUBARCHETYPES Sección 2.5
        # ==============================================================
        elif sid == 'SUB-HUM-MUS':
            return [
                {
                    'subdivision_id': 'SD_MUS_LIST',
                    'title': 'Identificación Auditiva Musical',
                    'instructions': (
                        'Escuche el fragmento musical e identifique: compositor, período, '
                        'género, forma musical y características estilísticas.'
                    ),
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {
                            'block_type': 'PRM-STRIKE',
                            'widget_id': 'W-AUDIO-INSTR',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Proporciona la URL de un fragmento musical del período o género '
                                'del material de estudio en media_assets (máx. 2 reproducciones). '
                                'Genera 5 preguntas de opción múltiple sobre: compositor, '
                                'período histórico, género musical, forma (sonata, fuga, etc.) '
                                'y características estilísticas identificables auditivamente.'
                            )
                        },
                        {
                            'block_type': 'EV-MUS-ANAL',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Solicita al alumno un comentario auditivo del fragmento: '
                                'identificación de instrumentación, tonalidad/modalidad aproximada, '
                                'carácter expresivo, elementos rítmicos y melódicos destacables. '
                                'word_count_range: min 150, max 250. '
                                'Proporciona en keywords los términos musicológicos esperados.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_MUS_SCORE',
                    'title': 'Análisis en Partitura — Armónico y Formal',
                    'instructions': (
                        'Analice la partitura proporcionada. '
                        'Identifique la tonalidad, cifre los acordes, '
                        'determine la estructura formal y localice las cadencias.'
                    ),
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 3600,
                    'items': [
                        {
                            'block_type': 'EV-MUS-ANAL',
                            'widget_id': 'W-MUS-SCORE',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Proporciona la URL de una partitura del período del material '
                                'en media_assets (fragmento de 8-16 compases). '
                                'Solicita al alumno: '
                                '1) Identificación de tonalidad y modo, '
                                '2) Cifrado armónico de los acordes principales, '
                                '3) Identificación de cadencias (auténtica, plagal, rota, etc.), '
                                '4) Análisis de la estructura formal (período, frase, sección). '
                                'word_count_range: min 300, max 500. '
                                'Proporciona en keywords los acordes y cadencias esperados.'
                            )
                        }
                    ]
                }
            ]

        # ==============================================================
        # 6. SUB-HUM-ANTH — Antropológico (Subarquetipo Transversal)
        # 2 fases: texto etnográfico + ensayo comparativo
        # Ref: V06DOC_SUBARCHETYPES Sección 2.6
        # ==============================================================
        elif sid == 'SUB-HUM-ANTH':
            return [
                {
                    'subdivision_id': 'SD_ANTH_TEXT',
                    'title': 'Comentario de Fuente Etnográfica',
                    'instructions': (
                        'Analice la fuente etnográfica o el texto antropológico proporcionado. '
                        'Identifique la metodología, el contexto de campo y las categorías analíticas empleadas.'
                    ),
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
                                'Proporciona un fragmento de texto etnográfico o antropológico '
                                '(diario de campo, monografía, artículo) como source_text. '
                                'Solicita al alumno el comentario crítico que incluya: '
                                '1) Identificación del autor, corriente teórica y metodología, '
                                '2) Análisis de las categorías analíticas empleadas, '
                                '3) Evaluación de la posición del investigador (emic/etic, reflexividad), '
                                '4) Valoración de la contribución al campo. '
                                'word_count_range: min 350, max 550. '
                                'rubric_axes: adecuacion_encargo 0.30, coherencia_cohesion 0.25, '
                                'riqueza_lexica 0.20, correccion_gramatical 0.25.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_ANTH_ESSAY',
                    'title': 'Disertación Comparativa Intercultural',
                    'instructions': (
                        'Redacte una disertación comparativa sobre el fenómeno cultural propuesto, '
                        'analizando al menos dos contextos culturales diferentes.'
                    ),
                    'layout_mode': 'STANDARD',
                    'time_limit': 3600,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera un tema de disertación comparativa relacionado con el material: '
                                'un fenómeno cultural universal (parentesco, ritual, tabú, '
                                'organización política, economía simbólica, etc.) que el alumno '
                                'debe analizar comparativamente en dos o más culturas. '
                                'Exige referencia a autores antropológicos del temario. '
                                f'word_count_range: {"min: 600, max: 900" if itin in ("ITIN_MAI", "ITIN_INV") else "min: 400, max: 650"}. '
                                'rubric_axes: adecuacion_encargo 0.30, coherencia_cohesion 0.25, '
                                'riqueza_lexica 0.20, correccion_gramatical 0.25.'
                            )
                        }
                    ]
                }
            ]

        # ------------------------------------------------------------------
        # FALLBACK: Generic humanities skeleton
        # FALLBACK: Esqueleto genérico de humanidades
        # ------------------------------------------------------------------
        else:
            return [
                {
                    'subdivision_id': 'SD_SOURCE',
                    'title': 'Análisis de Fuentes Primarias',
                    'instructions': 'Analice la fuente primaria proporcionada.',
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
                                'Proporciona una fuente primaria del material como source_text. '
                                'Solicita al alumno el comentario crítico con contextualización, '
                                'análisis y valoración. word_count_range: min 300, max 500.'
                            )
                        }
                    ]
                },
                {
                    'subdivision_id': 'SD_DISC',
                    'title': 'Discurso Crítico Argumentado',
                    'instructions': 'Desarrolle el ensayo crítico sobre el tema propuesto.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 3600,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'PENALTY',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera un tema de ensayo crítico relacionado con el material. '
                                'rubric_axes: adecuacion_encargo 0.25, coherencia_cohesion 0.25, '
                                'riqueza_lexica 0.25, correccion_gramatical 0.25. '
                                'word_count_range: min 400, max 650.'
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
        Returns the AI system prompt for this humanities sub-archetype.
        Formal rigor is always highlighted — errors in register are penalized.
        ---
        Devuelve el prompt de sistema de la IA para este sub-arquetipo de humanidades.
        El rigor formal siempre se destaca — los errores de registro tienen penalización.
        """
        roles = {
            'SUB-HUM-HIST':     'Historiador/Arqueólogo Catedrático (UGR). Foco: Crítica de fuentes, cronología, corrientes historiográficas, comentario de texto histórico.',
            'SUB-HUM-PHIL':     'Filósofo y Lógico Catedrático (UGR). Foco: Dialéctica, coherencia argumental, precisión terminológica, análisis de textos filosóficos.',
            'SUB-HUM-ART-HIST': 'Historiador del Arte y Experto Iconológico (UGR). Foco: Análisis formal, método Panofsky, iconografía, contexto cultural.',
            'SUB-HUM-ART-CREA': 'Crítico y Teórico del Arte / Docente de Bellas Artes. Foco: Técnica matérica, proceso creativo, discurso estético, portafolio.',
            'SUB-HUM-MUS':      'Musicólogo Catedrático (UGR). Foco: Análisis armónico-formal, identificación auditiva, cifrado, historia de la música.',
            'SUB-HUM-ANTH':     'Antropólogo Social y Cultural. Foco: Metodología etnográfica, comparación intercultural, corrientes teóricas, reflexividad.'
        }

        base_role = roles.get(self.sub_archetype_id, 'Humanista Académico.')

        itin_ctx = ''
        if self.itinerary_id == 'ITIN_DOC':
            itin_ctx = (
                '\nENFOQUE DIDÁCTICO (ITIN_DOC): '
                'Evalúa la capacidad de transposición didáctica. '
                'Los ítems deben poder ser usados como modelo para la enseñanza secundaria. '
                'Cumplimiento de LOMLOE y enfoque DUA donde proceda.'
            )
        elif self.itinerary_id == 'ITIN_INV':
            itin_ctx = (
                '\nENFOQUE INVESTIGADOR (ITIN_INV): '
                'Rigor bibliográfico absoluto. '
                'Exige cita de fuentes primarias, estado del arte y posicionamiento epistemológico. '
                'Los textos deben alcanzar el estándar de un trabajo académico publicable.'
            )
        elif self.itinerary_id == 'ITIN_MAI':
            itin_ctx = (
                '\nENFOQUE MAIOR (ITIN_MAI): '
                'Máxima exigencia en precisión terminológica, extensión y rigor argumental. '
                'Tolerancia cero en errores formales de registro o cita.'
            )

        return (
            f'IDENTIDAD Y ROL: {base_role}\n'
            f'SUB-ARQUETIPO ACTIVO: {self.sub_archetype_id}\n'
            f'NIVEL PEDAGÓGICO: {self.pedagogical_level} | ITINERARIO: {self.itinerary_id}\n'
            f'{itin_ctx}\n\n'
            f'REGLAS CRÍTICAS DE GENERACIÓN:\n'
            f'1. Los UUID de los ítems son INMUTABLES — devuélvelos exactamente como se reciben.\n'
            f'2. DRA-HOLO requiere siempre: rubric_axes (4 ejes con suma 1.0) y word_count_range en grading_logic.\n'
            f'3. EV-ICON-ART: NUNCA incluyas una URL en media_assets - el sistema adjunta una imagen real verificada mediante un servicio dedicado -, y proporciona los keywords con atributos de identificacion.\n'
            f'4. EV-MUS-ANAL: proporciona keywords con términos musicológicos esperados.\n'
            f'5. Los textos fuente (fuentes históricas, fragmentos filosóficos, partituras) van en source_text o section_stimulus.\n'
            f'6. PROHIBIDO incluir la respuesta correcta en options de forma identificable.\n'
            f'7. Devuelve EXCLUSIVAMENTE el JSON estructurado según ExamSectionSchema — sin texto envolvente.'
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
        Generates the user prompt for atomic humanities section generation.
        ---
        Genera el prompt de usuario para la generación atómica de sección de humanidades.
        """
        memory_note = (
            '\nANTI-REPETICIÓN — Obras, autores o temas ya evaluados (NO REPETIR): ' +
            ', '.join(generated_item_titles)
        ) if generated_item_titles else ''

        skeleton_note = (
            f'\nESQUELETO DE ÍTEMS (OBLIGATORIO — no modificar los item_id UUID):\n{skeleton_json}\n'
        ) if skeleton_json else ''

        return (
            f'GENERA EL CONTENIDO DE EVALUACIÓN HUMANÍSTICA PARA LA SIGUIENTE SECCIÓN.\n\n'
            f'Sub-arquetipo: {self.sub_archetype_id}\n'
            f'Sección objetivo: {subdivision_id}\n'
            f'Tema del material: {topic}\n'
            f'Nivel pedagógico: {self.pedagogical_level} | Itinerario: {self.itinerary_id}\n'
            f'{memory_note}\n\n'
            f'CONTEXTO DEL MATERIAL DE ESTUDIO (máximo 15.000 caracteres):\n'
            f'{(context_text or "")[:15000]}\n\n'
            f'{skeleton_note}\n'
            f'REGLAS DE SALIDA OBLIGATORIAS:\n'
            f'1. Devuelve UN ÚNICO objeto JSON conforme al esquema ExamSectionSchema.\n'
            f'2. Incluye UN ítem por cada UUID del esqueleto. No añadas ni elimines ítems.\n'
            f'3. Conserva cada item_id UUID EXACTAMENTE como aparece en el esqueleto.\n'
            f'4. Para DRA-HOLO: declara siempre rubric_axes y word_count_range en grading_logic.\n'
            f'5. Para EV-PALE: proporciona correct_transcription en grading_logic.\n'
            f'6. Para EV-ICON-ART y EV-MUS-ANAL: proporciona keywords con los términos esperados.\n'
            f'7. Si la sección es SPLIT_TEXT/SPLIT_VISUAL: incluye el texto fuente en section_stimulus.\n'
            f'8. Todo el contenido en castellano con terminología humanística precisa.\n'
            f'9. Genera contenido académico real y riguroso — sin placeholders ni contenido genérico.\n'
            f'10. Los textos fuente (fragmentos filosóficos, fuentes históricas, partituras) '
            f'deben ser reales o verosímiles — no inventados sin base documental.'
        )
