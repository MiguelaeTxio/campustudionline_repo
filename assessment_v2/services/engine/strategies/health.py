# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/strategies/health.py
"""
Exam strategy for ARCH_HEALTH (Ciencias de la Salud).
Covers all 18 certified sub-archetypes of the Health Sciences branch (v5.9):
  SUB-SAN-MED-CLIN       — Diagnóstico Clínico y Razonamiento (Medicina UGR)
  SUB-SAN-MED-BASIC      — Ciencias Básicas Médicas: Anatomía e Histología
  SUB-SAN-MED-FISIO-GEN  — Fisiología General y Médica (Medicina UGR)
  SUB-SAN-MED-FISIO-NEURO — Fisiología Neurológica (Medicina UGR)
  SUB-SAN-CUID           — Cuidados / Enfermería NANDA (UGR)
  SUB-SAN-ODON           — Odontología (EP Certificada)
  SUB-SAN-FISIO          — Fisioterapia (EP Certificada)
  SUB-SAN-BIOQUIM        — Bioquímica Metabólica (Farmacia UGR)
  SUB-SAN-FARM           — Farmacología I y II (Farmacia UGR)
  SUB-SAN-PSY-DIAG       — Psicopatología del Adulto (Psicología UGR)
  SUB-SAN-PSY-EVAL       — Evaluación Psicológica (UGR)
  SUB-SAN-PSY-MET        — Métodos y Diseños (Psicología UGR)
  SUB-SAN-PSY-STAT       — Descripción y Exploración de Datos (Psicología)
  SUB-SAN-VET-CLIN       — Veterinaria Clínica (UCO)
  SUB-SAN-VET-CIR        — Cirugía Veterinaria (UCO)
  SUB-SAN-NUT-DIET       — Dietética y Nutrición Clínica (UGR)
  SUB-SAN-NUT-BROM       — Bromatología (Nutrición UGR)
  SUB-SAN-NUT-SPUB       — Salud Pública y Alimentación en Colectividades

Complies with V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS,
V06DOC_ARCHETYPES (ECOE model, KILL_SWITCH, ITIN_ROT), V06DOC_LEVELS (v5.9).
---
Estrategia de examen para ARCH_HEALTH (Ciencias de la Salud).
Cubre los 18 subarquetipos certificados de la rama de Ciencias de la Salud (v5.9).
Cumple con V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS,
V06DOC_ARCHETYPES (modelo ECOE, KILL_SWITCH, ITIN_ROT), V06DOC_LEVELS (v5.9).
"""
from decimal import Decimal
from .base import BaseExamStrategy


