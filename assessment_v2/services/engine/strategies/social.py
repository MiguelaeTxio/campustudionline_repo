# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/social.py
"""
Exam strategy for ARCH_SOC (Ciencias Sociales y Jurídicas).
Covers all 19 certified sub-archetypes of the Social and Legal Sciences branch (v5.9):
  SUB-SOC-LAW-PROC-CIV   — Derecho Procesal Civil (UGR)
  SUB-SOC-LAW-PROC-PEN   — Derecho Procesal Penal (UGR)
  SUB-SOC-LAW-DICT-CIV   — Derecho Civil I-IV — Dictamen (UGR)
  SUB-SOC-LAW-DICT-PEN   — Derecho Penal I-II — Dictamen (UGR)
  SUB-SOC-ECON-QUAN-STAT — Estadística y Técnicas Cuantitativas (UGR)
  SUB-SOC-ECON-QUAN-ECON — Econometría I-III (Economía UGR)
  SUB-SOC-ECON-MGMT-ACC  — Contabilidad Financiera y de Gestión (UGR)
  SUB-SOC-ECON-MGMT-STR  — Dirección Estratégica I-II (ADE UGR)
  SUB-SOC-ECON-MGMT-ECO  — Microeconomía y Macroeconomía (UGR)
  SUB-SOC-EDU-KIDS        — Magisterio Infantil/Primaria DUA (UGR)
  SUB-SOC-EDU-SEC         — Máster Profesorado Secundaria MAES (UGR)
  SUB-SOC-COMM-JOUR       — Periodismo y Redacción (UGR)
  SUB-SOC-COMM-AV         — Comunicación Audiovisual y Guion (UGR)
  SUB-SOC-GEOG-SIG        — Sistemas de Información Geográfica (UGR)
  SUB-SOC-GEOG-TER        — Geografía Humana y Territorial (UGR)
  SUB-SOC-GEOG-FIS        — Geografía Física y Climatología (UGR)
  SUB-SOC-WORK-INT        — Trabajo Social: Intervención Individual/Familiar
  SUB-SOC-WORK-POL        — Trabajo Social: Política Social y Bienestar
  SUB-SOC-WORK-MED        — Trabajo Social: Mediación y Ámbitos Especializados

Complies with V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS,
V06DOC_ARCHETYPES (Casuistic model, FATAL violations for criminal proceedings),
V06DOC_LEVELS (v5.9).
---
Estrategia de examen para ARCH_SOC (Ciencias Sociales y Jurídicas).
Cubre los 19 subarquetipos certificados de la rama de Ciencias Sociales y Jurídicas (v5.9).
"""
from decimal import Decimal
from .base import BaseExamStrategy


