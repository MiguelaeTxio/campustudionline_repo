# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/tech.py
"""
Exam strategy for ARCH_TECH (Ciencias Técnicas e Ingeniería).
Covers all 17 certified sub-archetypes of the Engineering and Architecture branch (v5.9):
  SUB-TEC-SOFT-ALG    — Algoritmia y Estructuras de Datos (ETSIIT-UGR)
  SUB-TEC-SOFT-DS     — Diseño de Software e Ingeniería (ETSIIT-UGR)
  SUB-TEC-SOFT-SE     — Ingeniería del Software (ETSIIT-UGR)
  SUB-TEC-CIVIL-STRUCT — Estructuras de Edificación (ETSICCP-UGR)
  SUB-TEC-CIVIL-CONC  — Hormigón Armado y Pretensado (ETSICCP-UGR)
  SUB-TEC-CIVIL-STEEL — Estructuras Metálicas (ETSICCP-UGR)
  SUB-TEC-INDUS-THERMO — Termodinámica y Motores (EPSC-UCO)
  SUB-TEC-INDUS-TMM   — Teoría de Máquinas y Mecanismos (EPSC-UCO)
  SUB-TEC-INDUS-DEM   — Diseño y Fabricación (UCO)
  SUB-TEC-CHEM-BAL    — Balances de Materia y Energía (IQ-UGR)
  SUB-TEC-CHEM-REACT  — Ingeniería de Reactores Químicos (IQ-UGR)
  SUB-TEC-PROJ-ARCH   — Proyectos de Arquitectura (ETSAG-UGR)
  SUB-TEC-PROJ-URB    — Urbanismo y Ordenación del Territorio (ETSAG-UGR)
  SUB-TEC-CONS-TECH   — Tecnología de la Construcción (ETSIE-UGR)
  SUB-TEC-CONS-MAN    — Gestión y Economía de la Construcción (ETSIE-UGR)
  SUB-TEC-PURE-ANAL   — Análisis Matemático (Grado Matemáticas UGR)
  SUB-TEC-PURE-ALGSTR — Álgebra Estructural y Topología (Matemáticas UGR)

Complies with V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS,
V06DOC_ARCHETYPES (Resolutive model, ITIN_PROF normative enforcement),
V06DOC_LEVELS (v5.9).
---
Estrategia de examen para ARCH_TECH (Ciencias Técnicas e Ingeniería).
Cubre los 17 subarquetipos certificados de la rama de Ingeniería y Arquitectura (v5.9).
Cumple con V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS,
V06DOC_ARCHETYPES (modelo Resolutivo, aplicación normativa ITIN_PROF),
V06DOC_LEVELS (v5.9).
"""
from decimal import Decimal
from .base import BaseExamStrategy