class HealthStrategy(BaseExamStrategy):
    """
    Strategy for Health Sciences (ARCH_HEALTH).
    Patient safety is the highest priority: CDS-KILL triggers section annulment.
    ITIN_ROT activates the full ECOE protocol with Non-Backtracking.
    All 18 certified sub-archetypes have specific skeletons and motors.
    ---
    Estrategia para Ciencias de la Salud (ARCH_HEALTH).
    La seguridad del paciente es la máxima prioridad: CDS-KILL activa la anulación de sección.
    ITIN_ROT activa el protocolo ECOE completo con Non-Backtracking.
    Los 18 subarquetipos certificados tienen esqueletos y motores específicos.
    """

    # =========================================================================
    # GRADING ENGINE
    # MOTOR DE CALIFICACIÓN
    # Ref: V06DOC_BLOCKS (motores específicos para ARCH_HEALTH)
    # =========================================================================

    def grade_item(self, item, student_input) -> tuple:
        """
        Routes each item to the correct grading motor.
        CDS-KILL has absolute priority — wrong safety answers are always fatal in ITIN_ROT.
        PRM-STRIKE applies standard UGR formula without ITIN_ROT multiplier
        (penalty multipliers are not supported by any certified UGR degree guide).
        ---
        Enruta cada ítem al motor de calificación correcto.
        CDS-KILL tiene prioridad absoluta — las respuestas de seguridad incorrectas
        son siempre fatales en ITIN_ROT.
        PRM-STRIKE aplica la fórmula UGR estándar sin multiplicador ITIN_ROT
        (los multiplicadores de penalización no están respaldados por ninguna guía docente UGR certificada).
        """
        block_type = item.block_type

        if block_type == 'CDS-KILL':
            return self._grade_cds_kill(item, student_input)

        elif block_type == 'PRM-STRIKE':
            # Standard UGR formula — no ITIN_ROT multiplier
            # Fórmula UGR estándar — sin multiplicador ITIN_ROT
            return self._grade_prm_strike(item, student_input)

        elif block_type == 'RBT-CANON':
            return self._grade_rbt_canon(item, student_input)

        elif block_type == 'ILC-CONTEXT':
            # Full AI-evaluated motor (coordinates + clinical reasoning)
            # Motor evaluado completamente por IA (coordenadas + razonamiento clínico)
            return self._grade_ilc_context(item, student_input)

        elif block_type == 'RPP-TRAZA':
            return self._grade_rpp_traza(item, student_input)

        elif block_type == 'DRA-HOLO':
            return self._grade_dra_holo(item, student_input)

        elif block_type == 'MAT-LINK':
            return self._grade_mat_link(item, student_input)

        elif block_type == 'CLO-MULTI':
            return self._grade_clo_multi(item, student_input)

        elif block_type == 'CLO-OPEN':
            return self._grade_clo_open(item, student_input)

        # Fallback / Fallback
        return Decimal('0.0'), {
            'status': 'MOTOR_NOT_IMPLEMENTED',
            'feedback_category': 'FB_CONCEPT',
            'justification': f'Motor {block_type} no implementado para ARCH_HEALTH.'
        }

    # =========================================================================
    # RIGOR OVERRIDE
    # ANULACIÓN DE RIGOR
    # Ref: V06DOC_LEVELS (valores específicos por sub-arquetipo de Salud)
    # =========================================================================

    def _get_grading_params(self) -> dict:
        """
        Overrides the base rigor matrix for specific health sub-archetypes
        where V06DOC_LEVELS declares divergent values.
        Neurology (FISIO-NEURO): increased penalty threshold due to patient safety.
        Veterinary Surgery (VET-CIR): zero tolerance — eliminatory threshold.
        ---
        Anula la matriz de rigor base para subarquetipos de salud específicos
        donde V06DOC_LEVELS declara valores divergentes.
        Neurología (FISIO-NEURO): umbral de penalización aumentado por seguridad del paciente.
        Cirugía Veterinaria (VET-CIR): tolerancia cero — umbral eliminatorio.
        Ref: V06DOC_LEVELS (valores específicos por sub-arquetipo de Salud).
        """
        base = super()._get_grading_params()

        if self.sub_archetype_id == 'SUB-SAN-MED-FISIO-NEURO':
            # Neurological physiology: every question is patient-safety relevant
            # Fisiología neurológica: cada pregunta es relevante para la seguridad del paciente
            base['penalty_threshold'] = 0.0

        elif self.sub_archetype_id == 'SUB-SAN-VET-CIR':
            # Veterinary surgery: eliminatory threshold on all items
            # Cirugía veterinaria: umbral eliminatorio en todos los ítems
            base['penalty_threshold'] = 0.0

        return base

    # =========================================================================
    # EXAM SKELETON — 18 certified sub-archetypes
    # ESQUELETO DE EXAMEN — 18 subarquetipos certificados
    # Ref: V06DOC_SUBARCHETYPES, V06DOC_SUBDIVISIONS, V06DOC_BLOCKS (v5.9)
    # =========================================================================

    def get_exam_skeleton(self) -> list:
        """
        Returns the full structural skeleton for the sub-archetype.
        ITIN_ROT activates the full 5-station ECOE protocol for clinical sub-archetypes.
        ---
        Devuelve el esqueleto estructural completo para el sub-arquetipo.
        ITIN_ROT activa el protocolo ECOE completo de 5 estaciones para subarquetipos clínicos.
        Ref: V06DOC_STRUCTURE (Skeleton-First Protocol), V06DOC_SUBARCHETYPES v5.9.
        """
        sid  = self.sub_archetype_id
        itin = self.itinerary_id

        # Shared task instructions / Instrucciones de tarea compartidas
        I_CLINIC_Q  = (
            'Genera una pregunta de opción múltiple (A/B/C/D) basada en el caso clínico o patología. '
            'Las opciones deben incluir el diagnóstico correcto y 3 distractores clínicamente plausibles.'
        )
        I_IMAGE     = (
            'Genera el stem describiendo una prueba diagnóstica (RX, TC, RM, ECG, espirometría, '
            'histología, etc.) con hallazgos patológicos concretos para que el alumno la interprete. '
            'No incluyas ninguna URL en media_assets: el sistema recupera y verifica una imagen real '
            'por separado, y puede sustituir este enunciado por uno redactado sobre esa imagen concreta. '
            'Proporciona en keywords los términos semiológicos esperados.'
        )
        I_SAFETY    = (
            'Genera un checklist de pasos críticos de seguridad. '
            'El alumno debe confirmar la ejecución de cada paso obligatorio. '
            'Marca kill_switch=True en grading_logic para los pasos cuyo error es eliminatorio.'
        )
        I_TREATMENT = (
            'Genera una pregunta de opción múltiple (A/B/C/D) sobre el plan terapéutico, '
            'farmacológico o rehabilitador adecuado para el caso clínico.'
        )

        # ==============================================================
        # 1. SUB-SAN-MED-CLIN — Diagnóstico Clínico y Razonamiento
        # Full ECOE for ITIN_ROT / Standard 3-phase for others
        # ==============================================================
        if sid == 'SUB-SAN-MED-CLIN':
            if itin == 'ITIN_ROT':
                return [
                    {
                        'subdivision_id': 'SD_ANAMNESIS',
                        'title': 'Estación 1: Anamnesis y Entrevista Clínica',
                        'instructions': 'Realice la anamnesis completa. Identifique el motivo de consulta, antecedentes y sintomatología.',
                        'layout_mode': 'STANDARD',
                        'time_limit': 420,
                        'items': [
                            {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                             'task_instruction': 'Genera 3 preguntas de opción múltiple sobre la orientación correcta de la anamnesis (antecedentes relevantes, síntomas guía, preguntas de alarma).'}
                        ]
                    },
                    {
                        'subdivision_id': 'SD_SYNDROME_BUILD',
                        'title': 'Estación 2: Identificación Sindrómica',
                        'instructions': 'Identifique el síndrome principal y los signos de alarma presentes.',
                        'layout_mode': 'SPLIT_TEXT',
                        'time_limit': 420,
                        'items': [
                            {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                             'task_instruction': I_IMAGE}
                        ]
                    },
                    {
                        'subdivision_id': 'SD_DIFF_DIAGNOSIS',
                        'title': 'Estación 3: Diagnóstico Diferencial',
                        'instructions': 'Establezca el diagnóstico diferencial ordenado por probabilidad.',
                        'layout_mode': 'STANDARD',
                        'time_limit': 420,
                        'items': [
                            {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                             'task_instruction': I_CLINIC_Q}
                        ]
                    },
                    {
                        'subdivision_id': 'SD_CLINICAL_PRIORITY',
                        'title': 'Estación 4: Priorización y Plan Terapéutico',
                        'instructions': 'Establezca el plan de actuación inmediata y el tratamiento definitivo.',
                        'layout_mode': 'STANDARD',
                        'time_limit': 420,
                        'items': [
                            {'block_type': 'CDS-KILL', 'widget_id': 'W-PROC-ACTION', 'weight': 1.0, 'fail_logic': 'FATAL', 'level_requisite': 'MANDATORY',
                             'task_instruction': I_SAFETY},
                            {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                             'task_instruction': I_TREATMENT}
                        ]
                    },
                    {
                        'subdivision_id': 'SD_ECOE_STATION',
                        'title': 'Estación 5: Comunicación y Bioética',
                        'instructions': 'Informe al paciente/familia y gestione el aspecto bioético o legal del caso.',
                        'layout_mode': 'STANDARD',
                        'time_limit': 300,
                        'items': [
                            {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                             'task_instruction': 'Genera un supuesto de comunicación de malas noticias o consentimiento informado. El alumno redacta la información que daría al paciente/familia con empatía y rigor ético.'}
                        ]
                    }
                ]
            else:
                return [
                    {
                        'subdivision_id': 'SD_ANAMNESIS',
                        'title': 'Anamnesis y Síndrome Principal',
                        'instructions': 'Identifique los signos y síntomas guía del caso clínico.',
                        'layout_mode': 'SPLIT_TEXT',
                        'time_limit': 600,
                        'items': [
                            {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                             'task_instruction': I_CLINIC_Q}
                        ]
                    },
                    {
                        'subdivision_id': 'SD_DIFF_DIAGNOSIS',
                        'title': 'Diagnóstico Diferencial e Imagen',
                        'instructions': 'Interprete la prueba diagnóstica y establezca el diagnóstico.',
                        'layout_mode': 'SPLIT_VISUAL',
                        'time_limit': 900,
                        'items': [
                            {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                             'task_instruction': I_IMAGE}
                        ]
                    },
                    {
                        'subdivision_id': 'SD_CLINICAL_PRIORITY',
                        'title': 'Plan Terapéutico y Seguridad',
                        'instructions': 'Establezca el tratamiento y verifique los pasos críticos de seguridad.',
                        'layout_mode': 'STANDARD',
                        'time_limit': 600,
                        'items': [
                            {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                             'task_instruction': I_TREATMENT},
                            {'block_type': 'CDS-KILL', 'widget_id': 'W-PROC-ACTION', 'weight': 1.0, 'fail_logic': 'FATAL', 'level_requisite': 'MANDATORY',
                             'task_instruction': I_SAFETY}
                        ]
                    }
                ]

        # ==============================================================
        # 2. SUB-SAN-MED-BASIC — Ciencias Básicas: Anatomía e Histología
        # ==============================================================
        elif sid == 'SUB-SAN-MED-BASIC':
            return [
                {
                    'subdivision_id': 'SD_ANAT_MACRO',
                    'title': 'Anatomía Macroscópica — Nomenclatura',
                    'instructions': 'Identifique las estructuras anatómicas señaladas y proporcione su nomenclatura TAI.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo una imagen de anatomía macroscópica (disección, '
                             'modelo 3D, esquema) con 5 estructuras señaladas numeradas. '
                             'Solicita al alumno la identificación de cada estructura con su nombre TAI correcto. '
                             'Proporciona en keywords los nombres anatómicos esperados.'
                         )}
                    ]
                },
                {
                    'subdivision_id': 'SD_ANAT_RADIO',
                    'title': 'Anatomía Radiológica — Semiología',
                    'instructions': 'Identifique las estructuras en la imagen radiológica y describa la semiología normal.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo una imagen radiológica normal (RX tórax, '
                             'RM cerebral, ecografía abdominal) con estructuras a identificar. '
                             'El alumno debe identificar las estructuras señaladas y describir '
                             'los parámetros de normalidad. No incluyas ninguna URL en media_assets: '
                             'el sistema recupera y verifica una imagen real por separado.'
                         )}
                    ]
                },
                {
                    'subdivision_id': 'SD_HISTO_MICRO',
                    'title': 'Histología Microscópica — Identificación Tisular',
                    'instructions': 'Identifique el tejido o célula en la preparación microscópica.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 600,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera 4 preguntas de opción múltiple sobre identificación de tejidos, '
                             'células o estructuras subcelulares en imágenes de microscopía óptica '
                             'o electrónica. El stem debe describir la tinción y los rasgos morfológicos visibles.'
                         )}
                    ]
                }
            ]

        # ==============================================================
        # 3. SUB-SAN-MED-FISIO-GEN — Fisiología General y Médica
        # ==============================================================
        elif sid == 'SUB-SAN-MED-FISIO-GEN':
            return [
                {
                    'subdivision_id': 'SD_FISIO_HOMEO',
                    'title': 'Homeostasis y Sistema Nervioso Autónomo',
                    'instructions': 'Analice los mecanismos de homeostasis y respuesta del SNA.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas de opción múltiple sobre mecanismos homeostáticos, SNA (simpático/parasimpático) y regulación hormonal.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_FISIO_CARDIO',
                    'title': 'Fisiología Cardiovascular',
                    'instructions': 'Explique el ciclo cardíaco, gasto cardíaco y regulación de la presión arterial.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de cálculo de gasto cardíaco (GC = FC × VS) '
                             'o presión arterial media con los datos del caso clínico. '
                             'La step_matrix debe incluir: plantear la fórmula, sustituir valores, calcular. '
                             'Incluye una pregunta PRM-STRIKE asociada sobre el significado fisiológico del resultado.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera una pregunta sobre interpretación fisiológica del resultado calculado o sobre mecanismos de regulación cardiovascular.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_FISIO_RESP',
                    'title': 'Fisiología Respiratoria y Espirometría',
                    'instructions': 'Interprete la espirometría y explique los volúmenes y capacidades pulmonares.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo una espirometría con valores patológicos '
                             '(patrón obstructivo, restrictivo o mixto). '
                             'Solicita al alumno: interpretación del patrón, cálculo del índice de Tiffeneau, '
                             'y diagnóstico diferencial. Proporciona en keywords los términos esperados.'
                         )}
                    ]
                }
            ]

        # ==============================================================
        # 4. SUB-SAN-MED-FISIO-NEURO — Fisiología Neurológica
        # ==============================================================
        elif sid == 'SUB-SAN-MED-FISIO-NEURO':
            return [
                {
                    'subdivision_id': 'SD_FISIO_ECG',
                    'title': 'Neurofisiología — Potenciales de Acción',
                    'instructions': 'Analice el potencial de acción y la transmisión sináptica.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera 5 preguntas de opción múltiple sobre potenciales de membrana, '
                             'canales iónicos, sinapsis (excitadoras e inhibidoras) y '
                             'transmisión neuromuscular. Nivel de rigor máximo (SUB-SAN-MED-FISIO-NEURO).'
                         )}
                    ]
                },
                {
                    'subdivision_id': 'SD_FISIO_RENAL',
                    'title': 'Fisiología Renal y Equilibrio Ácido-Base',
                    'instructions': 'Calcule el balance renal e interprete el equilibrio ácido-base.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de equilibrio ácido-base con gasometría arterial. '
                             'La step_matrix debe incluir: identificar pH, PaCO2 y HCO3-, '
                             'determinar el trastorno primario, calcular la compensación esperada, '
                             'y emitir el diagnóstico final. kill_switch=True en el paso de identificación del pH.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera una pregunta sobre la causa más probable del trastorno ácido-base identificado.'}
                    ]
                }
            ]

        # ==============================================================
        # 5. SUB-SAN-CUID — Enfermería y Cuidados NANDA
        # ==============================================================
        elif sid == 'SUB-SAN-CUID':
            return [
                {
                    'subdivision_id': 'SD_CUID_NANDA',
                    'title': 'Diagnóstico NANDA y Plan de Cuidados',
                    'instructions': 'Formule el diagnóstico de enfermería y elabore el plan de cuidados NIC/NOC.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera una viñeta clínica de paciente hospitalizado y 4 preguntas '
                             'sobre priorización de diagnósticos NANDA, '
                             'selección de intervenciones NIC y criterios NOC esperados. '
                             'El caso clínico debe ser section_stimulus.'
                         )},
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Solicita al alumno redactar el plan de cuidados completo: '
                             'diagnóstico NANDA (etiqueta, factores relacionados, características definitorias), '
                             'objetivo NOC con indicador y escala, e intervención NIC con actividades. '
                             'word_count_range: min 200, max 350.'
                         )}
                    ]
                },
                {
                    'subdivision_id': 'SD_CUID_SAFETY',
                    'title': 'Protocolo de Seguridad en Técnicas Enfermeras',
                    'instructions': 'Verifique los pasos críticos de seguridad antes de ejecutar la técnica.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 600,
                    'items': [
                        {'block_type': 'CDS-KILL', 'widget_id': 'W-PROC-ACTION', 'weight': 1.0, 'fail_logic': 'FATAL', 'level_requisite': 'MANDATORY',
                         'task_instruction': I_SAFETY}
                    ]
                }
            ]

        # ==============================================================
        # 6. SUB-SAN-ODON — Odontología (EP Certificada)
        # ==============================================================
        elif sid == 'SUB-SAN-ODON':
            return [
                {
                    'subdivision_id': 'SD_ODON_RADIO',
                    'title': 'Radiología Dental — Ortopantomografía',
                    'instructions': 'Identifique los hallazgos patológicos en la imagen radiológica dental.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Describe una ortopantomografía o radiografía periapical con hallazgos '
                             'patológicos concretos (caries interproximal, lesión periapical, '
                             'agenesia, inclusión dental). El alumno identifica y describe los hallazgos '
                             'con su localización según la nomenclatura FDI.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 3 preguntas de opción múltiple sobre diagnóstico diferencial dental basado en los hallazgos radiológicos descritos.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_ODON_PROC',
                    'title': 'Procedimiento Técnico Odontológico',
                    'instructions': 'Ejecute el protocolo clínico verificando los pasos críticos de seguridad.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 600,
                    'items': [
                        {'block_type': 'CDS-KILL', 'widget_id': 'W-PROC-ACTION', 'weight': 1.0, 'fail_logic': 'FATAL', 'level_requisite': 'MANDATORY',
                         'task_instruction': I_SAFETY}
                    ]
                }
            ]

        # ==============================================================
        # 7. SUB-SAN-FISIO — Fisioterapia (EP Certificada)
        # ==============================================================
        elif sid == 'SUB-SAN-FISIO':
            return [
                {
                    'subdivision_id': 'SD_FISIO_VAL',
                    'title': 'Valoración Funcional',
                    'instructions': 'Determine el grado de afectación funcional y las escalas de valoración aplicables.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera 4 preguntas de opción múltiple sobre valoración funcional: '
                             'escalas de dolor (EVA, NRS), balance articular (goniometría), '
                             'balance muscular (Daniels) y pruebas funcionales específicas.'
                         )}
                    ]
                },
                {
                    'subdivision_id': 'SD_FISIO_PALP',
                    'title': 'Anatomía Palpatoria — Puntos Gatillo',
                    'instructions': 'Localice la estructura anatómica o el punto gatillo en la imagen.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo una zona anatómica con marcadores de puntos '
                             'de referencia óseos y musculares. El alumno debe identificar: '
                             'la estructura señalada, su relevancia clínica y la técnica palpatoria correcta. '
                             'Proporciona en keywords los nombres anatómicos y puntos gatillo esperados.'
                         )}
                    ]
                }
            ]

        # ==============================================================
        # 8. SUB-SAN-BIOQUIM — Bioquímica Metabólica (Farmacia UGR)
        # ==============================================================
        elif sid == 'SUB-SAN-BIOQUIM':
            return [
                {
                    'subdivision_id': 'SD_BIOQUIM_METAB',
                    'title': 'Bioquímica Metabólica — Rutas y Enzimas',
                    'instructions': 'Analice la ruta metabólica e identifique las enzimas reguladoras clave.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas de opción múltiple sobre rutas metabólicas (glucólisis, ciclo de Krebs, beta-oxidación, síntesis de proteínas), enzimas alostéricas y regulación metabólica.'},
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera un problema de cálculo enzimático (Michaelis-Menten, inhibición) o de balance energético de rutas. La step_matrix debe incluir todos los pasos del cálculo.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_BIOQUIM_LAB',
                    'title': 'Prácticas de Laboratorio Bioquímico',
                    'instructions': 'Verifique el protocolo de seguridad y la secuencia de la técnica analítica.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 600,
                    'items': [
                        {'block_type': 'CDS-KILL', 'widget_id': 'W-PROC-ACTION', 'weight': 1.0, 'fail_logic': 'FATAL', 'level_requisite': 'MANDATORY',
                         'task_instruction': I_SAFETY}
                    ]
                }
            ]

        # ==============================================================
        # 9. SUB-SAN-FARM — Farmacología I y II (Farmacia UGR)
        # ==============================================================
        elif sid == 'SUB-SAN-FARM':
            return [
                {
                    'subdivision_id': 'SD_FARM_FUNDA',
                    'title': 'Fundamentos de Farmacología — Mecanismo de Acción',
                    'instructions': 'Identifique el mecanismo de acción del fármaco y su diana terapéutica.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas de opción múltiple sobre mecanismos de acción farmacológica, farmacocinética (ADME), interacciones medicamentosas y efectos adversos.'},
                        {'block_type': 'MAT-LINK', 'widget_id': 'W-MIX-MATCH', 'weight': 0.8, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 6 pares de emparejamiento fármaco→mecanismo de acción o fármaco→indicación terapéutica principal.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_FARM_CLINICA',
                    'title': 'Farmacología Clínica — Selección y Dosificación',
                    'instructions': 'Seleccione el fármaco de elección y calcule la dosis ajustada al caso.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de dosificación farmacológica para un paciente con '
                             'insuficiencia renal o hepática (ajuste de dosis). '
                             'La step_matrix debe incluir: calcular el aclaramiento, ajustar la dosis, '
                             'verificar el intervalo de administración. '
                             'kill_switch=True en el paso de verificación del margen terapéutico.'
                         )}
                    ]
                }
            ]

        # ==============================================================
        # 10. SUB-SAN-PSY-DIAG — Psicopatología del Adulto
        # ==============================================================
        elif sid == 'SUB-SAN-PSY-DIAG':
            return [
                {
                    'subdivision_id': 'SD_PSY_DIAG',
                    'title': 'Diagnóstico DSM-5/CIE-11 — Psicopatología',
                    'instructions': 'Categorice el trastorno mental según los criterios diagnósticos vigentes.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera una viñeta clínica psicopatológica y 5 preguntas de opción múltiple '
                             'sobre: diagnóstico diferencial (DSM-5/CIE-11), criterios diagnósticos, '
                             'especificadores, diagnóstico principal vs. comorbilidad. '
                             'La viñeta debe ser section_stimulus.'
                         )},
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Solicita al alumno la formulación diagnóstica completa: '
                             'diagnóstico principal (con código CIE-11), diagnósticos diferenciales descartados '
                             'y justificación clínica. word_count_range: min 200, max 350.'
                         )}
                    ]
                }
            ]

        # ==============================================================
        # 11. SUB-SAN-PSY-EVAL — Evaluación Psicológica
        # ==============================================================
        elif sid == 'SUB-SAN-PSY-EVAL':
            return [
                {
                    'subdivision_id': 'SD_PSY_EVAL_TECH',
                    'title': 'Técnicas de Evaluación Psicológica',
                    'instructions': 'Seleccione y aplique las técnicas de evaluación psicológica adecuadas al caso.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre selección de instrumentos de evaluación (tests de inteligencia, personalidad, psicopatología), propiedades psicométricas (fiabilidad, validez) y normas de aplicación.'},
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo un perfil de resultados de una batería '
                             'psicológica (MMPI-2, WAIS-IV, MCMI-III, etc.) con puntuaciones T y percentiles. '
                             'Solicita al alumno la interpretación clínica del perfil. '
                             'Proporciona en keywords los descriptores clínicos esperados.'
                         )}
                    ]
                }
            ]

        # ==============================================================
        # 12. SUB-SAN-PSY-MET — Métodos y Diseños de Investigación
        # ==============================================================
        elif sid == 'SUB-SAN-PSY-MET':
            return [
                {
                    'subdivision_id': 'SD_PSY_MET_DESIGN',
                    'title': 'Diseño de Investigación Psicológica',
                    'instructions': 'Evalúe el diseño del estudio e identifique sesgos y amenazas a la validez.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera una descripción de estudio de investigación psicológica y '
                             '5 preguntas sobre: tipo de diseño, variables (dependiente/independiente/extrañas), '
                             'amenazas a la validez interna y externa, y tamaño muestral. '
                             'La descripción del estudio es section_stimulus.'
                         )},
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Solicita al alumno redactar la sección "Método" de un protocolo de investigación '
                             'para un tema psicológico concreto. '
                             'Debe incluir: participantes, diseño, instrumentos y procedimiento. '
                             'word_count_range: min 250, max 400.'
                         )}
                    ]
                }
            ]

        # ==============================================================
        # 13. SUB-SAN-PSY-STAT — Estadística Aplicada a la Psicología
        # ==============================================================
        elif sid == 'SUB-SAN-PSY-STAT':
            return [
                {
                    'subdivision_id': 'SD_PSY_STAT_DATA',
                    'title': 'Descripción y Exploración de Datos Psicológicos',
                    'instructions': 'Analice la distribución de los datos e interprete los estadísticos descriptivos.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo una tabla de estadísticos descriptivos '
                             '(media, mediana, desviación típica, asimetría, curtosis) y un histograma '
                             'de una variable psicológica (puntuación en test, tiempo de reacción). '
                             'Solicita interpretación de la distribución y conclusiones para el análisis.'
                         )},
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de contraste de hipótesis (t de Student, chi-cuadrado, ANOVA). '
                             'La step_matrix debe incluir: plantear H0/H1, seleccionar el estadístico, '
                             'calcular el valor crítico, tomar la decisión e interpretar el resultado.'
                         )}
                    ]
                }
            ]

        # ==============================================================
        # 14. SUB-SAN-VET-CLIN — Veterinaria Clínica (UCO)
        # ==============================================================
        elif sid == 'SUB-SAN-VET-CLIN':
            return [
                {
                    'subdivision_id': 'SD_VET_CLIN',
                    'title': 'Diagnóstico Veterinario — Clínica Animal',
                    'instructions': 'Identifique la patología animal a partir de los signos clínicos presentados.',
                    'layout_mode': 'SPLIT_VISUAL',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo una imagen clínica de un animal '
                             '(lesión dérmica, postura anormal, hallazgo radiológico veterinario) '
                             'con los datos de anamnesis (especie, edad, sintomatología). '
                             'Solicita diagnóstico diferencial y plan diagnóstico. '
                             'Proporciona en keywords las patologías esperadas.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': I_TREATMENT}
                    ]
                }
            ]

        # ==============================================================
        # 15. SUB-SAN-VET-CIR — Cirugía Veterinaria (UCO)
        # ==============================================================
        elif sid == 'SUB-SAN-VET-CIR':
            return [
                {
                    'subdivision_id': 'SD_VET_CIR',
                    'title': 'Cirugía Veterinaria — Protocolo Quirúrgico',
                    'instructions': 'Verifique el protocolo anestésico-quirúrgico y los pasos críticos de seguridad.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas de opción múltiple sobre técnica quirúrgica veterinaria, anestesia loco-regional, manejo del dolor y protocolo perioperatorio.'},
                        {'block_type': 'CDS-KILL', 'widget_id': 'W-PROC-ACTION', 'weight': 1.0, 'fail_logic': 'FATAL', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             I_SAFETY +
                             ' Contexto: cirugía veterinaria (laparotomía, ortopedia). '
                             'Todos los pasos del checklist son kill_switch=True (tolerancia cero).'
                         )}
                    ]
                }
            ]

        # ==============================================================
        # 16. SUB-SAN-NUT-DIET — Dietética y Nutrición Clínica
        # ==============================================================
        elif sid == 'SUB-SAN-NUT-DIET':
            return [
                {
                    'subdivision_id': 'SD_NUT_DISENO',
                    'title': 'Diseño y Evaluación de Dietas',
                    'instructions': 'Diseñe la dieta terapéutica ajustada a los requerimientos del caso.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un caso clínico de paciente (edad, peso, talla, patología) y solicita '
                             'el diseño de la dieta. La step_matrix debe incluir: '
                             'calcular el GET (Harris-Benedict), determinar el reparto calórico por macronutrientes, '
                             'calcular las raciones y verificar el aporte de micronutrientes clave.'
                         )}
                    ]
                },
                {
                    'subdivision_id': 'SD_NUT_VALORACION',
                    'title': 'Valoración del Estado Nutricional',
                    'instructions': 'Interprete los parámetros antropométricos y bioquímicos del estado nutricional.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas de opción múltiple sobre valoración nutricional: interpretación de IMC, pliegues cutáneos, circunferencia muscular del brazo y parámetros bioquímicos (albúmina, prealbúmina, linfocitos).'}
                    ]
                }
            ]

        # ==============================================================
        # 17. SUB-SAN-NUT-BROM — Bromatología (Nutrición UGR)
        # ==============================================================
        elif sid == 'SUB-SAN-NUT-BROM':
            return [
                {
                    'subdivision_id': 'SD_BROM_COMPOSICION',
                    'title': 'Composición y Valor Nutricional de Alimentos',
                    'instructions': 'Analice la composición nutricional y determine el valor energético.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'RPP-TRAZA', 'widget_id': 'W-TECH-CALC', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera un problema de cálculo del valor energético y nutricional '
                             'de un alimento o receta a partir de su composición en 100g. '
                             'La step_matrix debe incluir: calcular kcal de proteínas, grasas e hidratos, '
                             'sumar el total, comparar con la CDR y emitir valoración nutricional.'
                         )},
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 4 preguntas sobre composición de alimentos, reacciones de deterioro (Maillard, oxidación lipídica), conservantes y tecnología alimentaria.'}
                    ]
                },
                {
                    'subdivision_id': 'SD_BROM_ALTERACIONES',
                    'title': 'Alteraciones, Adulteraciones y Calidad Alimentaria',
                    'instructions': 'Identifique las alteraciones y adulteraciones en el alimento propuesto.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': 'Genera 5 preguntas sobre alteraciones físico-químicas y microbiológicas, adulteraciones frecuentes, métodos de detección y normativa de calidad alimentaria (Reglamento CE 178/2002).'}
                    ]
                }
            ]

        # ==============================================================
        # 18. SUB-SAN-NUT-SPUB — Salud Pública y Alimentación en Colectividades
        # ==============================================================
        elif sid == 'SUB-SAN-NUT-SPUB':
            return [
                {
                    'subdivision_id': 'SD_SPUB_EPIDEMIOLOGIA',
                    'title': 'Epidemiología Nutricional y Vigilancia Alimentaria',
                    'instructions': 'Interprete los datos epidemiológicos nutricionales y diseñe la estrategia de vigilancia.',
                    'layout_mode': 'SPLIT_TEXT',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'ILC-CONTEXT', 'widget_id': 'W-CLIN-SCAN', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Genera el stem describiendo datos epidemiológicos nutricionales de una población '
                             '(prevalencia de obesidad, déficit de micronutrientes, encuesta dietética). '
                             'Solicita al alumno interpretación de los indicadores y propuesta de intervención. '
                             'Proporciona en keywords los indicadores epidemiológicos esperados.'
                         )}
                    ]
                },
                {
                    'subdivision_id': 'SD_SPUB_COLECTIVIDADES',
                    'title': 'Gestión de Alimentación en Colectividades',
                    'instructions': 'Diseñe el menú escolar/hospitalario y verifique el cumplimiento APPCC.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 1200,
                    'items': [
                        {'block_type': 'DRA-HOLO', 'widget_id': 'W-HUM-TEXT', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             'Solicita al alumno el diseño de un ciclo de menús semanal para una colectividad '
                             '(escolar, hospitalaria, geriátrica) con justificación nutricional, '
                             'control de alérgenos y puntos críticos APPCC. '
                             'word_count_range: min 300, max 500.'
                         )},
                        {'block_type': 'CDS-KILL', 'widget_id': 'W-PROC-ACTION', 'weight': 1.0, 'fail_logic': 'FATAL', 'level_requisite': 'MANDATORY',
                         'task_instruction': (
                             I_SAFETY +
                             ' Contexto: cocina colectiva — puntos críticos APPCC (temperaturas, '
                             'contaminación cruzada, higiene de manipuladores).'
                         )}
                    ]
                }
            ]

        # ------------------------------------------------------------------
        # FALLBACK: Generic health skeleton
        # FALLBACK: Esqueleto genérico de salud
        # ------------------------------------------------------------------
        else:
            return [
                {
                    'subdivision_id': 'SD_ANAMNESIS',
                    'title': 'Evaluación de Salud General',
                    'instructions': 'Resuelva el caso clínico o sanitario propuesto.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 900,
                    'items': [
                        {'block_type': 'PRM-STRIKE', 'widget_id': 'W-OBJ-STRIKE', 'weight': 1.0, 'fail_logic': 'PENALTY', 'level_requisite': 'MANDATORY',
                         'task_instruction': I_CLINIC_Q}
                    ]
                },
                {
                    'subdivision_id': 'SD_CUID_SAFETY',
                    'title': 'Protocolo y Seguridad',
                    'instructions': 'Verifique el cumplimiento del protocolo de seguridad.',
                    'layout_mode': 'STANDARD',
                    'time_limit': 600,
                    'items': [
                        {'block_type': 'CDS-KILL', 'widget_id': 'W-PROC-ACTION', 'weight': 1.0, 'fail_logic': 'FATAL', 'level_requisite': 'MANDATORY',
                         'task_instruction': I_SAFETY}
                    ]
                }
            ]

    # =========================================================================
    # SYSTEM PROMPT
    # PROMPT DE SISTEMA
    # =========================================================================

    def get_system_prompt(self) -> str:
        """
        Returns the AI system prompt for this health sub-archetype.
        Patient safety protocols are always highlighted.
        ---
        Devuelve el prompt de sistema de la IA para este sub-arquetipo de salud.
        Los protocolos de seguridad del paciente siempre se destacan.
        """
        roles = {
            'SUB-SAN-MED-CLIN':       'Facultativo Especialista (UGR). Foco: Diagnóstico diferencial, razonamiento clínico basado en evidencia, protocolo terapéutico.',
            'SUB-SAN-MED-BASIC':      'Catedrático de Ciencias Básicas Médicas (UGR). Foco: Nomenclatura anatómica TAI, semiología radiológica, identificación histológica.',
            'SUB-SAN-MED-FISIO-GEN':  'Catedrático de Fisiología General (UGR). Foco: Homeostasis, SNA, fisiología cardiovascular, respiratoria y renal.',
            'SUB-SAN-MED-FISIO-NEURO': 'Catedrático de Neurofisiología (UGR). Foco: Potenciales de acción, sinapsis, transmisión neuromuscular. Rigor máximo.',
            'SUB-SAN-CUID':           'Enfermero/a Clínico Especialista (NANDA/NIC/NOC). Foco: Planes de cuidados, seguridad del paciente, protocolos de técnicas.',
            'SUB-SAN-ODON':           'Odontólogo Especialista. Foco: Nomenclatura FDI, radiología dental, técnica clínica y seguridad.',
            'SUB-SAN-FISIO':          'Fisioterapeuta Clínico. Foco: Valoración funcional, escalas de evaluación, anatomía palpatoria.',
            'SUB-SAN-BIOQUIM':        'Catedrático de Bioquímica (Farmacia UGR). Foco: Rutas metabólicas, enzimología, cálculo bioquímico.',
            'SUB-SAN-FARM':           'Catedrático de Farmacología (Farmacia UGR). Foco: Mecanismos de acción, ADME, dosificación clínica.',
            'SUB-SAN-PSY-DIAG':       'Psicólogo Clínico Especialista. Foco: Diagnóstico DSM-5/CIE-11, psicopatología descriptiva, formulación clínica.',
            'SUB-SAN-PSY-EVAL':       'Psicólogo Evaluador. Foco: Instrumentos psicométricos, fiabilidad, validez, interpretación de perfiles.',
            'SUB-SAN-PSY-MET':        'Investigador en Psicología. Foco: Diseños experimentales, validez interna/externa, metodología científica.',
            'SUB-SAN-PSY-STAT':       'Estadístico en Psicología. Foco: Estadística descriptiva, contrastes de hipótesis, pruebas no paramétricas.',
            'SUB-SAN-VET-CLIN':       'Veterinario Clínico (UCO). Foco: Diagnóstico animal, medicina interna veterinaria, zoonosis.',
            'SUB-SAN-VET-CIR':        'Cirujano Veterinario (UCO). Foco: Técnica quirúrgica, anestesia veterinaria, protocolo perioperatorio. Tolerancia CERO en seguridad.',
            'SUB-SAN-NUT-DIET':       'Dietista-Nutricionista Clínico (UGR). Foco: Diseño de dietas, cálculo energético, valoración nutricional.',
            'SUB-SAN-NUT-BROM':       'Bromatólogo (Nutrición UGR). Foco: Composición de alimentos, alteraciones, adulteraciones, normativa de calidad.',
            'SUB-SAN-NUT-SPUB':       'Especialista en Salud Pública Alimentaria. Foco: Epidemiología nutricional, APPCC, gestión de colectividades.'
        }

        base_role = roles.get(self.sub_archetype_id, 'Evaluador de Ciencias de la Salud.')
        safety_rule = ''
        if self.itinerary_id == 'ITIN_ROT':
            safety_rule = (
                '\nPROTOCOLO ECOE ACTIVO (ITIN_ROT): '
                'Tolerancia CERO en pasos de seguridad crítica. '
                'Activa kill_switch=True en todos los ítems CDS-KILL. '
                'El error en cualquier paso de seguridad anula la sección completa.'
            )
        elif self.sub_archetype_id == 'SUB-SAN-VET-CIR':
            safety_rule = (
                '\nCIRUGÍA VETERINARIA — RIGOR QUIRÚRGICO MÁXIMO: '
                'Todos los pasos del checklist CDS-KILL son eliminatorios (kill_switch=True).'
            )

        return (
            f'IDENTIDAD Y ROL: {base_role}\n'
            f'SUB-ARQUETIPO ACTIVO: {self.sub_archetype_id}\n'
            f'NIVEL PEDAGÓGICO: {self.pedagogical_level} | ITINERARIO: {self.itinerary_id}\n'
            f'{safety_rule}\n\n'
            f'REGLAS CRÍTICAS DE GENERACIÓN:\n'
            f'1. Los UUID de los ítems son INMUTABLES — devuélvelos exactamente como se reciben.\n'
            f'2. Para W-CLIN-SCAN NUNCA incluyas una URL en media_assets - el sistema adjunta una imagen real verificada mediante un servicio dedicado.\n'
            f'3. Para CDS-KILL declara kill_switch en grading_logic según la criticidad del paso.\n'
            f'4. gap_solutions DEBE ser una lista de objetos {{"gap_id": "[HUECO_ID_N]", "accepted_answer": "respuesta"}} — una entrada por hueco, nunca un diccionario.\n'
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
        Generates the user prompt for atomic health section generation.
        ---
        Genera el prompt de usuario para la generación atómica de sección de salud.
        """
        memory_note = (
            '\nANTI-REPETICIÓN — Conceptos ya evaluados en este examen (NO REPETIR): ' +
            ', '.join(generated_item_titles)
        ) if generated_item_titles else ''

        skeleton_note = (
            f'\nESQUELETO DE ÍTEMS (OBLIGATORIO — no modificar los item_id UUID):\n{skeleton_json}\n'
        ) if skeleton_json else ''

        return (
            f'GENERA EL CONTENIDO DE EVALUACIÓN CLÍNICA/SANITARIA PARA LA SIGUIENTE SECCIÓN.\n\n'
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
            f'4. Para ítems CDS-KILL: declara kill_switch=True/False según la criticidad clínica del paso.\n'
            f'5. Para ítems ILC-CONTEXT (W-CLIN-SCAN): NUNCA incluyas una URL en media_assets '
            f'- el sistema adjunta una imagen real verificada por separado -, y proporciona '
            f'igualmente los keywords clínicos esperados en grading_logic.keywords.\n'
            f'6. Para ítems RPP-TRAZA: define step_matrix completa con weights que sumen 1.0.\n'
            f'7. Todo el contenido en castellano. Terminología clínica en castellano (con término latino/inglés entre paréntesis cuando sea necesario).\n'
            f'8. Genera contenido clínico real y riguroso basado en el material de estudio — '
            f'sin placeholders ni contenido genérico.\n'
            f'9. Si la sección requiere section_stimulus (caso clínico completo), inclúyelo en el JSON.'
        )
