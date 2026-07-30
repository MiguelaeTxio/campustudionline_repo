# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/science.py
"""
Exam strategy for ARCH_SCI (Ciencias Puras y Experimentales).
Covers all 15 certified sub-archetypes of the Pure Sciences branch (v5.9):
  SUB-SCI-BIO-GEN    — Biología Molecular y Genética (UGR)
  SUB-SCI-BIO-ZOO    — Zoología y Botánica (UGR)
  SUB-SCI-BIO-ECO    — Ecología (UGR)
  SUB-SCI-CHEM-ORG   — Química Orgánica Pura (UGR)
  SUB-SCI-CHEM-INORG — Química Inorgánica Pura (UGR)
  SUB-SCI-PHYS-EM    — Electromagnetismo (Física UGR)
  SUB-SCI-PHYS-QM    — Mecánica Cuántica (Física UGR)
  SUB-SCI-GEOL-MIN   — Mineralogía y Petrología (UGR)
  SUB-SCI-GEOL-STRAT — Estratigrafía (UGR)
  SUB-SCI-GEOL-MAP   — Cartografía Geológica (UGR)
  SUB-SCI-ENV-RES    — Gestión de Residuos y Recursos (UGR)
  SUB-SCI-ENV-CONT   — Contaminación Ambiental (UGR)
  SUB-SCI-DATA-STAT  — Estadística Computacional e Inferencia (UCM GIDIA)
  SUB-SCI-DATA-ML    — Aprendizaje Automático e IA (UCM GIDIA)
  SUB-SCI-DATA-BIG   — Ingeniería de Datos y Big Data (UCM GIDIA)

Complies with V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS,
V06DOC_ARCHETYPES (Methodological model), V06DOC_LEVELS (v5.9).
---
Estrategia de examen para ARCH_SCI (Ciencias Puras y Experimentales).
Cubre los 15 subarquetipos certificados de la rama de Ciencias Puras (v5.9).
Cumple con V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS,
V06DOC_ARCHETYPES (modelo Metodológico), V06DOC_LEVELS (v5.9).
"""
from decimal import Decimal
from .base import BaseExamStrategy