class TechnicalStrategy(BaseExamStrategy):
    """
    Strategy for Technical Sciences and Engineering (ARCH_TECH).
    The resolutive model combines theoretical foundations (PRM-STRIKE, RBT-CANON)
    with multi-step procedural resolution (RPP-TRAZA) and numeric validation.
    ITIN_PROF activates normative enforcement: critical step failure triggers FATAL.
    All 17 certified sub-archetypes have specific skeletons.
    ---
    Estrategia para Ciencias Técnicas e Ingeniería (ARCH_TECH).
    El modelo resolutivo combina fundamentos teóricos (PRM-STRIKE, RBT-CANON)
    con resolución procedimental multietapa (RPP-TRAZA) y validación numérica.
    ITIN_PROF activa la aplicación normativa: el fallo en un paso crítico activa FATAL.
    Los 17 subarquetipos certificados tienen esqueletos específicos.
    """

    # =========================================================================
    # GRADING ENGINE
    # MOTOR DE CALIFICACIÓN
    # Ref: V06DOC_BLOCKS (motores específicos para ARCH_TECH)
    # =========================================================================

    def grade_item(self, item, student_input) -> tuple:
        """
        Routes each item to the correct grading motor.
        RPP-TRAZA uses the base motor with numeric tolerance validation.
        PRM-STRIKE uses the standard UGR formula.
        RBT-CANON delegates to the base motor.
        ---
        Enruta cada ítem al motor de calificación correcto.
        RPP-TRAZA usa el motor base con validación de tolerancia numérica.
        PRM-STRIKE usa la fórmula UGR estándar.
        RBT-CANON delega al motor base.
        """
        block_type = item.block_type

        if block_type == 'RPP-TRAZA':
            return self._grade_rpp_traza(item, student_input)

        elif block_type == 'PRM-STRIKE':
            return self._grade_prm_strike(item, student_input)

        elif block_type == 'RBT-CANON':
            return self._grade_rbt_canon(item, student_input)

        elif block_type == 'CLO-MULTI':
            return self._grade_clo_multi(item, student_input)

        elif block_type == 'MAT-LINK':
            return self._grade_mat_link(item, student_input)

        elif block_type == 'DRA-HOLO':
            return self._grade_dra_holo(item, student_input)

        elif block_type == 'ILC-CONTEXT':
            return self._grade_ilc_context(item, student_input)

        # Fallback / Fallback
        return Decimal('0.0'), {
            'status': 'MOTOR_NOT_IMPLEMENTED',
            'feedback_category': 'FB_CONCEPT',
            'justification': f'Motor {block_type} no implementado para ARCH_TECH.'
        }

    @staticmethod
    def _validate_technical_value(input_val, expected_val) -> bool:
        """
        Validates a student step value against the expected value.
        Numeric comparison uses 1% tolerance (standard engineering precision).
        String comparison is case-insensitive and trimmed.
        Accepts pipe-separated variants in expected_val.
        ---
        Valida el valor de un paso del alumno frente al valor esperado.
        La comparación numérica usa tolerancia del 1% (precisión estándar de ingeniería).
        La comparación de cadenas es insensible a mayúsculas y recortada.
        Acepta variantes separadas por '|' en expected_val.
        """
        # Check pipe-separated variants / Comprobar variantes separadas por '|'
        variants = [v.strip() for v in str(expected_val).split('|')]

        for variant in variants:
            try:
                f_in = float(str(input_val).strip().replace(',', '.'))
                f_ex = float(variant.replace(',', '.'))
                if abs(f_in - f_ex) <= abs(f_ex) * 0.01:
                    return True
            except (ValueError, TypeError):
                if str(input_val).strip().lower() == variant.lower():
                    return True

        return False

    # =========================================================================
    # EXAM SKELETON — 17 certified sub-archetypes
    # ESQUELETO DE EXAMEN — 17 subarquetipos certificados
    # Ref: V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS (v5.9)
    # =========================================================================

    def get_exam_skeleton(self) -> list:
        """
        Returns the full structural skeleton for the sub-archetype.
        ITIN_PROF activates kill_switch=True on critical normative steps.
        ---
        Devuelve el esqueleto estructural completo para el sub-arquetipo.
        ITIN_PROF activa kill_switch=True en pasos normativos críticos.
        Ref: V06DOC_STRUCTURE (Skeleton-First Protocol), V06DOC_SUBARCHETYPES v5.9.
        """
        sid  = self.sub_archetype_id
        itin = self.itinerary_id

        # Shared task instructions / Instrucciones de tarea compartidas
        I_THEORY = (
            'Genera 4 preguntas de opción múltiple (A/B/C/D) sobre fundamentos teóricos técnicos. '
            'Las opciones deben requerir comprensión conceptual y precisión terminológica.'
        )
        I_CALC = (
            'Genera un problema de cálculo técnico multietapa. '
            'OBLIGATORIO: Define step_matrix completa con weights que sumen 1.0. '
            f'{"Marca critical=True en pasos de verificación normativa (ITIN_PROF)." if itin == "ITIN_PROF" else "Marca critical=True en el planteamiento inicial."}'
        )
        I_NORM = (
            'Genera 4 preguntas de opción múltiple sobre normativa técnica aplicable '
            '(CTE, EHE, EC, ISO, UNE). '
            'Las preguntas deben requerir conocimiento de artículos específicos y criterios de cumplimiento.'
        )

        # ==============================================================
        # RAMA INFORMÁTICA / SOFTWARE
        # ==============================================================

        # 1. SUB-TEC-SOFT-ALG — Algoritmia y Estructuras de Datos
        if sid == 'SUB-TEC-SOFT-ALG':
            return [
                {
                    'subdivision_id': 'SD_SOFT_ALG',
                    'title': 'Algoritmia y Complejidad Computacional',
                    'instructions': 'Analice la complejidad del algoritmo e implemente la solución óptima.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre notación asintótica (Big-O, Ω, Θ), análisis de algoritmos de ordenación/búsqueda, estructuras de datos (árboles, grafos, tablas hash) y técnicas algorítmicas (divide y vencerás, programación dinámica, greedy).'},
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de implementación o análisis algorítmico: '
                             'traza de ejecución de un algoritmo (ordenación, árbol, grafo), '
                             'cálculo de complejidad o diseño de estructura de datos. '
                             'step_matrix: cada paso es una iteración del algoritmo con el estado de la estructura. '
                             'critical=True en el paso de identificación del patrón algorítmico.'
                         )}
                    ]
                },
                {
                    'subdivision_id': 'SD_SOFT_DEBUG',
                    'title': 'Depuración, Optimización y Patrones de Diseño',
                    'instructions': 'Identifique el error lógico y proponga la solución optimizada.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un fragmento de pseudocódigo o código con un error lógico o de eficiencia. '
                             'step_matrix: identificar el error, analizar el impacto en la complejidad, '
                             'proponer la corrección, verificar la corrección con un caso de prueba.'
                         )}
                    ]
                }
            ]

        # 2. SUB-TEC-SOFT-DS — Diseño de Software
        elif sid == 'SUB-TEC-SOFT-DS':
            return [
                {
                    'subdivision_id': 'SD_SOFT_DEBUG',
                    'title': 'Patrones de Diseño y Arquitectura de Software',
                    'instructions': 'Identifique el patrón de diseño aplicable y justifique la decisión arquitectónica.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre patrones de diseño GoF (creacionales, estructurales, de comportamiento), arquitecturas (MVC, microservicios, hexagonal) y principios SOLID.'},
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un caso de diseño de software con requisitos funcionales y no funcionales '
                             'y solicita al alumno: selección de patrones de diseño justificada, '
                             'descripción de la arquitectura propuesta y diagrama de componentes en texto. '
                             'word_count_range: min 300, max 500.'
                         )}
                    ]
                }
            ]

        # 3. SUB-TEC-SOFT-SE — Ingeniería del Software
        elif sid == 'SUB-TEC-SOFT-SE':
            return [
                {
                    'subdivision_id': 'SD_SOFT_SE',
                    'title': 'Ingeniería del Software — Requisitos y Arquitectura',
                    'instructions': 'Analice los requisitos del sistema y proponga la arquitectura adecuada.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre elicitación de requisitos (casos de uso, historias de usuario), modelos de proceso (ágil, cascada, espiral), métricas de calidad (cobertura, complejidad ciclomática) y gestión de proyectos software.'},
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera una especificación de sistema y solicita al alumno: '
                             'casos de uso principales (con actores y flujo básico), '
                             'diagrama de clases simplificado en texto, '
                             'plan de pruebas (tipos, estrategia, criterios de aceptación). '
                             'word_count_range: min 350, max 550.'
                         )}
                    ]
                }
            ]

        # ==============================================================
        # RAMA INGENIERÍA CIVIL / ESTRUCTURAS
        # ==============================================================

        # 4. SUB-TEC-CIVIL-STRUCT — Estructuras
        elif sid == 'SUB-TEC-CIVIL-STRUCT':
            return [
                {
                    'subdivision_id': 'SD_CIVIL_CALC',
                    'title': 'Cálculo de Estructuras — Esfuerzos y Dimensionado',
                    'instructions': 'Calcule los esfuerzos en la estructura e identifique la sección crítica.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de cálculo de vigas o pórticos: '
                             'determinación de reacciones (equilibrio estático), '
                             'diagramas de esfuerzos (cortante, flector, axil) y dimensionado de la sección crítica. '
                             'step_matrix: calcular reacciones, trazar el diagrama de cortante, '
                             'trazar el diagrama flector, identificar la sección crítica, dimensionar. '
                             f'{"critical=True en el paso de reacciones (ITIN_PROF)." if itin == "ITIN_PROF" else ""}'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': I_THEORY}
                    ]
                },
                {
                    'subdivision_id': 'SD_CIVIL_NORM',
                    'title': 'Cumplimiento Normativo Estructural',
                    'instructions': 'Verifique el cumplimiento de los estados límite según el CTE y el EC.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': I_NORM}
                    ]
                }
            ]

        # 5. SUB-TEC-CIVIL-CONC — Hormigón Armado
        elif sid == 'SUB-TEC-CIVIL-CONC':
            return [
                {
                    'subdivision_id': 'SD_CIVIL_CALC',
                    'title': 'Hormigón Armado — Cálculo y Armado',
                    'instructions': 'Dimensione la sección de hormigón armado según la EHE.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de dimensionado de viga o pilar de hormigón armado. '
                             'step_matrix: calcular las acciones de cálculo (ELU), determinar el esfuerzo de diseño, '
                             'dimensionar la sección (b×h), calcular la armadura (As), '
                             'verificar la cuantía mínima y máxima (EHE). '
                             f'{"critical=True en la verificación de la cuantía mínima (ITIN_PROF)." if itin == "ITIN_PROF" else ""}'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre materiales del hormigón (resistencias, coeficientes parciales), estados límite (ELU, ELS), armaduras pasivas y pretensado básico.'}
                    ]
                }
            ]

        # 6. SUB-TEC-CIVIL-STEEL — Estructuras Metálicas
        elif sid == 'SUB-TEC-CIVIL-STEEL':
            return [
                {
                    'subdivision_id': 'SD_CIVIL_CALC',
                    'title': 'Estructuras Metálicas — Cálculo de Perfiles',
                    'instructions': 'Dimensione el perfil metálico para la solicitación indicada.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de dimensionado de perfil metálico (IPE, HEB, UPN) a flexión, '
                             'cortante o compresión (pandeo). '
                             'step_matrix: calcular las solicitaciones de diseño, seleccionar el perfil, '
                             'verificar la resistencia a flexión/cortante, verificar el pandeo (λ y χ), '
                             'comprobar la deformación (ELS). '
                             f'{"critical=True en la verificación del pandeo (ITIN_PROF)." if itin == "ITIN_PROF" else ""}'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 3 preguntas sobre clasificación de secciones metálicas, cordones de soldadura, uniones atornilladas y protección frente al fuego (EF-60, EF-90).'}
                    ]
                }
            ]

        # ==============================================================
        # RAMA INGENIERÍA INDUSTRIAL
        # ==============================================================

        # 7. SUB-TEC-INDUS-THERMO — Termodinámica y Motores
        elif sid == 'SUB-TEC-INDUS-THERMO':
            return [
                {
                    'subdivision_id': 'SD_INDUS_TERM',
                    'title': 'Termodinámica — Ciclos de Potencia',
                    'instructions': 'Analice el ciclo termodinámico y calcule su rendimiento.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre leyes de la termodinámica, ciclos ideales (Carnot, Otto, Diesel, Rankine, Brayton), entropía e irreversibilidades.'},
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de cálculo de un ciclo termodinámico dado (Otto, Diesel o Rankine). '
                             'step_matrix: identificar los estados del ciclo, aplicar la 1ª ley en cada proceso, '
                             'calcular el trabajo neto, calcular el rendimiento térmico, '
                             'comparar con el límite de Carnot.'
                         )}
                    ]
                }
            ]

        # 8. SUB-TEC-INDUS-TMM — Teoría de Máquinas
        elif sid == 'SUB-TEC-INDUS-TMM':
            return [
                {
                    'subdivision_id': 'SD_INDUS_TMM',
                    'title': 'Teoría de Máquinas — Cinemática y Dinámica',
                    'instructions': 'Analice el mecanismo e identifique las posiciones, velocidades y aceleraciones.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre grados de libertad (Grübler-Kutzbach), clasificación de mecanismos (cuadrilátero articulado, biela-manivela), análisis cinemático y dinámico, y transmisiones (engranajes, correas).'},
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de análisis cinemático de un mecanismo articulado. '
                             'step_matrix: calcular los grados de libertad, determinar la posición, '
                             'calcular las velocidades (método vectorial o gráfico), '
                             'calcular las aceleraciones, verificar el equilibrio dinámico.'
                         )}
                    ]
                }
            ]

        # 9. SUB-TEC-INDUS-DEM — Diseño y Fabricación
        elif sid == 'SUB-TEC-INDUS-DEM':
            return [
                {
                    'subdivision_id': 'SD_CIVIL_NORM',
                    'title': 'Diseño y Fabricación — Metrología y Expresión Gráfica',
                    'instructions': 'Interprete el plano técnico y determine las tolerancias dimensionales.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo un plano técnico de pieza mecánica '
                             'con cotas, tolerancias dimensionales (ISO) y acabados superficiales. '
                             'El alumno debe: interpretar las tolerancias (ajuste H7/g6, etc.), '
                             'calcular las dimensiones máxima y mínima, '
                             'determinar el tipo de ajuste (apriete, deslizante, indeterminado). '
                             'Proporciona en keywords los términos de metrología esperados.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre procesos de fabricación (arranque de viruta, moldeo, conformado), materiales de ingeniería (aceros, aluminio, polímeros) y control de calidad (Cpk, SPC).'}
                    ]
                }
            ]

        # ==============================================================
        # RAMA INGENIERÍA QUÍMICA
        # ==============================================================

        # 10. SUB-TEC-CHEM-BAL — Balances de Materia y Energía
        elif sid == 'SUB-TEC-CHEM-BAL':
            return [
                {
                    'subdivision_id': 'SD_CHEM_BAL',
                    'title': 'Balances de Materia y Energía en Procesos Químicos',
                    'instructions': 'Realice los balances de materia y energía del proceso propuesto.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un proceso químico con múltiples corrientes (alimentación, producto, purga). '
                             'step_matrix: dibujar el diagrama de flujo del proceso, '
                             'plantear los balances globales de materia (base de cálculo), '
                             'resolver el sistema de ecuaciones, '
                             'aplicar el balance de energía (entalpías de mezcla, de reacción), '
                             'calcular la eficiencia energética del proceso.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 3 preguntas sobre operaciones unitarias (destilación, absorción, extracción), grados de libertad del proceso y conversión, rendimiento y selectividad.'}
                    ]
                }
            ]

        # 11. SUB-TEC-CHEM-REACT — Ingeniería de Reactores
        elif sid == 'SUB-TEC-CHEM-REACT':
            return [
                {
                    'subdivision_id': 'SD_CHEM_REACT',
                    'title': 'Diseño de Reactores y Cinética Química',
                    'instructions': 'Diseñe el reactor y calcule su volumen para la conversión requerida.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de diseño de reactor (CSTR, PFR o batch). '
                             'step_matrix: plantear la ecuación de diseño del reactor, '
                             'expresar la velocidad de reacción (cinética), '
                             'integrar o resolver el sistema de ecuaciones algebraicas, '
                             'calcular el volumen del reactor para X requerida, '
                             'verificar la temperatura de operación (isotérmico/adiabático).'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre tipos de reactores (CSTR, PFR, batch, semi-batch), modelos cinéticos (Arrhenius, Langmuir-Hinshelwood) y criterios de selección del reactor.'}
                    ]
                }
            ]

        # ==============================================================
        # RAMA ARQUITECTURA Y URBANISMO
        # ==============================================================

        # 12. SUB-TEC-PROJ-ARCH — Proyectos de Arquitectura
        elif sid == 'SUB-TEC-PROJ-ARCH':
            return [
                {
                    'subdivision_id': 'SD_ARCH_PROJ',
                    'title': 'Proyecto Arquitectónico — Composición y Programa',
                    'instructions': 'Analice el programa funcional y justifique la solución compositiva.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 3600,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre teoría de la arquitectura (composición, proporción, escala), tipologías arquitectónicas, historia de la arquitectura contemporánea y normativa urbanística básica.'},
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un encargo arquitectónico con programa funcional, '
                             'condicionantes del solar y normativa urbanística. '
                             'El alumno redacta la memoria descriptiva del proyecto: '
                             'análisis del programa, concepto generador, solución formal y funcional, '
                             'sistemas constructivos propuestos y adecuación normativa. '
                             'word_count_range: min 400, max 650.'
                         )}
                    ]
                }
            ]

        # 13. SUB-TEC-PROJ-URB — Urbanismo
        elif sid == 'SUB-TEC-PROJ-URB':
            return [
                {
                    'subdivision_id': 'SD_URB_PLAN',
                    'title': 'Planeamiento Urbanístico y Ordenación del Territorio',
                    'instructions': 'Analice el planeamiento vigente y proponga la ordenación adecuada.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo un plano de ordenación urbana '
                             'con calificación del suelo, alineaciones, retranqueos y parámetros urbanísticos. '
                             'El alumno interpreta la normativa gráfica, calcula aprovechamientos '
                             '(edificabilidad, ocupación, densidad) y propone la ordenación de un ámbito concreto. '
                             'Proporciona en keywords los parámetros urbanísticos esperados.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre instrumentos de planeamiento (PGOU, Plan Parcial, Plan Especial), clasificación del suelo (urbano, urbanizable, no urbanizable) y normativa urbanística autonómica.'}
                    ]
                }
            ]

        # ==============================================================
        # RAMA EDIFICACIÓN / CONSTRUCCIÓN
        # ==============================================================

        # 14. SUB-TEC-CONS-TECH — Tecnología de la Construcción
        elif sid == 'SUB-TEC-CONS-TECH':
            return [
                {
                    'subdivision_id': 'SD_CONS_TECH',
                    'title': 'Sistemas Constructivos y Detalle Técnico',
                    'instructions': 'Identifique el sistema constructivo y elabore el detalle técnico.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo un detalle constructivo '
                             '(encuentro de forjado y fachada, cubierta plana, solera, '
                             'partición interior, aislamiento acústico/térmico). '
                             'El alumno identifica los materiales, describe la secuencia de ejecución '
                             'y verifica el cumplimiento del CTE (DB-HE, DB-HR, DB-HS). '
                             'Proporciona en keywords los materiales y parámetros técnicos esperados.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre sistemas de cimentación, cerramientos, cubiertas, aislamientos y revestimientos según el CTE.'}
                    ]
                }
            ]

        # 15. SUB-TEC-CONS-MAN — Gestión de Obra
        elif sid == 'SUB-TEC-CONS-MAN':
            return [
                {
                    'subdivision_id': 'SD_CONS_MAN',
                    'title': 'Gestión de Obra — Planificación y Seguridad',
                    'instructions': 'Planifique la obra y elabore el plan de seguridad y salud.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de planificación de obra: '
                             'dada la lista de actividades con duraciones y precedencias, '
                             'el alumno elabora el diagrama de Gantt o PERT/CPM. '
                             'step_matrix: ordenar las actividades, calcular los tiempos early/late, '
                             'identificar la ruta crítica, determinar las holguras.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera 4 preguntas sobre seguridad y salud en construcción '
                             '(RD 1627/1997, coordinación de seguridad, EPI, señalización), '
                             'control de calidad de obra y gestión de residuos de construcción (RD 105/2008).'
                             f'{"Las preguntas deben incluir artículos específicos del RD (ITIN_PROF)." if itin == "ITIN_PROF" else ""}'
                         )}
                    ]
                }
            ]

        # ==============================================================
        # RAMA MATEMÁTICAS PURAS
        # ==============================================================

        # 16. SUB-TEC-PURE-ANAL — Análisis Matemático
        elif sid == 'SUB-TEC-PURE-ANAL':
            return [
                {
                    'subdivision_id': 'SD_MATH_PROOF',
                    'title': 'Demostración Matemática — Análisis',
                    'instructions': 'Demuestre formalmente el resultado matemático propuesto.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'RBT-CANON', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas de precisión terminológica sobre definiciones de análisis (límite, continuidad, diferenciabilidad, convergencia, compacidad).'},
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de demostración formal en análisis: '
                             'demostración del teorema del valor medio, de la regla de L\'Hôpital, '
                             'o de convergencia de una serie. '
                             'step_matrix: enunciar las hipótesis, justificar cada paso lógico '
                             'con el teorema o axioma que lo sustenta, '
                             'concluir formalmente. critical=True en el paso inicial de hipótesis.'
                         )}
                    ]
                },
                {
                    'subdivision_id': 'SD_MATH_PROB',
                    'title': 'Resolución de Problemas — Análisis',
                    'instructions': 'Resuelva el problema de análisis matemático justificando cada paso.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de cálculo en análisis matemático: '
                             'integral impropia, serie de potencias, ecuación diferencial ordinaria '
                             'o extremos de funciones de varias variables. '
                             'step_matrix: identificar el tipo de problema, aplicar el método adecuado, '
                             'realizar los cálculos intermedios, verificar el resultado.'
                         )}
                    ]
                }
            ]

        # 17. SUB-TEC-PURE-ALGSTR — Álgebra Estructural y Topología
        elif sid == 'SUB-TEC-PURE-ALGSTR':
            return [
                {
                    'subdivision_id': 'SD_MATH_PROOF',
                    'title': 'Demostración — Álgebra y Topología',
                    'instructions': 'Demuestre la propiedad algebraica o topológica propuesta.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'RBT-CANON', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas de precisión terminológica sobre definiciones de álgebra abstracta (grupo, anillo, cuerpo, espacio vectorial, homomorfismo) y topología (topología, base, compacidad, conexidad).'},
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de demostración en álgebra: '
                             'verificar que una estructura es un grupo/anillo/cuerpo, '
                             'demostrar un isomorfismo, o probar que un subconjunto es cerrado. '
                             'step_matrix: verificar los axiomas uno a uno, '
                             'construir el morfismo si procede, verificar la biyectividad.'
                         )}
                    ]
                },
                {
                    'subdivision_id': 'SD_MATH_PROB',
                    'title': 'Resolución de Problemas — Álgebra',
                    'instructions': 'Resuelva el problema algebraico justificando la estructura.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de álgebra estructural: '
                             'cálculo en grupos cociente, teorema de Sylow, '
                             'factorización en dominios de factorización única, '
                             'o espacios topológicos cociente. '
                             'step_matrix: identificar la estructura, aplicar el teorema adecuado, '
                             'realizar los cálculos, verificar las propiedades.'
                         )}
                    ]
                }
            ]

        # ------------------------------------------------------------------
        # FALLBACK: Generic technical skeleton
        # FALLBACK: Esqueleto genérico de ingeniería
        # ------------------------------------------------------------------
        else:
            return [
                {
                    'subdivision_id': 'SD_THEO',
                    'title': 'Fundamentos Teóricos',
                    'instructions': 'Responda a las cuestiones teóricas sobre el material de estudio.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': I_THEORY}
                    ]
                },
                {
                    'subdivision_id': 'SD_CALC',
                    'title': 'Resolución Técnica',
                    'instructions': 'Resuelva el problema técnico desarrollando la solución paso a paso.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': I_CALC}
                    ]
                }
            ]

    # =========================================================================
    # SYSTEM PROMPT
    # PROMPT DE SISTEMA
    # =========================================================================

    def get_system_prompt(self) -> str:
        """
        Returns the AI system prompt for this engineering sub-archetype.
        ITIN_PROF always highlights normative enforcement.
        ---
        Devuelve el prompt de sistema de la IA para este sub-arquetipo de ingeniería.
        ITIN_PROF siempre destaca la aplicación normativa.
        """
        roles = {
            'SUB-TEC-SOFT-ALG':    'Arquitecto/a de Software Senior (ETSIIT-UGR). Foco: Algoritmia, complejidad computacional, estructuras de datos.',
            'SUB-TEC-SOFT-DS':     'Ingeniero/a de Software — Diseño de Sistemas (ETSIIT-UGR). Foco: Patrones de diseño GoF, SOLID, arquitecturas software.',
            'SUB-TEC-SOFT-SE':     'Ingeniero/a de Software — Proceso (ETSIIT-UGR). Foco: Requisitos, metodologías ágiles, calidad del software.',
            'SUB-TEC-CIVIL-STRUCT':'Ingeniero/a de Estructuras (ETSICCP-UGR). Foco: Cálculo estructural, EC/CTE, estados límite.',
            'SUB-TEC-CIVIL-CONC':  'Especialista en Hormigón (ETSICCP-UGR). Foco: EHE-08, dimensionado de secciones, armaduras.',
            'SUB-TEC-CIVIL-STEEL': 'Especialista en Estructuras Metálicas (ETSICCP-UGR). Foco: EC-3, perfiles, pandeo, uniones.',
            'SUB-TEC-INDUS-THERMO':'Ingeniero/a Industrial — Termodinámica (EPSC-UCO). Foco: Ciclos de potencia, eficiencia energética.',
            'SUB-TEC-INDUS-TMM':   'Ingeniero/a Industrial — TMM (EPSC-UCO). Foco: Cinemática, dinámica de mecanismos, transmisiones.',
            'SUB-TEC-INDUS-DEM':   'Ingeniero/a Industrial — Fabricación (UCO). Foco: Metrología, tolerancias ISO, procesos de fabricación.',
            'SUB-TEC-CHEM-BAL':    'Ingeniero/a Químico/a — Procesos (IQ-UGR). Foco: Balances de materia y energía, operaciones unitarias.',
            'SUB-TEC-CHEM-REACT':  'Ingeniero/a Químico/a — Reactores (IQ-UGR). Foco: Cinética química, diseño de reactores CSTR/PFR.',
            'SUB-TEC-PROJ-ARCH':   'Arquitecto/a Proyectista (ETSAG-UGR). Foco: Composición arquitectónica, memoria descriptiva, normativa.',
            'SUB-TEC-PROJ-URB':    'Urbanista (ETSAG-UGR). Foco: Planeamiento urbanístico, aprovechamientos, normativa autonómica.',
            'SUB-TEC-CONS-TECH':   'Arquitecto/a Técnico/a — Tecnología (ETSIE-UGR). Foco: Sistemas constructivos, CTE, detalles técnicos.',
            'SUB-TEC-CONS-MAN':    'Arquitecto/a Técnico/a — Gestión (ETSIE-UGR). Foco: Planificación de obra, seguridad (RD 1627/1997), gestión.',
            'SUB-TEC-PURE-ANAL':   'Catedrático/a de Análisis Matemático (UGR). Foco: Rigor deductivo, demostraciones, análisis real y complejo.',
            'SUB-TEC-PURE-ALGSTR': 'Catedrático/a de Álgebra Abstracta y Topología (UGR). Foco: Estructuras algebraicas, topología general, demostraciones.'
        }

        base_role = roles.get(self.sub_archetype_id, 'Catedrático/a de Ingeniería.')

        itin_ctx = ''
        if self.itinerary_id == 'ITIN_PROF':
            itin_ctx = (
                '\nENFOQUE PROFESIONAL (ITIN_PROF): '
                'Cumplimiento estricto de la reglamentación técnica vigente. '
                'Marca critical=True en todos los pasos de verificación normativa de la step_matrix. '
                'Los errores en cumplimiento normativo son eliminatorios.'
            )
        elif self.itinerary_id == 'ITIN_INV':
            itin_ctx = (
                '\nENFOQUE INVESTIGADOR (ITIN_INV): '
                'Rigor formal absoluto. '
                'Los problemas deben incluir análisis de error, incertidumbre o propagación. '
                'Las demostraciones matemáticas deben ser completas y rigorosas.'
            )

        return (
            f'IDENTIDAD Y ROL: {base_role}\n'
            f'SUB-ARQUETIPO ACTIVO: {self.sub_archetype_id}\n'
            f'NIVEL PEDAGÓGICO: {self.pedagogical_level} | ITINERARIO: {self.itinerary_id}\n'
            f'{itin_ctx}\n\n'
            f'REGLAS CRÍTICAS DE GENERACIÓN:\n'
            f'1. Los UUID de los ítems son INMUTABLES — devuélvelos exactamente como se reciben.\n'
            f'2. Para RPP-TRAZA: step_matrix completa con weights que sumen 1.0. '
            f'Los valores esperados deben ser numéricos precisos o expresiones simbólicas inequívocas.\n'
            f'3. Para RBT-CANON: correct_answer con los términos exactos esperados, variantes separadas por |.\n'
            f'4. Para ILC-CONTEXT (W-CLIN-SCAN): URL de imagen técnica en media_assets y keywords esperados.\n'
            f'5. Los enunciados (stem) en castellano. Nomenclatura técnica normalizada entre paréntesis.\n'
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
        Generates the user prompt for atomic engineering section generation.
        ---
        Genera el prompt de usuario para la generación atómica de sección de ingeniería.
        """
        memory_note = (
            '\nANTI-REPETICIÓN — Problemas o conceptos ya evaluados (NO REPETIR): ' +
            ', '.join(generated_item_titles)
        ) if generated_item_titles else ''

        skeleton_note = (
            f'\nESQUELETO DE ÍTEMS (OBLIGATORIO — no modificar los item_id UUID):\n{skeleton_json}\n'
        ) if skeleton_json else ''

        return (
            f'GENERA EL CONTENIDO DE EVALUACIÓN TÉCNICA PARA LA SIGUIENTE SECCIÓN.\n\n'
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
            f'4. Para RPP-TRAZA: step_matrix con weights que sumen 1.0. '
            f'Los valores numéricos deben ser precisos (no "≈" sino el valor exacto).\n'
            f'5. Para PRM-STRIKE: 4 opciones (A/B/C/D), correct_answer es el ID de la opción correcta.\n'
            f'6. Para RBT-CANON: correct_answer con el término exacto, variantes aceptables separadas por |.\n'
            f'7. Todo el contenido en castellano. Nomenclatura técnica normalizada.\n'
            f'8. Los problemas deben ser reales y basados en el material de estudio.\n'
            f'9. Si la sección requiere section_stimulus (plano, tabla de datos), inclúyelo en el JSON.'
        )