class SocialStrategy(BaseExamStrategy):
    """
    Strategy for Social and Legal Sciences (ARCH_SOC).
    The casuistic model centers on practical cases (supuestos prácticos) with
    mandatory legal/normative grounding and verified real source citation.
    Specific FATAL rules apply for criminal procedure and gender violence mediation.
    All 19 certified sub-archetypes have specific skeletons.
    ---
    Estrategia para Ciencias Sociales y Jurídicas (ARCH_SOC).
    El modelo casuístico se centra en supuestos prácticos con fundamentación
    jurídica/normativa obligatoria y cita de fuentes reales verificadas.
    Reglas FATAL específicas para proceso penal y mediación en violencia de género.
    Los 19 subarquetipos certificados tienen esqueletos específicos.
    """

    # =========================================================================
    # GRADING ENGINE
    # MOTOR DE CALIFICACIÓN
    # Ref: V06DOC_BLOCKS (motores específicos para ARCH_SOC)
    # =========================================================================

    def grade_item(self, item, student_input) -> tuple:
        """
        Routes each item to the correct grading motor.
        DRA-HOLO detects real source citations and signals GradingOrchestrator
        with 'fuentes_reales' for the +20% bonus application.
        ---
        Enruta cada ítem al motor de calificación correcto.
        DRA-HOLO detecta citas de fuentes reales y señala al GradingOrchestrator
        con 'fuentes_reales' para la aplicación del bonus del +20%.
        """
        block_type = item.block_type

        if block_type == 'DRA-HOLO':
            return self._grade_dra_holo_social(item, student_input)

        elif block_type == 'PRM-STRIKE':
            return self._grade_prm_strike(item, student_input)

        elif block_type == 'RBT-CANON':
            return self._grade_rbt_canon(item, student_input)

        elif block_type == 'MAT-LINK':
            return self._grade_mat_link(item, student_input)

        elif block_type == 'CLO-MULTI':
            return self._grade_clo_multi(item, student_input)

        elif block_type == 'RPP-TRAZA':
            return self._grade_rpp_traza(item, student_input)

        elif block_type == 'ILC-CONTEXT':
            return self._grade_ilc_context(item, student_input)

        elif block_type == 'CDS-KILL':
            return self._grade_cds_kill(item, student_input)

        # Fallback / Fallback
        return Decimal('0.0'), {
            'status': 'MOTOR_NOT_IMPLEMENTED',
            'feedback_category': 'FB_CONCEPT',
            'justification': f'Motor {block_type} no implementado para ARCH_SOC.'
        }

    def _grade_dra_holo_social(self, item, student_input) -> tuple:
        """
        DRA-HOLO variant for social/legal sciences.
        Detects normative/legal citations in the student response.
        When verified citations are found, signals 'fuentes_reales' in the justification
        so GradingOrchestrator applies the +20% real source multiplier.
        Also applies the base DRA-HOLO holistic evaluation (AI-pending).
        ---
        Variante DRA-HOLO para ciencias sociales y jurídicas.
        Detecta citas normativas/jurídicas en la respuesta del alumno.
        Cuando se detectan citas verificadas, señaliza 'fuentes_reales' en la justificación
        para que GradingOrchestrator aplique el multiplicador del +20% de fuentes reales.
        Aplica también la evaluación holística base DRA-HOLO (pendiente de IA).
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
                'justification': 'No se ha proporcionado ninguna respuesta al supuesto.'
            }

        word_count = len(student_text.split())

        # Detect normative/legal citations / Detectar citas normativas/jurídicas
        # Required norms declared in grading_logic by the AI
        # Normas requeridas declaradas en grading_logic por la IA
        required_norms  = logic.get('required_norms', [])
        citations_found = sum(
            1 for norm in required_norms
            if norm.lower() in student_text.lower()
        ) if required_norms else 0

        has_real_sources = citations_found > 0

        # Base heuristic score / Puntuación heurística base
        heuristic_score = Decimal('0.6')
        heuristic_score = max(Decimal('0.0'), heuristic_score + formal_penalty)

        # Build justification with real source signal
        # Construir justificación con señal de fuentes reales
        justification = logic.get('feedback_justification', '')
        if has_real_sources:
            justification = f'fuentes_reales verificadas ({citations_found}/{len(required_norms)}). ' + justification

        return heuristic_score, {
            'status': 'PENDING_AI_ANALYSIS',
            'feedback_category': 'FB_FORMAL',
            'justification': justification,
            'word_count': word_count,
            'citations_found': citations_found,
            'required_norms_count': len(required_norms),
            'pending_ai_refinement': True
        }

    # =========================================================================
    # EXAM SKELETON — 19 certified sub-archetypes
    # ESQUELETO DE EXAMEN — 19 subarquetipos certificados
    # Ref: V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS (v5.9)
    # =========================================================================

    def get_exam_skeleton(self) -> list:
        """
        Returns the full structural skeleton for the sub-archetype.
        Legal/procedural sub-archetypes include FATAL rules for critical violations.
        ---
        Devuelve el esqueleto estructural completo para el sub-arquetipo.
        Los subarquetipos jurídicos/procesales incluyen reglas FATAL para violaciones críticas.
        Ref: V06DOC_STRUCTURE (Skeleton-First Protocol), V06DOC_SUBARCHETYPES v5.9.
        """
        sid  = self.sub_archetype_id
        itin = self.itinerary_id

        # Shared task instructions / Instrucciones de tarea compartidas
        I_PRM     = 'Genera una pregunta de opción múltiple (A/B/C/D) sobre conceptos jurídicos, normativos o teóricos fundamentales.'
        I_CASO    = 'Genera un supuesto práctico detallado. El alumno debe redactar una solución fundamentada con cita normativa.'
        I_LAW_NAV = 'Genera un ejercicio de búsqueda legislativa o jurisprudencial simulada con el repositorio normativo.'

        # ==============================================================
        # RAMA DERECHO PROCESAL CIVIL
        # ==============================================================

        # 1. SUB-SOC-LAW-PROC-CIV
        if sid == 'SUB-SOC-LAW-PROC-CIV':
            return [
                {
                    'subdivision_id': 'SD_PROC_CIV_PRINCIPIOS',
                    'title': 'Principios y Presupuestos Procesales Civiles',
                    'instructions': 'Identifique los presupuestos procesales y los principios del proceso civil aplicables al caso.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre presupuestos procesales (competencia, capacidad, legitimación), principios procesales (dispositivo, aportación, contradicción) y tipos de procesos civiles (ordinario, verbal, monitorio).'}
                    ]
                },
                {
                    'subdivision_id': 'SD_PROC_CIV_DEMANDA',
                    'title': 'Demanda, Contestación y Proceso Declarativo',
                    'instructions': 'Redacte el escrito procesal solicitado y determine la vía procesal adecuada.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-LAW-NAV', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un supuesto de litigio civil (arrendamiento, responsabilidad contractual, '
                             'reclamación de cantidad) y solicita al alumno la redacción del escrito de demanda '
                             'o contestación con: hechos, fundamentos de derecho y suplico. '
                             'required_norms: [LEC arts. relevantes, CC arts. relevantes]. '
                             'word_count_range: min 300, max 500. '
                             f'rubric_axes: adecuacion_encargo 0.30, coherencia_cohesion 0.25, riqueza_lexica 0.20, correccion_gramatical 0.25.'
                         )}
                    ]
                },
                {
                    'subdivision_id': 'SD_PROC_CIV_EXEC',
                    'title': 'Ejecución Forzosa y Medidas Cautelares',
                    'instructions': 'Determine el procedimiento de ejecución y las medidas cautelares aplicables.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre ejecución de sentencias (dineraria, no dineraria), medidas cautelares (embargo preventivo, anotación preventiva) y recursos procesales (apelación, casación).'}
                    ]
                }
            ]

        # 2. SUB-SOC-LAW-PROC-PEN
        elif sid == 'SUB-SOC-LAW-PROC-PEN':
            return [
                {
                    'subdivision_id': 'SD_PROC_PEN_INVEST',
                    'title': 'Instrucción e Investigación Penal',
                    'instructions': 'Identifique las diligencias de investigación procedentes y sus requisitos constitucionales.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre diligencias de investigación (entrada y registro, intervención de comunicaciones, reconocimientos en rueda), garantías constitucionales y nulidad de la prueba.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_PROC_PEN_JUICIO',
                    'title': 'Juicio Oral Penal — Principios y Prueba',
                    'instructions': 'Analice la validez de la prueba y la aplicación de los principios del juicio oral.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-LAW-NAV', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un caso penal con prueba potencialmente nula '
                             '(entrada sin autorización judicial, declaración bajo coacción, etc.). '
                             'El alumno debe analizar: legalidad de la prueba, regla de exclusión, '
                             'doctrina del fruto del árbol envenenado y efecto en el juicio oral. '
                             'required_norms: [CE art. 24, LECRIM arts. relevantes, STC relevantes]. '
                             'word_count_range: min 350, max 550.'
                         )}
                    ]
                },
                {
                    'subdivision_id': 'SD_PROC_PEN_SENT',
                    'title': 'Sentencia Penal y Recursos',
                    'instructions': 'Determine la calificación jurídica de los hechos y la pena aplicable.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre estructura de la sentencia penal, calificación de los hechos, determinación de la pena (reglas del CP art. 66) y recursos (apelación, casación, revisión).'}
                    ]
                }
            ]

        # 3. SUB-SOC-LAW-DICT-CIV
        elif sid == 'SUB-SOC-LAW-DICT-CIV':
            return [
                {
                    'subdivision_id': 'SD_DICT_CIV_PERSONA',
                    'title': 'Persona, Familia y Derecho Civil General',
                    'instructions': 'Resuelva el supuesto de derecho civil personal o familiar.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre personas jurídicas, capacidad de obrar, matrimonio, filiación, patria potestad y tutela según el Código Civil reformado (Ley 8/2021).'}
                    ]
                },
                {
                    'subdivision_id': 'SD_DICT_CIV_OBLIG',
                    'title': 'Obligaciones y Contratos — Dictamen',
                    'instructions': 'Redacte el dictamen jurídico sobre el contrato o la responsabilidad civil planteada.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-LAW-NAV', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un supuesto de incumplimiento contractual, vicio del consentimiento '
                             'o responsabilidad extracontractual (art. 1902 CC). '
                             'El alumno redacta un dictamen jurídico con: '
                             'hechos relevantes, calificación jurídica, normativa aplicable, '
                             'pretensiones ejercitables y probabilidad de éxito. '
                             'required_norms: [CC arts. relevantes, STS relevantes]. '
                             'word_count_range: min 400, max 600.'
                         )}
                    ]
                },
                {
                    'subdivision_id': 'SD_DICT_CIV_REAL',
                    'title': 'Derechos Reales y Propiedad',
                    'instructions': 'Determine los derechos reales aplicables y su protección registral.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre propiedad, posesión, usufructo, servidumbres, hipoteca y Registro de la Propiedad (Ley Hipotecaria).'}
                    ]
                }
            ]

        # 4. SUB-SOC-LAW-DICT-PEN
        elif sid == 'SUB-SOC-LAW-DICT-PEN':
            return [
                {
                    'subdivision_id': 'SD_DICT_PEN_TIPOS',
                    'title': 'Tipos Penales y Bien Jurídico Protegido',
                    'instructions': 'Califique jurídico-penalmente los hechos e identifique el bien jurídico protegido.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas de calificación penal: identificación del tipo delictivo (doloso/imprudente, comisión/omisión), bien jurídico, sujeto activo/pasivo y elemento subjetivo del injusto.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_DICT_PEN_CONCURSO',
                    'title': 'Concurso de Delitos y Determinación de la Pena',
                    'instructions': 'Resuelva el concurso de delitos y calcule la pena aplicable.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-LAW-NAV', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un supuesto penal con concurso de infracciones (real, ideal, medial) '
                             'o circunstancias modificativas. '
                             'El alumno debe: calificar cada hecho, resolver el concurso según el CP, '
                             'determinar la pena en abstracto, aplicar las reglas del art. 66 CP '
                             'y fijar la pena en concreto. '
                             'required_norms: [CP arts. relevantes]. '
                             'word_count_range: min 400, max 600.'
                         )},
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un ejercicio de cálculo de pena según las reglas del CP: '
                             'step_matrix: identificar el tipo penal y su marco penal, '
                             'aplicar las circunstancias modificativas, '
                             'resolver el concurso, determinar la pena concreta.'
                         )}
                    ]
                }
            ]

        # ==============================================================
        # RAMA ECONOMÍA Y ADE
        # ==============================================================

        # 5. SUB-SOC-ECON-QUAN-STAT
        elif sid == 'SUB-SOC-ECON-QUAN-STAT':
            return [
                {
                    'subdivision_id': 'SD_STAT_FUND',
                    'title': 'Estadística y Técnicas Cuantitativas',
                    'instructions': 'Aplique las técnicas estadísticas adecuadas al caso económico.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre estadística descriptiva, distribuciones de probabilidad, contrastes de hipótesis y análisis de varianza aplicados a datos económicos.'},
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de análisis estadístico con datos económicos reales: '
                             'cálculo de medias, varianzas, correlación o contraste de hipótesis. '
                             'step_matrix: calcular el estadístico descriptivo, '
                             'plantear el contraste, calcular el p-valor, interpretar.'
                         )}
                    ]
                }
            ]

        # 6. SUB-SOC-ECON-QUAN-ECON
        elif sid == 'SUB-SOC-ECON-QUAN-ECON':
            return [
                {
                    'subdivision_id': 'SD_ECON_REGRESION',
                    'title': 'Econometría — Regresión y MCO',
                    'instructions': 'Estime y valide el modelo de regresión lineal por Mínimos Cuadrados Ordinarios.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de estimación MCO con datos económicos. '
                             'step_matrix: especificar el modelo, estimar los coeficientes, '
                             'contrastar la significatividad (t y F), interpretar el R², '
                             'verificar los supuestos del modelo (heterocedasticidad, autocorrelación).'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 3 preguntas sobre interpretación de coeficientes, elasticidades y validación del modelo econométrico.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_ECON_SERIES',
                    'title': 'Series Temporales y Predicción',
                    'instructions': 'Analice la serie temporal e identifique sus componentes.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo un gráfico de serie temporal económica '
                             '(PIB, IPC, desempleo) con tendencia, estacionalidad y ciclo. '
                             'El alumno identifica los componentes, determina la estacionariedad '
                             'y propone el modelo de predicción adecuado (ARIMA, Holt-Winters).'
                         )}
                    ]
                }
            ]

        # 7. SUB-SOC-ECON-MGMT-ACC
        elif sid == 'SUB-SOC-ECON-MGMT-ACC':
            return [
                {
                    'subdivision_id': 'SD_ACC_FUND',
                    'title': 'Contabilidad Financiera — Fundamentos',
                    'instructions': 'Registre las operaciones contables y elabore los estados financieros.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un conjunto de operaciones contables de una empresa '
                             '(compras, ventas, amortizaciones, provisiones) y solicita '
                             'el asiento contable, la cuenta T y el balance de situación. '
                             'step_matrix: identificar debe/haber, registrar el asiento, '
                             'actualizar las cuentas T, elaborar el balance parcial.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 3 preguntas sobre principios contables (PGC), criterios de valoración (coste amortizado, valor razonable) y normativa NIIF.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_ACC_ANALISIS',
                    'title': 'Análisis de Estados Financieros',
                    'instructions': 'Calcule e interprete los ratios financieros del caso.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem proporcionando el balance de situación y la cuenta de PyG '
                             'de una empresa como section_stimulus. '
                             'El alumno calcula los ratios de liquidez, endeudamiento, rentabilidad '
                             'y rotación, interpreta la situación financiera y propone medidas correctoras. '
                             'Proporciona en keywords los ratios y valores esperados.'
                         )}
                    ]
                }
            ]

        # 8. SUB-SOC-ECON-MGMT-STR
        elif sid == 'SUB-SOC-ECON-MGMT-STR':
            return [
                {
                    'subdivision_id': 'SD_STR_ANALISIS',
                    'title': 'Análisis Estratégico del Entorno',
                    'instructions': 'Realice el análisis externo e interno de la empresa propuesta.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre análisis PESTEL, 5 fuerzas de Porter, cadena de valor, recursos y capacidades, y análisis DAFO.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_STR_FORMULA',
                    'title': 'Formulación e Implantación Estratégica',
                    'instructions': 'Formule la estrategia competitiva adecuada y diseñe el plan de implantación.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un caso de empresa con problema estratégico definido '
                             '(entrada en nuevo mercado, relanzamiento de producto, reestructuración). '
                             'El alumno propone la estrategia con: análisis situacional, '
                             'opciones estratégicas evaluadas, estrategia seleccionada con justificación, '
                             'plan de acción y KPIs de control. '
                             'word_count_range: min 400, max 600. '
                             f'required_norms: [] (no requeridas para estrategia — but valorar referencias a autores como Porter, Barney, etc.).'
                         )}
                    ]
                }
            ]

        # 9. SUB-SOC-ECON-MGMT-ECO
        elif sid == 'SUB-SOC-ECON-MGMT-ECO':
            return [
                {
                    'subdivision_id': 'SD_MICRO_FUND',
                    'title': 'Microeconomía — Teoría del Consumidor y la Empresa',
                    'instructions': 'Analice el equilibrio del consumidor y la empresa en el mercado.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre teoría del consumidor (utilidad, curvas de indiferencia, restricción presupuestaria), teoría de la empresa (costes, producción, maximización del beneficio) y estructuras de mercado.'},
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de equilibrio del consumidor o de la empresa: '
                             'maximización de utilidad sujeta a restricción, o maximización de beneficio '
                             'en competencia perfecta/monopolio. '
                             'step_matrix: plantear el problema de optimización, derivar las condiciones '
                             'de primer orden, resolver el sistema, interpretar el equilibrio.'
                         )}
                    ]
                },
                {
                    'subdivision_id': 'SD_MACRO_FUND',
                    'title': 'Macroeconomía — Modelos de Equilibrio',
                    'instructions': 'Analice el equilibrio macroeconómico y los efectos de la política económica.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre modelo IS-LM, DA-OA, política fiscal y monetaria, multiplicador keynesiano y crecimiento económico (Solow).'}
                    ]
                }
            ]

        # ==============================================================
        # RAMA EDUCACIÓN
        # ==============================================================

        # 10. SUB-SOC-EDU-KIDS
        elif sid == 'SUB-SOC-EDU-KIDS':
            return [
                {
                    'subdivision_id': 'SD_EDU_DUA',
                    'title': 'Diseño Universal para el Aprendizaje (DUA/LOMLOE)',
                    'instructions': 'Adapte la propuesta didáctica para la diversidad del aula siguiendo el marco DUA.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre principios DUA (representación múltiple, acción/expresión, implicación), LOMLOE (competencias clave, situaciones de aprendizaje, perfiles de salida) y atención a la diversidad.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_EDU_SITUACION',
                    'title': 'Situación de Aprendizaje y Programación Didáctica',
                    'instructions': 'Diseñe una situación de aprendizaje completa para el nivel de Infantil o Primaria.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un contexto educativo (curso, área, necesidades del grupo) '
                             'y solicita al alumno el diseño de una situación de aprendizaje con: '
                             'título, competencias clave y específicas, objetivos, descripción de actividades '
                             '(inicio, desarrollo, cierre), recursos, adaptaciones DUA e instrumentos de evaluación. '
                             'required_norms: [LOMLOE, Real Decreto de currículo de Primaria o Infantil]. '
                             'word_count_range: min 400, max 650.'
                         )}
                    ]
                }
            ]

        # 11. SUB-SOC-EDU-SEC
        elif sid == 'SUB-SOC-EDU-SEC':
            return [
                {
                    'subdivision_id': 'SD_EDU_MAES_PROC',
                    'title': 'Procesos y Contextos Educativos — MAES UGR',
                    'instructions': 'Analice el contexto educativo y los procesos de aprendizaje en Secundaria.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre psicología del aprendizaje adolescente, tutoría, orientación, convivencia escolar y marco normativo de la ESO y Bachillerato (LOMLOE).'}
                    ]
                },
                {
                    'subdivision_id': 'SD_EDU_MAES_DID',
                    'title': 'Didáctica Específica — Diseño de Unidad Didáctica',
                    'instructions': 'Diseñe la unidad didáctica para la especialidad y nivel asignados.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un contexto de aula de Secundaria (especialidad, curso, grupo-clase) '
                             'y solicita el diseño de una Unidad Didáctica con: '
                             'justificación y contextualización, competencias específicas, criterios de evaluación, '
                             'saberes básicos, secuencia de actividades y metodología activa, '
                             'temporización e instrumentos de evaluación. '
                             'required_norms: [LOMLOE, Real Decreto 217/2022, normativa autonómica]. '
                             'word_count_range: min 500, max 800.'
                         )}
                    ]
                }
            ]

        # ==============================================================
        # RAMA COMUNICACIÓN
        # ==============================================================

        # 12. SUB-SOC-COMM-JOUR
        elif sid == 'SUB-SOC-COMM-JOUR':
            return [
                {
                    'subdivision_id': 'SD_JOUR_ETICA',
                    'title': 'Ética, Deontología y Verificación Periodística',
                    'instructions': 'Valore el tratamiento informativo del caso desde la perspectiva ética y deontológica.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre códigos deontológicos (FAPE, APM), derecho a la información vs. derecho al honor, verificación de fuentes (fact-checking) y responsabilidad del periodista.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_JOUR_REDACCION',
                    'title': 'Redacción Periodística — Géneros Informativos',
                    'instructions': 'Redacte la pieza periodística solicitada respetando el género y el libro de estilo.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un conjunto de datos noticiables (declaraciones, hechos, contexto) '
                             'como source_text y solicita al alumno la redacción de: '
                             'una noticia (pirámide invertida), una crónica o un reportaje en profundidad. '
                             'Se evalúa: estructura del género, pirámide de datos, rigor informativo, '
                             'estilo y deontología. word_count_range: min 300, max 500.'
                         )}
                    ]
                }
            ]

        # 13. SUB-SOC-COMM-AV
        elif sid == 'SUB-SOC-COMM-AV':
            return [
                {
                    'subdivision_id': 'SD_AV_GUION',
                    'title': 'Guion Audiovisual — Literario y Técnico',
                    'instructions': 'Redacte el guion literario o técnico del producto audiovisual propuesto.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera una sinopsis o premisa narrativa y solicita al alumno '
                             'la redacción de: una escaleta (estructura narrativa), '
                             'una secuencia de guion literario (con acotaciones de acción y diálogos) '
                             'y el guion técnico de 2-3 planos con descripción técnica. '
                             'word_count_range: min 350, max 550.'
                         )}
                    ]
                },
                {
                    'subdivision_id': 'SD_AV_REALIZACION',
                    'title': 'Técnica de Realización y Postproducción',
                    'instructions': 'Resuelva los problemas técnicos de producción audiovisual.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre óptica y objetivos, iluminación (temperatura de color, ratio), sonido (micrófono, pistas), formatos de vídeo y flujo de postproducción.'}
                    ]
                }
            ]

        # ==============================================================
        # RAMA GEOGRAFÍA
        # ==============================================================

        # 14. SUB-SOC-GEOG-SIG
        elif sid == 'SUB-SOC-GEOG-SIG':
            return [
                {
                    'subdivision_id': 'SD_GEOG_SIG_ANALISIS',
                    'title': 'Análisis SIG y Cartografía Digital',
                    'instructions': 'Interprete el análisis espacial e identifique los patrones geográficos.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo una salida de análisis SIG '
                             '(mapa temático, análisis de proximidad, interpolación, cluster espacial). '
                             'El alumno interpreta los resultados, identifica los patrones espaciales '
                             'y valora la metodología SIG empleada. '
                             'Proporciona en keywords los conceptos espaciales esperados.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 3 preguntas sobre tipos de datos geoespaciales (vectorial, ráster), sistemas de referencia (UTM, WGS84), análisis espacial (buffer, overlay, red) y software SIG (QGIS, ArcGIS).'}
                    ]
                }
            ]

        # 15. SUB-SOC-GEOG-TER
        elif sid == 'SUB-SOC-GEOG-TER':
            return [
                {
                    'subdivision_id': 'SD_GEOG_TER_ANALISIS',
                    'title': 'Análisis Territorial y Demografía',
                    'instructions': 'Analice la estructura territorial y los procesos demográficos del área propuesta.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo una pirámide poblacional, '
                             'mapa de densidad o indicadores demográficos de un territorio. '
                             'El alumno interpreta la estructura demográfica, '
                             'identifica las dinámicas (envejecimiento, migración, urbanización) '
                             'y valora sus implicaciones territoriales. '
                             'Proporciona en keywords los indicadores demográficos esperados.'
                         )},
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Solicita al alumno un análisis territorial integrado: '
                             'diagnóstico demográfico, estructura económica, problemas ambientales '
                             'y propuesta de ordenación del territorio. '
                             'word_count_range: min 300, max 500.'
                         )}
                    ]
                }
            ]

        # 16. SUB-SOC-GEOG-FIS
        elif sid == 'SUB-SOC-GEOG-FIS':
            return [
                {
                    'subdivision_id': 'SD_GEOG_FIS_CLIMA',
                    'title': 'Climatología y Geomorfología',
                    'instructions': 'Analice el clima y los procesos geomorfológicos del área propuesta.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo un climograma, mapa de isoyetas '
                             'o perfil topográfico con indicaciones geomorfológicas. '
                             'El alumno identifica el tipo climático, interpreta los datos '
                             'y explica los procesos geomorfológicos dominantes. '
                             'Proporciona en keywords los términos climatológicos y geomorfológicos esperados.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre clasificaciones climáticas (Köppen, Papadakis), factores del clima, agentes y procesos geomorfológicos (fluvial, eólico, kárstico, glaciar).'}
                    ]
                }
            ]

        # ==============================================================
        # RAMA TRABAJO SOCIAL
        # ==============================================================

        # 17. SUB-SOC-WORK-INT
        elif sid == 'SUB-SOC-WORK-INT':
            return [
                {
                    'subdivision_id': 'SD_WORK_INT_THEO',
                    'title': 'Teoría y Modelos de Intervención Social',
                    'instructions': 'Identifique el modelo de intervención adecuado al caso.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre modelos de trabajo social (sistémico, ecológico, conductual, humanista), fases del proceso de intervención y ética profesional (deontología del TS).'}
                    ]
                },
                {
                    'subdivision_id': 'SD_WORK_INT_PRAC',
                    'title': 'Intervención Social — Diagnóstico y Plan de Caso',
                    'instructions': 'Elabore el diagnóstico social y el plan de intervención para el caso propuesto.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un caso de intervención individual/familiar '
                             '(familia en riesgo, persona mayor dependiente, menor en protección). '
                             'El alumno elabora: diagnóstico social (necesidades, recursos, fortalezas), '
                             'objetivos de intervención, metodología (entrevista, trabajo grupal, coordinación '
                             'interinstitucional) y plan de seguimiento. '
                             'required_norms: [Ley de Servicios Sociales autonómica, Ley 39/2006]. '
                             'word_count_range: min 350, max 550.'
                         )}
                    ]
                }
            ]

        # 18. SUB-SOC-WORK-POL
        elif sid == 'SUB-SOC-WORK-POL':
            return [
                {
                    'subdivision_id': 'SD_WORK_POL_THEO',
                    'title': 'Política Social — Estado de Bienestar y Modelos',
                    'instructions': 'Analice el modelo de bienestar y las políticas sociales vigentes.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre modelos de estado de bienestar (Esping-Andersen), sistemas de protección social (pensiones, desempleo, sanidad), políticas activas de empleo y tendencias de reforma.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_WORK_POL_PRAC',
                    'title': 'Análisis Crítico de Política Social',
                    'instructions': 'Analice críticamente la política social propuesta y sus efectos.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un supuesto de análisis de una medida de política social '
                             '(reforma de pensiones, renta mínima, ayuda a la vivienda). '
                             'El alumno elabora un informe crítico con: '
                             'objetivos declarados, colectivo beneficiario, financiación, '
                             'efectos distributivos, evaluación y propuesta de mejora. '
                             'required_norms: [Normativa específica de la política analizada]. '
                             'word_count_range: min 350, max 550.'
                         )}
                    ]
                }
            ]

        # 19. SUB-SOC-WORK-MED
        elif sid == 'SUB-SOC-WORK-MED':
            return [
                {
                    'subdivision_id': 'SD_WORK_MED_THEO',
                    'title': 'Mediación Social — Teoría y Modelos',
                    'instructions': 'Identifique el modelo de mediación adecuado y sus fases.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre modelos de mediación (Harvard, transformativo, circular-narrativo), fases del proceso, principios éticos y ámbitos especializados (familia, penal, intercultural).'}
                    ]
                },
                {
                    'subdivision_id': 'SD_WORK_MED_PRAC',
                    'title': 'Supuesto de Mediación — Plan de Intervención',
                    'instructions': 'Diseñe el plan de mediación para el conflicto propuesto.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 2400,
                    'items': [
                        {
                            'block_type': 'DRA-HOLO',
                            'widget_id': 'W-HUM-TEXT',
                            'weight': 1.0,
                            'fail_logic': 'FATAL',
                            'level_requisite': 'MANDATORY',
                            'task_instruction': (
                                'Genera un caso de conflicto susceptible de mediación '
                                '(separación/divorcio, conflicto vecinal, mediación intercultural). '
                                'PROHIBIDO incluir casos de violencia de género, violencia doméstica '
                                'o cualquier situación donde la mediación esté legalmente vedada '
                                '(LO 1/2004 art. 44.5, LO 8/2021). '
                                'El alumno diseña el plan de mediación: evaluación de la idoneidad, '
                                'fases del proceso, técnicas de comunicación y acuerdo. '
                                'required_norms: [Ley 5/2012 de Mediación, normativa autonómica]. '
                                'word_count_range: min 350, max 550. '
                                'KILL_SWITCH: Si el alumno propone mediación en caso de violencia de género, '
                                'la sección queda anulada (FATAL — LO 1/2004 art. 44.5).'
                            )
                        }
                    ]
                }
            ]

        # ------------------------------------------------------------------
        # FALLBACK: Generic social skeleton
        # FALLBACK: Esqueleto genérico de ciencias sociales
        # ------------------------------------------------------------------
        else:
            return [
                {
                    'subdivision_id': 'SD_FACT',
                    'title': 'Análisis del Caso Práctico',
                    'instructions': 'Identifique y jerarquice los hechos relevantes del supuesto.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': I_PRM}
                    ]
                },
                {
                    'subdivision_id': 'SD_PROC',
                    'title': 'Resolución Fundamentada',
                    'instructions': 'Redacte la solución fundamentada al supuesto propuesto.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': I_CASO}
                    ]
                }
            ]

    # =========================================================================
    # SYSTEM PROMPT
    # PROMPT DE SISTEMA
    # =========================================================================

    def get_system_prompt(self) -> str:
        """
        Returns the AI system prompt for this social/legal sub-archetype.
        Legal sub-archetypes always highlight normative citation requirements.
        ---
        Devuelve el prompt de sistema de la IA para este sub-arquetipo social/jurídico.
        Los subarquetipos jurídicos siempre destacan los requisitos de cita normativa.
        """
        roles = {
            'SUB-SOC-LAW-PROC-CIV':    'Letrado/a de la Administración de Justicia (Civil). Foco: Técnica procesal civil, LEC, plazos y recursos.',
            'SUB-SOC-LAW-PROC-PEN':    'Fiscal / Letrado Penal. Foco: LECRIM, garantías constitucionales, prueba ilícita, juicio oral.',
            'SUB-SOC-LAW-DICT-CIV':    'Magistrado/a Civil / Notario. Foco: CC reformado, dictamen civil, contratos, derechos reales.',
            'SUB-SOC-LAW-DICT-PEN':    'Magistrado/a Penal / Penalista. Foco: CP, calificación penal, concurso de delitos, determinación de pena.',
            'SUB-SOC-ECON-QUAN-STAT':  'Estadístico/a Económico. Foco: Estadística aplicada a Economía, contrastes, análisis descriptivo.',
            'SUB-SOC-ECON-QUAN-ECON':  'Econometrista. Foco: Regresión MCO, series temporales, validación de modelos econométricos.',
            'SUB-SOC-ECON-MGMT-ACC':   'Auditor/a / Contable. Foco: PGC, asientos contables, análisis de estados financieros, NIIF.',
            'SUB-SOC-ECON-MGMT-STR':   'Consultor/a de Estrategia (ADE). Foco: Análisis competitivo, formulación estratégica, Porter, DAFO.',
            'SUB-SOC-ECON-MGMT-ECO':   'Catedrático/a de Economía. Foco: Microeconomía (optimización), Macroeconomía (IS-LM, DA-OA).',
            'SUB-SOC-EDU-KIDS':        'Maestro/a Especialista (Infantil/Primaria). Foco: DUA, situaciones de aprendizaje, LOMLOE, competencias clave.',
            'SUB-SOC-EDU-SEC':         'Catedrático/a de Secundaria — MAES. Foco: Didáctica específica, unidades didácticas, orientación, LOMLOE.',
            'SUB-SOC-COMM-JOUR':       'Redactor/a Jefe / Periodista. Foco: Géneros informativos, ética periodística, verificación, libro de estilo.',
            'SUB-SOC-COMM-AV':         'Realizador/a Audiovisual / Guionista. Foco: Guion literario y técnico, narrativa audiovisual, producción.',
            'SUB-SOC-GEOG-SIG':        'Geógrafo/a SIG / Analista Espacial. Foco: Análisis geoespacial, QGIS, cartografía digital, datos ráster/vector.',
            'SUB-SOC-GEOG-TER':        'Geógrafo/a Humano/a. Foco: Demografía, ordenación del territorio, urbanismo, dinámicas territoriales.',
            'SUB-SOC-GEOG-FIS':        'Geógrafo/a Físico/a. Foco: Climatología, geomorfología, hidrología, biogeografía.',
            'SUB-SOC-WORK-INT':        'Trabajador/a Social de Caso. Foco: Diagnóstico social, intervención individual/familiar, coordinación.',
            'SUB-SOC-WORK-POL':        'Especialista en Política Social. Foco: Estado de bienestar, sistemas de protección, análisis de políticas.',
            'SUB-SOC-WORK-MED':        'Mediador/a Social. Foco: Modelos de mediación, proceso, ámbitos especializados. PROHIBIDO proponer mediación en VG.'
        }

        base_role = roles.get(self.sub_archetype_id, 'Especialista en Ciencias Sociales y Jurídicas.')

        itin_ctx = ''
        if self.itinerary_id == 'ITIN_PROF':
            itin_ctx = (
                '\nENFOQUE PROFESIONAL (ITIN_PROF): '
                'Exige rigor absoluto en la cita normativa actualizada. '
                'Las respuestas incompletas en fundamentación jurídica o normativa '
                'deben declararse insuficientes en feedback_justification. '
                'Incluir siempre required_norms en grading_logic.'
            )
        elif self.itinerary_id == 'ITIN_MAI':
            itin_ctx = (
                '\nENFOQUE MAIOR (ITIN_MAI): '
                'Máxima exigencia en precisión conceptual, cita de fuentes y extensión. '
                'Los supuestos deben tener complejidad alta con concurso de normas o situaciones límite.'
            )

        fatal_note = ''
        if self.sub_archetype_id == 'SUB-SOC-WORK-MED':
            fatal_note = (
                '\nALERTA FATAL — MEDIACIÓN EN VG: '
                'PROHIBIDO ABSOLUTO generar supuestos que impliquen o puedan implicar violencia de género. '
                'La LO 1/2004 art. 44.5 prohíbe expresamente la mediación en estos casos. '
                'Si por error se genera un supuesto de VG, declara el ítem como FATAL en grading_logic.'
            )

        return (
            f'IDENTIDAD Y ROL: {base_role}\n'
            f'SUB-ARQUETIPO ACTIVO: {self.sub_archetype_id}\n'
            f'NIVEL PEDAGÓGICO: {self.pedagogical_level} | ITINERARIO: {self.itinerary_id}\n'
            f'{itin_ctx}\n'
            f'{fatal_note}\n\n'
            f'REGLAS CRÍTICAS DE GENERACIÓN:\n'
            f'1. Los UUID de los ítems son INMUTABLES — devuélvelos exactamente como se reciben.\n'
            f'2. Para DRA-HOLO con supuestos jurídicos: declara required_norms en grading_logic.\n'
            f'3. Para W-LAW-NAV: el repositorio normativo debe incluir las normas requeridas como options.\n'
            f'4. Para RPP-TRAZA: step_matrix completa con weights que sumen 1.0.\n'
            f'5. Todo el contenido en castellano con terminología jurídica/social precisa.\n'
            f'6. Devuelve EXCLUSIVAMENTE el JSON estructurado según ExamSectionSchema — sin texto envolvente.'
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
        Generates the user prompt for atomic social/legal section generation.
        ---
        Genera el prompt de usuario para la generación atómica de sección social/jurídica.
        """
        memory_note = (
            '\nANTI-REPETICIÓN — Supuestos o temas ya evaluados (NO REPETIR): ' +
            ', '.join(generated_item_titles)
        ) if generated_item_titles else ''

        skeleton_note = (
            f'\nESQUELETO DE ÍTEMS (OBLIGATORIO — no modificar los item_id UUID):\n{skeleton_json}\n'
        ) if skeleton_json else ''

        return (
            f'GENERA EL CONTENIDO DE EVALUACIÓN SOCIAL/JURÍDICA PARA LA SIGUIENTE SECCIÓN.\n\n'
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
            f'4. Para DRA-HOLO con supuestos jurídicos: declara required_norms en grading_logic.\n'
            f'5. Para W-LAW-NAV: incluye el repositorio normativo como lista en options.\n'
            f'6. Para RPP-TRAZA: step_matrix completa, weights suman 1.0.\n'
            f'7. Todo el contenido en castellano. Terminología jurídica/técnica precisa.\n'
            f'8. Los supuestos deben ser reales y basados en el material de estudio.\n'
            f'9. Si la sección requiere section_stimulus (caso práctico completo), inclúyelo en el JSON.\n'
            f'10. PROHIBIDO generar supuestos de violencia de género en SUB-SOC-WORK-MED.'
        )