class ScienceStrategy(BaseExamStrategy):
    """
    Strategy for Pure and Experimental Sciences (ARCH_SCI).
    The methodological model combines theoretical foundations (PRM-STRIKE)
    with multi-step procedural resolution (RPP-TRAZA) and data interpretation (ILC-CONTEXT).
    All 15 certified sub-archetypes have specific skeletons and motors.
    ---
    Estrategia para Ciencias Puras y Experimentales (ARCH_SCI).
    El modelo metodológico combina fundamentos teóricos (PRM-STRIKE)
    con resolución procedimental multietapa (RPP-TRAZA) e interpretación de datos (ILC-CONTEXT).
    Los 15 subarquetipos certificados tienen esqueletos y motores específicos.
    """

    # =========================================================================
    # GRADING ENGINE
    # MOTOR DE CALIFICACIÓN
    # Ref: V06DOC_BLOCKS (motores específicos para ARCH_SCI)
    # =========================================================================

    def grade_item(self, item, student_input) -> tuple:
        """
        Routes each item to the correct grading motor based on block_type.
        Science uses the full UGR PRM-STRIKE formula (no penalty overrides).
        RPP-TRAZA uses the base motor with correct logical approach preservation (50%).
        ---
        Enruta cada ítem al motor de calificación correcto basado en block_type.
        Ciencias usa la fórmula PRM-STRIKE UGR completa (sin anulaciones de penalización).
        RPP-TRAZA usa el motor base con preservación del planteamiento lógico correcto (50%).
        """
        block_type = item.block_type

        if block_type == 'PRM-STRIKE':
            return self._grade_prm_strike(item, student_input)

        elif block_type == 'RPP-TRAZA':
            return self._grade_rpp_traza(item, student_input)

        elif block_type == 'ILC-CONTEXT':
            return self._grade_ilc_context(item, student_input)

        elif block_type == 'RBT-CANON':
            return self._grade_rbt_canon(item, student_input)

        elif block_type == 'MAT-LINK':
            return self._grade_mat_link(item, student_input)

        elif block_type == 'CLO-MULTI':
            return self._grade_clo_multi(item, student_input)

        elif block_type == 'DRA-HOLO':
            return self._grade_dra_holo(item, student_input)

        # Fallback / Fallback
        return Decimal('0.0'), {
            'status': 'MOTOR_NOT_IMPLEMENTED',
            'feedback_category': 'FB_CONCEPT',
            'justification': f'Motor {block_type} no implementado para ARCH_SCI.'
        }

    # =========================================================================
    # EXAM SKELETON — 15 certified sub-archetypes
    # ESQUELETO DE EXAMEN — 15 subarquetipos certificados
    # Ref: V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS (v5.9)
    # =========================================================================

    def get_exam_skeleton(self) -> list:
        """
        Returns the full structural skeleton for the sub-archetype.
        Each sub-archetype has specific subdivision sequences per V06DOC_SUBDIVISIONS.
        ITIN_INV activates additional methodological rigor requirements.
        ---
        Devuelve el esqueleto estructural completo para el sub-arquetipo.
        Cada sub-arquetipo tiene secuencias de subdivisiones específicas según V06DOC_SUBDIVISIONS.
        ITIN_INV activa requisitos adicionales de rigor metodológico.
        Ref: V06DOC_STRUCTURE (Skeleton-First Protocol), V06DOC_SUBARCHETYPES v5.9.
        """
        sid  = self.sub_archetype_id
        itin = self.itinerary_id

        # Shared task instructions / Instrucciones de tarea compartidas
        I_THEORY = (
            'Genera 4 preguntas de opción múltiple (A/B/C/D) sobre fundamentos teóricos. '
            'Las opciones deben requerir comprensión conceptual, no solo memorización.'
        )
        I_CALC = (
            'Genera un problema de cálculo procedimental multietapa. '
            'OBLIGATORIO: Define step_matrix completa con weights que sumen 1.0. '
            'Marca como critical=True los pasos cuyo error invalida el resultado.'
        )
        I_DATA = (
            'Genera el stem describiendo datos experimentales, gráficas o tablas '
            'para su interpretación científica. '
            'Proporciona en keywords los términos y conclusiones esperados.'
        )

        # ==============================================================
        # RAMA BIOLOGÍA
        # ==============================================================

        # 1. SUB-SCI-BIO-GEN — Biología Molecular y Genética
        if sid == 'SUB-SCI-BIO-GEN':
            return [
                {
                    'subdivision_id': 'SD_BIO_TEORIA',
                    'title': 'Fundamentos de Biología Molecular y Genética',
                    'instructions': 'Responda a las cuestiones teóricas sobre biología molecular y genética.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas de opción múltiple sobre: estructura del ADN/ARN, replicación, transcripción, traducción, regulación génica y epigenética.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_BIO_GENETIC',
                    'title': 'Genética y Problemas de Herencia',
                    'instructions': 'Resuelva los problemas de genética mendeliana, poblacional o molecular.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un cruce genético (monohíbrido, dihíbrido o ligado al sexo) '
                             'o un problema de genética poblacional (Hardy-Weinberg). '
                             'La step_matrix debe incluir: plantear el cruce/ecuación, '
                             'calcular frecuencias genotípicas, calcular frecuencias fenotípicas, '
                             'verificar el resultado. critical=True en el paso de planteamiento.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 3 preguntas sobre interpretación de resultados genéticos, herencia no mendeliana y mutaciones.'}
                    ]
                }
            ]

        # 2. SUB-SCI-BIO-ZOO — Zoología y Botánica
        elif sid == 'SUB-SCI-BIO-ZOO':
            return [
                {
                    'subdivision_id': 'SD_BIO_TEORIA',
                    'title': 'Sistemática y Taxonomía Biológica',
                    'instructions': 'Identifique los taxones y clasifique los organismos según criterios filogenéticos.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre características taxonómicas de filos animales y divisiones vegetales, nomenclatura binomial, cladística y filogenia.'},
                        {'block_type': 'MAT-LINK', 'widget_id': 'W-MIX-MATCH', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 6 pares de emparejamiento taxón→característica diagnóstica o especie→grupo taxonómico.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_BIO_GENETIC',
                    'title': 'Morfología y Adaptaciones',
                    'instructions': 'Analice las adaptaciones morfológicas y fisiológicas del grupo propuesto.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo una imagen de un organismo o estructura anatómica '
                             '(preparación microscópica, fotografía de campo, dibujo científico). '
                             'El alumno identifica el grupo taxonómico, describe la estructura '
                             'y explica su valor adaptativo. Proporciona keywords esperados.'
                         )}
                    ]
                }
            ]

        # 3. SUB-SCI-BIO-ECO — Ecología
        elif sid == 'SUB-SCI-BIO-ECO':
            return [
                {
                    'subdivision_id': 'SD_BIO_TEORIA',
                    'title': 'Fundamentos de Ecología',
                    'instructions': 'Responda a las cuestiones teóricas sobre estructura y funcionamiento de ecosistemas.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre estructura trófica, ciclos biogeoquímicos, sucesión ecológica, biodiversidad y servicios ecosistémicos.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_BIO_GENETIC',
                    'title': 'Análisis de Datos Ecológicos',
                    'instructions': 'Interprete los datos ecológicos e identifique las dinámicas poblacionales.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de dinámica poblacional: '
                             'modelo logístico (r, K, N), cálculo de densidad de población '
                             'o índice de diversidad (Shannon, Simpson). '
                             'step_matrix: plantear ecuación, sustituir datos, calcular, interpretar.'
                         )},
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': I_DATA}
                    ]
                }
            ]

        # ==============================================================
        # RAMA QUÍMICA
        # ==============================================================

        # 4. SUB-SCI-CHEM-ORG — Química Orgánica Pura
        elif sid == 'SUB-SCI-CHEM-ORG':
            return [
                {
                    'subdivision_id': 'SD_CHEM_TEORIA',
                    'title': 'Fundamentos de Química Orgánica',
                    'instructions': 'Identifique grupos funcionales, nomenclatura y tipos de reacciones.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre nomenclatura IUPAC, grupos funcionales, isomería, estereoquímica (R/S, E/Z) y tipos de mecanismos de reacción.'},
                        {'block_type': 'MAT-LINK', 'widget_id': 'W-MIX-MATCH', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 pares de emparejamiento compuesto→nombre IUPAC o reacción→tipo de mecanismo.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_CHEM_SINTESIS',
                    'title': 'Síntesis y Reactividad Orgánica',
                    'instructions': 'Diseñe la ruta de síntesis y prediga los productos de reacción.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de síntesis orgánica multietapa '
                             '(2-3 pasos desde material de partida hasta producto objetivo). '
                             'step_matrix: para cada paso indicar reactivo, condiciones y producto esperado. '
                             'critical=True en el paso de identificación del mecanismo clave.'
                         )}
                    ]
                }
            ]

        # 5. SUB-SCI-CHEM-INORG — Química Inorgánica Pura
        elif sid == 'SUB-SCI-CHEM-INORG':
            return [
                {
                    'subdivision_id': 'SD_CHEM_TEORIA',
                    'title': 'Fundamentos de Química Inorgánica',
                    'instructions': 'Analice la estructura electrónica, enlace y propiedades de los compuestos.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre tabla periódica (tendencias, propiedades), teoría del enlace (VSEPR, OM), química de coordinación y estado sólido.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_CHEM_SINTESIS',
                    'title': 'Equilibrio Químico y Cálculo Estequiométrico',
                    'instructions': 'Resuelva los problemas de equilibrio y calcule los rendimientos de reacción.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de equilibrio químico (Kc, Kp, desplazamiento) '
                             'o estequiometría con reactivo limitante y rendimiento. '
                             'step_matrix: ajustar la ecuación, plantear la expresión de K, '
                             'calcular concentraciones en el equilibrio, calcular el rendimiento. '
                             'critical=True en el ajuste de la ecuación.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 3 preguntas sobre termodinámica de la reacción (ΔG, ΔH, ΔS) y su relación con la espontaneidad.'}
                    ]
                }
            ]

        # ==============================================================
        # RAMA FÍSICA
        # ==============================================================

        # 6. SUB-SCI-PHYS-EM — Electromagnetismo
        elif sid == 'SUB-SCI-PHYS-EM':
            return [
                {
                    'subdivision_id': 'SD_PHYS_TEORIA',
                    'title': 'Principios de Electromagnetismo',
                    'instructions': 'Analice los fenómenos electromagnéticos y aplique las ecuaciones de Maxwell.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre campos eléctrico y magnético, ley de Gauss, ley de Faraday, ondas electromagnéticas y óptica física.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_PHYS_CALC',
                    'title': 'Resolución Analítica — Electromagnetismo',
                    'instructions': 'Resuelva el problema de electromagnetismo desarrollando la solución paso a paso.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de electromagnetismo (campo eléctrico de distribuciones de carga, '
                             'fuerza sobre cargas en campo magnético, inducción electromagnética). '
                             'step_matrix: identificar la ley aplicable, plantear la integral/ecuación, '
                             'sustituir datos, calcular el resultado, verificar unidades. '
                             'critical=True en la identificación de la ley y el planteamiento.'
                         )}
                    ]
                }
            ]

        # 7. SUB-SCI-PHYS-QM — Mecánica Cuántica
        elif sid == 'SUB-SCI-PHYS-QM':
            return [
                {
                    'subdivision_id': 'SD_PHYS_TEORIA',
                    'title': 'Fundamentos de Mecánica Cuántica',
                    'instructions': 'Analice los principios y postulados de la mecánica cuántica.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre el principio de incertidumbre, función de onda, ecuación de Schrödinger, números cuánticos y espín.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_PHYS_CALC',
                    'title': 'Problemas de Mecánica Cuántica',
                    'instructions': 'Resuelva los problemas cuánticos desarrollando la solución formal.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema cuántico (partícula en una caja, oscilador armónico, '
                             'átomo de hidrógeno, efecto fotoeléctrico). '
                             'step_matrix: plantear la ecuación de Schrödinger o la relación aplicable, '
                             'aplicar las condiciones de contorno, calcular los valores propios, '
                             'interpretar el resultado físico.'
                         )}
                    ]
                }
            ]

        # ==============================================================
        # RAMA GEOLOGÍA
        # ==============================================================

        # 8. SUB-SCI-GEOL-MIN — Mineralogía y Petrología
        elif sid == 'SUB-SCI-GEOL-MIN':
            return [
                {
                    'subdivision_id': 'SD_GEOL_IDENT',
                    'title': 'Identificación Mineralógica y Petrológica',
                    'instructions': 'Identifique el mineral o roca en la muestra o imagen proporcionada.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo una imagen de muestra mineralógica o petrográfica '
                             '(fotografía de mano, sección delgada al microscopio). '
                             'El alumno identifica el mineral/roca, describe sus propiedades diagnósticas '
                             '(color, brillo, exfoliación, dureza, textura) y determina su clasificación. '
                             'Proporciona en keywords el nombre y propiedades esperados.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre clasificación de minerales (silicatos, óxidos, sulfuros), sistemas cristalinos y procesos petrogenéticos.'}
                    ]
                }
            ]

        # 9. SUB-SCI-GEOL-STRAT — Estratigrafía
        elif sid == 'SUB-SCI-GEOL-STRAT':
            return [
                {
                    'subdivision_id': 'SD_GEOL_STRAT',
                    'title': 'Estratigrafía y Lectura de Columnas',
                    'instructions': 'Interprete la columna estratigráfica e identifique las unidades y sus relaciones.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo una columna estratigráfica con diferentes unidades litológicas, '
                             'discordancias y superficies de discontinuidad. '
                             'El alumno debe: identificar las unidades, interpretar las relaciones temporales, '
                             'identificar las discontinuidades y reconstruir la historia geológica. '
                             'Proporciona en keywords los términos estratigráficos esperados.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre principios estratigráficos (superposición, horizontalidad, continuidad lateral, fauna), geocronología y escala de tiempo geológico.'}
                    ]
                }
            ]

        # 10. SUB-SCI-GEOL-MAP — Cartografía Geológica
        elif sid == 'SUB-SCI-GEOL-MAP':
            return [
                {
                    'subdivision_id': 'SD_GEOL_CARTOG',
                    'title': 'Cartografía Geológica e Interpretación de Cortes',
                    'instructions': 'Interprete el mapa geológico y construya el corte geológico.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 2400,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo un mapa geológico simplificado con '
                             'diferentes unidades litológicas, contactos, fallas y estructura tectónica. '
                             'El alumno debe: identificar las estructuras, determinar la edad relativa, '
                             'interpretar los contactos y describir la historia tectónica. '
                             'Proporciona en keywords los términos estructurales y tectónicos esperados.'
                         )},
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de cálculo geométrico sobre el mapa: '
                             'determinar el buzamiento a partir de la regla de la V, '
                             'calcular el espesor de una unidad o la profundidad de un contacto. '
                             'step_matrix: identificar los elementos geométricos, '
                             'aplicar la relación trigonométrica, calcular el resultado.'
                         )}
                    ]
                }
            ]

        # ==============================================================
        # RAMA CIENCIAS AMBIENTALES
        # ==============================================================

        # 11. SUB-SCI-ENV-RES — Gestión de Residuos y Recursos
        elif sid == 'SUB-SCI-ENV-RES':
            return [
                {
                    'subdivision_id': 'SD_ENV_GESTIÓN',
                    'title': 'Gestión de Residuos y Evaluación de Impacto',
                    'instructions': 'Analice el caso de gestión ambiental y proponga las medidas correctoras.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre clasificación de residuos (LRSC 7/2022), jerarquía de gestión (prevención, reutilización, reciclaje), valorización y eliminación.'},
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un caso de evaluación de impacto ambiental (EIA) simplificado '
                             'y solicita al alumno: identificación de impactos, valoración según '
                             'la metodología matricial y propuesta de medidas correctoras. '
                             'word_count_range: min 250, max 400.'
                         )}
                    ]
                }
            ]

        # 12. SUB-SCI-ENV-CONT — Contaminación Ambiental
        elif sid == 'SUB-SCI-ENV-CONT':
            return [
                {
                    'subdivision_id': 'SD_ENV_CONTAM',
                    'title': 'Contaminación — Fuentes, Dispersión y Control',
                    'instructions': 'Analice el contaminante, su dispersión y proponga medidas de control.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre tipos de contaminantes (primarios/secundarios), fuentes de emisión, mecanismos de dispersión en aire/agua/suelo y toxicología ambiental.'},
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de cálculo de índice de contaminación '
                             '(ICA del agua, ICA del aire, concentración de contaminante). '
                             'step_matrix: identificar los parámetros, aplicar la fórmula, '
                             'calcular el índice, clasificar el nivel de contaminación e interpretar.'
                         )}
                    ]
                }
            ]

        # ==============================================================
        # RAMA CIENCIA DE DATOS
        # ==============================================================

        # 13. SUB-SCI-DATA-STAT — Estadística Computacional e Inferencia
        elif sid == 'SUB-SCI-DATA-STAT':
            return [
                {
                    'subdivision_id': 'SD_DATA_PROB',
                    'title': 'Probabilidad y Modelos Estadísticos',
                    'instructions': 'Aplique los modelos de probabilidad y resuelva los problemas de inferencia.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre distribuciones de probabilidad (binomial, Poisson, normal), teorema de Bayes, variables aleatorias y esperanza matemática.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_DATA_INF',
                    'title': 'Inferencia Estadística y Contrastes de Hipótesis',
                    'instructions': 'Realice el contraste de hipótesis y la estimación por intervalos.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de contraste de hipótesis (z, t, chi-cuadrado, F). '
                             'step_matrix: plantear H0/H1, determinar el estadístico de contraste, '
                             'calcular el valor del estadístico, determinar el p-valor o región crítica, '
                             'tomar la decisión e interpretar en términos del problema. '
                             'critical=True en el planteamiento de H0/H1.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 3 preguntas sobre estimación puntual, intervalos de confianza y potencia del contraste.'}
                    ]
                }
            ]

        # 14. SUB-SCI-DATA-ML — Aprendizaje Automático e IA
        elif sid == 'SUB-SCI-DATA-ML':
            return [
                {
                    'subdivision_id': 'SD_ML_SUPER',
                    'title': 'Aprendizaje Supervisado — Clasificación y Regresión',
                    'instructions': 'Seleccione el modelo adecuado y evalúe su rendimiento.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre algoritmos supervisados (regresión lineal/logística, SVM, árboles de decisión, k-NN), métricas de evaluación (accuracy, F1, AUC-ROC) y validación cruzada.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_ML_UNSUPER',
                    'title': 'Aprendizaje No Supervisado y Evaluación de Modelos',
                    'instructions': 'Aplique técnicas de clustering y reducción de dimensionalidad.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de implementación de K-means o PCA: '
                             'dados los datos, ejecutar el algoritmo iterativamente y evaluar. '
                             'step_matrix: inicializar centroides, asignar puntos, recalcular centroides, '
                             'verificar convergencia, interpretar el resultado.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 3 preguntas sobre algoritmos no supervisados (K-means, DBSCAN, PCA, t-SNE) y métricas de evaluación de clustering (silhouette, inercia).'}
                    ]
                }
            ]

        # 15. SUB-SCI-DATA-BIG — Ingeniería de Datos y Big Data
        elif sid == 'SUB-SCI-DATA-BIG':
            return [
                {
                    'subdivision_id': 'SD_BIG_ADQUI',
                    'title': 'Adquisición, Limpieza y Almacenamiento de Datos',
                    'instructions': 'Diseñe el pipeline de adquisición y preprocesamiento de datos.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre fuentes de datos (APIs, scraping, bases de datos), formatos (JSON, Parquet, CSV), técnicas de limpieza (imputación, detección de outliers) y almacenamiento (OLAP, OLTP, Data Lake).'}
                    ]
                },
                {
                    'subdivision_id': 'SD_BIG_PROC',
                    'title': 'Procesamiento Distribuido — Hadoop/Spark/Streaming',
                    'instructions': 'Diseñe la arquitectura de procesamiento y optimice el pipeline.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1800,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre Hadoop (HDFS, MapReduce), Spark (RDD, DataFrame, Spark Streaming), Kafka y procesamiento en tiempo real vs. batch.'},
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un caso de diseño de arquitectura Big Data: '
                             'dados los requisitos del sistema (volumen, velocidad, variedad), '
                             'el alumno propone la arquitectura (Lambda, Kappa o similar) '
                             'con justificación tecnológica. word_count_range: min 250, max 400.'
                         )}
                    ]
                }
            ]

        # ------------------------------------------------------------------
        # FALLBACK: Generic science skeleton
        # FALLBACK: Esqueleto genérico de ciencias
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
                    'title': 'Resolución de Problemas',
                    'instructions': 'Resuelva el problema científico desarrollando la solución paso a paso.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1800,
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
        Returns the AI system prompt for this science sub-archetype.
        Methodological rigor is always highlighted for ITIN_INV.
        ---
        Devuelve el prompt de sistema de la IA para este sub-arquetipo de ciencias.
        El rigor metodológico siempre se destaca para ITIN_INV.
        """
        roles = {
            'SUB-SCI-BIO-GEN':    'Catedrático de Biología Molecular y Genética (UGR). Foco: Dogma central, genética mendeliana y poblacional, regulación génica.',
            'SUB-SCI-BIO-ZOO':    'Catedrático de Zoología y Botánica (UGR). Foco: Sistemática, taxonomía filogenética, morfología comparada.',
            'SUB-SCI-BIO-ECO':    'Catedrático de Ecología (UGR). Foco: Dinámica poblacional, estructura trófica, ciclos biogeoquímicos.',
            'SUB-SCI-CHEM-ORG':   'Catedrático de Química Orgánica (UGR). Foco: Nomenclatura IUPAC, mecanismos de reacción, síntesis multietapa.',
            'SUB-SCI-CHEM-INORG': 'Catedrático de Química Inorgánica (UGR). Foco: Tabla periódica, enlace químico, equilibrio, estequiometría.',
            'SUB-SCI-PHYS-EM':    'Catedrático de Electromagnetismo (UGR). Foco: Ecuaciones de Maxwell, campos, ondas electromagnéticas.',
            'SUB-SCI-PHYS-QM':    'Catedrático de Mecánica Cuántica (UGR). Foco: Ecuación de Schrödinger, principio de incertidumbre, espectroscopía.',
            'SUB-SCI-GEOL-MIN':   'Catedrático de Mineralogía y Petrología (UGR). Foco: Identificación mineralógica, clasificación petrográfica.',
            'SUB-SCI-GEOL-STRAT': 'Catedrático de Estratigrafía (UGR). Foco: Principios estratigráficos, geocronología, columnas estratigráficas.',
            'SUB-SCI-GEOL-MAP':   'Catedrático de Cartografía Geológica (UGR). Foco: Interpretación de mapas, cortes geológicos, tectónica.',
            'SUB-SCI-ENV-RES':    'Especialista en Gestión Ambiental (UGR). Foco: Gestión de residuos, EIA, normativa ambiental.',
            'SUB-SCI-ENV-CONT':   'Especialista en Contaminación Ambiental (UGR). Foco: Fuentes de contaminación, dispersión, control y remediación.',
            'SUB-SCI-DATA-STAT':  'Estadístico Computacional (UCM GIDIA). Foco: Probabilidad, inferencia, contrastes de hipótesis.',
            'SUB-SCI-DATA-ML':    'Científico de Datos / ML Engineer (UCM GIDIA). Foco: Algoritmos supervisados/no supervisados, evaluación de modelos.',
            'SUB-SCI-DATA-BIG':   'Ingeniero de Datos Big Data (UCM GIDIA). Foco: Arquitecturas distribuidas, Spark, Kafka, pipelines de datos.'
        }

        base_role = roles.get(self.sub_archetype_id, 'Científico Senior.')

        itin_ctx = ''
        if self.itinerary_id == 'ITIN_INV':
            itin_ctx = (
                '\nENFOQUE INVESTIGADOR (ITIN_INV): '
                'Rigor metodológico absoluto. '
                'Los problemas deben incluir análisis de error, propagación de incertidumbres '
                'y discusión de la validez del modelo. '
                'Las preguntas teóricas deben requerir demostración formal, no solo aplicación.'
            )
        elif self.itinerary_id == 'ITIN_PROF':
            itin_ctx = (
                '\nENFOQUE PROFESIONAL (ITIN_PROF): '
                'Prioridad en aplicabilidad y normativa. '
                'Los problemas deben estar contextualizados en casos reales del ámbito profesional. '
                'Los cálculos deben seguir los estándares y normativas del sector.'
            )

        return (
            f'IDENTIDAD Y ROL: {base_role}\n'
            f'SUB-ARQUETIPO ACTIVO: {self.sub_archetype_id}\n'
            f'NIVEL PEDAGÓGICO: {self.pedagogical_level} | ITINERARIO: {self.itinerary_id}\n'
            f'{itin_ctx}\n\n'
            f'REGLAS CRÍTICAS DE GENERACIÓN:\n'
            f'1. Los UUID de los ítems son INMUTABLES — devuélvelos exactamente como se reciben.\n'
            f'2. Para RPP-TRAZA: define step_matrix completa con weights que sumen 1.0 y marca critical=True en pasos clave.\n'
            f'3. Para ILC-CONTEXT (W-CLIN-SCAN): NUNCA incluyas una URL en media_assets - el sistema adjunta una imagen real verificada mediante un servicio dedicado, y proporciona los keywords esperados.\n'
            f'4. Para PRM-STRIKE: 4 opciones (A/B/C/D) con distractores científicamente plausibles.\n'
            f'5. Los enunciados (stem) en castellano. Nomenclatura científica internacional entre paréntesis.\n'
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
        Generates the user prompt for atomic science section generation.
        ---
        Genera el prompt de usuario para la generación atómica de sección de ciencias.
        """
        memory_note = (
            '\nANTI-REPETICIÓN — Conceptos o problemas ya evaluados (NO REPETIR): ' +
            ', '.join(generated_item_titles)
        ) if generated_item_titles else ''

        skeleton_note = (
            f'\nESQUELETO DE ÍTEMS (OBLIGATORIO — no modificar los item_id UUID):\n{skeleton_json}\n'
        ) if skeleton_json else ''

        return (
            f'GENERA EL CONTENIDO DE EVALUACIÓN CIENTÍFICA PARA LA SIGUIENTE SECCIÓN.\n\n'
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
            f'4. Para RPP-TRAZA: step_matrix completa, weights suman 1.0, critical marcado correctamente.\n'
            f'5. Para ILC-CONTEXT: NUNCA incluyas una URL en media_assets - el sistema adjunta una imagen real verificada por separado -, y proporciona los keywords científicos esperados.\n'
            f'6. Para PRM-STRIKE: 4 opciones (A/B/C/D), correct_answer es el ID de la opción correcta.\n'
            f'7. Todo el contenido en castellano. Nomenclatura científica entre paréntesis cuando sea necesario.\n'
            f'8. Los problemas deben ser reales y basados en el material de estudio — sin datos inventados.\n'
            f'9. Para step_matrix: los valores esperados deben ser numéricos o expresiones simbólicas precisas.'
        )
