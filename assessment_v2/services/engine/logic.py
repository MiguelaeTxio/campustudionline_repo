# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/logic.py
"""
Academic deduction and grading orchestration for the Hito 6 assessment engine.

AcademicDeductor  — Hybrid protocol (AI + Python) for subject classification.
GradingOrchestrator — Submission grading with kill-switch, gating and reporting.

Complies with V06DOC_LOGIC_MAPPING V1.3, V06DOC_BLOCKS, V06DOC_ARCHETYPES,
V06DOC_LEVELS, V06DOC_METADATA, V06DOC_TEMPLATES (v5.9 — 2026-05-16).
---
Deducción académica y orquestación de calificación para el motor de evaluación del Hito 6.

AcademicDeductor    — Protocolo híbrido (IA + Python) para clasificación de asignaturas.
GradingOrchestrator — Calificación de entregas con kill-switch, gating e informes.

Cumple con V06DOC_LOGIC_MAPPING V1.3, V06DOC_BLOCKS, V06DOC_ARCHETYPES,
V06DOC_LEVELS, V06DOC_METADATA, V06DOC_TEMPLATES (v5.9 — 2026-05-16).
"""
import re
import logging
from decimal import Decimal
from django.utils import timezone
from django.utils.translation import gettext as _
from academic_structure.models import Subject
from orchestrator.models import AutomationSettings
from core.services.gemini_service import classify_subject_identity, AIServiceCriticalError

logger = logging.getLogger(__name__)


# ==============================================================================
# SECCIÓN 1: DEDUCTOR ACADÉMICO HÍBRIDO
# Academic deductor — Phase 1 (AI identity) + Phase 2 (Python parameters)
# Ref: V06DOC_LOGIC_MAPPING V1.3
# ==============================================================================

class AcademicDeductor:
    """
    Hybrid service for academic parameter deduction.
    Phase 1 — Cognitive Identity: resolved by Gemini AI classifier.
    Phase 2 — Deterministic Parameters: itinerary, level, immersion mode via Python rules.
    Both phases comply strictly with V06DOC_LOGIC_MAPPING V1.3.
    ---
    Servicio híbrido de deducción de parámetros académicos.
    Fase 1 — Identidad Cognitiva: resuelta por el clasificador IA Gemini.
    Fase 2 — Parámetros Deterministas: itinerario, nivel, modo de inmersión por reglas Python.
    Ambas fases cumplen estrictamente con V06DOC_LOGIC_MAPPING V1.3.
    """

    # Valid archetype IDs — mirrors Exam.Archetype TextChoices
    # IDs de arquetipo válidos — espejo de Exam.Archetype TextChoices
    VALID_ARCHETYPES = frozenset([
        'ARCH_LANG', 'ARCH_HEALTH', 'ARCH_TECH',
        'ARCH_SOC',  'ARCH_HUM',    'ARCH_SCI'
    ])

    @staticmethod
    def deduce_itinerary(subject, context_title=None) -> str:
        """
        Phase 2 — Deduces the ITIN_ID from branch keywords and subject type.
        Priority order: explicit name detection → branch mapping → subject_type fallback.
        ---
        Fase 2 — Deduce el ITIN_ID a partir de palabras clave de la rama y tipo de asignatura.
        Orden de prioridad: detección explícita en nombre → mapeo de rama → fallback por subject_type.
        Ref: V06DOC_LOGIC_MAPPING V1.3 Sección 2 (Parámetros Deterministas).
        """
        name        = (context_title or subject.name).lower()
        branch_name = subject.academic_year.degree.branch.name.lower()

        # 1. Explicit name detection / Detección explícita en el nombre
        if re.search(r'\bmaior\b', name):
            return 'ITIN_MAI'
        if re.search(r'\bminor\b', name):
            return 'ITIN_MIN'

        # 2. Branch keyword mapping / Mapeo por palabra clave de rama
        # Health/Clinical sciences → Rotatorio / Ciencias de la Salud/Clínicas → Rotatorio
        if any(k in branch_name for k in (
            'salud', 'medicina', 'enfermería', 'enfermeria',
            'veterinaria', 'farmacia', 'fisioterapia', 'odontología', 'odontologia',
            'nutrición', 'nutricion', 'psicología', 'psicologia'
        )):
            return 'ITIN_ROT'

        # Engineering/Architecture → Professional / Ingeniería/Arquitectura → Profesional
        if any(k in branch_name for k in (
            'ingeniería', 'ingenieria', 'técnica', 'tecnica',
            'arquitectura', 'edificación', 'edificacion', 'informática', 'informatica'
        )):
            return 'ITIN_PROF'

        # Teaching/Education → Didactic / Docencia/Educación → Didáctico
        if any(k in branch_name for k in (
            'educación', 'educacion', 'magisterio', 'didáctica', 'didactica',
            'pedagogía', 'pedagogia', 'docent'
        )):
            return 'ITIN_DOC'

        # Research → Investigator / Investigación → Investigador
        if any(k in branch_name for k in ('investigac', 'doctoral', 'posgrado')):
            return 'ITIN_INV'

        # 3. Subject type fallback / Fallback por tipo de asignatura
        if subject.subject_type in (Subject.SubjectType.CORE, Subject.SubjectType.MANDATORY):
            return 'ITIN_MAI'

        return 'ITIN_MIN'

    @staticmethod
    def deduce_level(subject, context_title=None) -> str:
        """
        Phase 2 — Deduces the LVL_ID (Pedagogical Level) from name and academic year.
        Priority: semantic detection in name → year-based fallback.
        ---
        Fase 2 — Deduce el LVL_ID (Nivel Pedagógico) desde el nombre y el año académico.
        Prioridad: detección semántica en nombre → fallback por año.
        Ref: V06DOC_LOGIC_MAPPING V1.3 Sección 2, V06DOC_LEVELS Sección 1.
        """
        name = (context_title or subject.name).lower()
        year = subject.academic_year.year if subject.academic_year else 1

        # Semantic detection including Roman numerals / Detección semántica incluyendo números romanos
        if re.search(r'(avanzado|superior|c1|c2|nivel\s+iii|\biii\b|\biv\b|máster|master|postgrado)', name):
            return 'LVL_C'
        if re.search(r'(intermedio|b1|b2|nivel\s+ii|\bii\b)', name):
            return 'LVL_B'
        if re.search(r'(inicial|básico|basico|a1|a2|intro|iniciación|iniciacion|nivel\s+i|\bi\b)', name):
            return 'LVL_A'

        # Year-based fallback / Fallback por año académico
        if year <= 2:
            return 'LVL_A'
        if year == 3:
            return 'LVL_B'

        return 'LVL_C'

    @staticmethod
    def deduce_immersion_mode(archetype_id, itinerary_id, pedagogical_level) -> str:
        """
        Phase 2 — Deduces the immersion mode for ARCH_LANG exams.
        Non-language archetypes always return VEHICULAR.
        ---
        Fase 2 — Deduce el modo de inmersión para exámenes ARCH_LANG.
        Los arquetipos no lingüísticos siempre devuelven VEHICULAR.
        Ref: V06DOC_LEVELS Sección 4 (Modo de Inmersión — Normativa UGR).
        """
        if archetype_id != 'ARCH_LANG':
            return 'VEHICULAR'

        # LVL_C always total immersion / LVL_C siempre inmersión total
        if pedagogical_level == 'LVL_C':
            return 'TOTAL'

        # ITIN_MAI + LVL_B → total; ITIN_MAI + LVL_A → bilingual
        if itinerary_id == 'ITIN_MAI':
            return 'TOTAL' if pedagogical_level == 'LVL_B' else 'BILINGUAL'

        # LVL_B → bilingual; LVL_A → vehicular
        return 'BILINGUAL' if pedagogical_level == 'LVL_B' else 'VEHICULAR'

    @classmethod
    def get_context_metadata(cls, subject, context_title=None) -> dict:
        """
        Main entry point for the hybrid classification protocol.
        Phase 1: AI resolves cognitive identity (archetype + sub-archetype + language).
        Phase 2: Python resolves deterministic parameters (itinerary, level, immersion).
        Raises AIServiceCriticalError if Phase 1 fails — triggers 10-min Celery retry.
        ---
        Punto de entrada principal del protocolo de clasificación híbrido.
        Fase 1: La IA resuelve la identidad cognitiva (arquetipo + sub-arquetipo + idioma).
        Fase 2: Python resuelve los parámetros deterministas (itinerario, nivel, inmersión).
        Lanza AIServiceCriticalError si la Fase 1 falla — activa el reintento Celery de 10 min.
        Ref: V06DOC_LOGIC_MAPPING V1.3.
        """
        # -----------------------------------------------------------------------
        # FASE 1: Identidad Cognitiva vía IA
        # Cognitive Identity via AI
        # Ref: V06DOC_LOGIC_MAPPING V1.3 Sección 1
        # -----------------------------------------------------------------------
        settings = AutomationSettings.load()
        api_key  = settings.active_api_key

        if not api_key:
            raise AIServiceCriticalError(
                "No hay claves de API activas disponibles para la clasificación de asignatura."
            )

        success, identity, _ = classify_subject_identity(
            subject_name = context_title or subject.name,
            branch_name  = subject.academic_year.degree.branch.name,
            degree_name  = subject.academic_year.degree.name,
            api_key      = api_key
        )

        if not success:
            raise AIServiceCriticalError(
                f"Fallo en la clasificación IA de la asignatura '{context_title or subject.name}'. "
                f"El orquestador ejecutará el protocolo de reintentos de 10 min."
            )

        archetype_id         = identity.get('archetype_id', 'ARCH_SOC')
        sub_archetype_id     = identity.get('sub_archetype_id', 'SUB-SOC-LAW-DICT-CIV')
        target_language_code = identity.get('target_language_code', 'es')
        localized_sections   = identity.get('localized_sections', {})

        # Archetype validation — reject hallucinated or obsolete IDs
        # Validación de arquetipo — rechazar IDs alucinados u obsoletos
        if archetype_id not in cls.VALID_ARCHETYPES:
            logger.warning(
                f"AcademicDeductor: arquetipo IA '{archetype_id}' no válido. "
                f"Fallback a ARCH_SOC."
            )
            archetype_id = 'ARCH_SOC'

        # BARRERA DE FUEGO: purge language data for non-language archetypes
        # BARRERA DE FUEGO: purgar datos de idioma para arquetipos no lingüísticos
        if archetype_id != 'ARCH_LANG':
            localized_sections   = {}
            target_language_code = 'es'

        # -----------------------------------------------------------------------
        # FASE 2: Parámetros Deterministas vía Python
        # Deterministic Parameters via Python
        # Ref: V06DOC_LOGIC_MAPPING V1.3 Sección 2
        # -----------------------------------------------------------------------
        itinerary_id   = cls.deduce_itinerary(subject, context_title)
        pedagogical_level = cls.deduce_level(subject, context_title)
        immersion_mode = cls.deduce_immersion_mode(archetype_id, itinerary_id, pedagogical_level)

        logger.info(
            f"AcademicDeductor OK — Asignatura: '{context_title or subject.name}' | "
            f"Arquetipo: {archetype_id} | Sub: {sub_archetype_id} | "
            f"Nivel: {pedagogical_level} | Itinerario: {itinerary_id} | "
            f"Inmersión: {immersion_mode} | Idioma: {target_language_code}"
        )

        return {
            'archetype_id':          archetype_id,
            'sub_archetype_id':      sub_archetype_id,
            'itinerary_id':          itinerary_id,
            'pedagogical_level':     pedagogical_level,
            'immersion_mode':        immersion_mode,
            'target_language_code':  target_language_code,
            'localized_sections':    localized_sections,
        }


# ==============================================================================
# SECCIÓN 2: ORQUESTADOR DE CALIFICACIÓN
# Grading Orchestrator — submission grading pipeline
# Ref: V06DOC_BLOCKS, V06DOC_ARCHETYPES, V06DOC_METADATA, V06DOC_TEMPLATES
# ==============================================================================

class GradingOrchestrator:
    """
    Orchestrates the full grading pipeline for a student submission.
    Responsibilities:
      - Iterates all sections and items delegating to strategy.grade_item().
      - Applies rigor adjustment via strategy.apply_rigor_adjustment().
      - Enforces section-level kill-switches (CDS-KILL, FB_SAFETY, ITIN_INV).
      - Enforces archetype-level gating (ARCH_LANG Non-Compensation Rule).
      - Builds the GRADING_REPORT contract (V06DOC_TEMPLATES Sección 5).
      - Generates the qualitative summary (Professor Voice).
    ---
    Orquesta el pipeline de calificación completo de una entrega de alumno.
    Responsabilidades:
      - Itera todas las secciones e ítems delegando a strategy.grade_item().
      - Aplica el ajuste de rigor vía strategy.apply_rigor_adjustment().
      - Aplica kill-switches a nivel de sección (CDS-KILL, FB_SAFETY, ITIN_INV).
      - Aplica gating a nivel de arquetipo (Regla de No-Compensación ARCH_LANG).
      - Construye el contrato GRADING_REPORT (V06DOC_TEMPLATES Sección 5).
      - Genera el resumen cualitativo (Voz del Catedrático).
    """

    @staticmethod
    def grade_submission(submission, strategy):
        """
        Main grading entry point. Processes a Submission instance end-to-end.
        Returns the grading_report dict and persists it to submission.grading_report.
        ---
        Punto de entrada principal de calificación. Procesa una instancia Submission de extremo a extremo.
        Devuelve el dict grading_report y lo persiste en submission.grading_report.
        Ref: V06DOC_TEMPLATES Sección 5 (GRADING_REPORT Contract).
        """
        # Extract raw responses from submission contract
        # Extraer respuestas brutas del contrato de entrega
        responses = submission.student_responses.get('responses', {}) \
            if isinstance(submission.student_responses, dict) \
            else {}

        exam = submission.exam

        # Initialize report structure / Inicializar estructura del informe
        report = {
            'sections':  [],
            'global_flags': [],
            'feedback_stats': {
                'FB_CONCEPT':    0,
                'FB_FORMAL':     0,
                'FB_PROCEDURAL': 0,
                'FB_SAFETY':     0
            },
            'qualitative_summary': ''
        }

        total_exam_score  = Decimal('0.0')
        section_scores    = {}
        sections          = exam.sections.all().prefetch_related('items')
        section_count     = sections.count()

        for section in sections:
            section_score         = Decimal('0.0')
            section_items         = list(section.items.all())
            section_items_count   = len(section_items)
            section_kill_activated = False

            section_report = {
                'subdivision_id': section.subdivision_id,
                'title':          section.title,
                'items':          [],
                'status':         'COMPLETED',
                'section_score':  0.0
            }

            for item in section_items:
                # Retrieve student input for this item
                # Recuperar la entrada del alumno para este ítem
                student_payload = responses.get(str(item.id), {})

                # Normalize raw_input extraction (V06DOC_TEMPLATES Sec 4 contract)
                # Normalizar la extracción de raw_input (contrato V06DOC_TEMPLATES Sec 4)
                if isinstance(student_payload, dict) and 'raw_input' in student_payload:
                    student_input = student_payload['raw_input']
                else:
                    student_input = student_payload

                # Delegate to archetype strategy / Delegar a la estrategia del arquetipo
                item_raw_score, item_feedback = strategy.grade_item(item, student_input)

                # Apply rigor adjustment / Aplicar ajuste de rigor
                item_final_score = strategy.apply_rigor_adjustment(item_raw_score)

                # Feedback taxonomy counting / Conteo de taxonomía de feedback
                fb_category = item_feedback.get('feedback_category', 'FB_CONCEPT')
                if fb_category in report['feedback_stats']:
                    report['feedback_stats'][fb_category] += 1

                # -----------------------------------------------------------
                # KILL-SWITCH LOGIC (Ref: V06DOC_BLOCKS Sección 2, V06DOC_ARCHETYPES)
                # -----------------------------------------------------------

                # CDS-KILL explicit flag
                if item_feedback.get('kill_switch_activated', False):
                    section_kill_activated = True
                    section_report['status'] = 'ANNULLED_BY_SAFETY_BREACH'
                    report['global_flags'].append(
                        f"KILL_SWITCH activado en sección {section.subdivision_id} "
                        f"(ítem {item.id}, block_type: {item.block_type})"
                    )
                    report['feedback_stats']['FB_SAFETY'] += 1

                # ITIN_INV: fatal on methodological/conceptual error ≥ LVL_B
                # ITIN_INV: fatal en error metodológico/conceptual ≥ LVL_B
                if (
                    exam.itinerary_id == 'ITIN_INV' and
                    fb_category in ('FB_PROCEDURAL', 'FB_CONCEPT') and
                    item_final_score < Decimal('0.5')
                ):
                    section_kill_activated = True
                    section_report['status'] = 'ANNULLED_BY_METHODOLOGICAL_ERROR'
                    item_feedback['kill_switch_activated'] = True
                    item_feedback['justification'] = (
                        'ERROR FATAL METODOLÓGICO (ITIN_INV): ' +
                        item_feedback.get('justification', '')
                    )
                    report['global_flags'].append(
                        f"ITIN_INV KILL activado en sección {section.subdivision_id}"
                    )

                # ARCH_HEALTH: safety errors are always fatal
                # ARCH_HEALTH: los errores de seguridad son siempre fatales
                if (
                    exam.archetype_id == 'ARCH_HEALTH' and
                    fb_category == 'FB_SAFETY' and
                    item_final_score < Decimal('0.5')
                ):
                    section_kill_activated = True
                    section_report['status'] = 'ANNULLED_BY_CLINICAL_SAFETY_BREACH'
                    item_feedback['kill_switch_activated'] = True
                    item_feedback['justification'] = (
                        'ERROR FATAL CLÍNICO (SEGURIDAD): ' +
                        item_feedback.get('justification', '')
                    )
                    report['global_flags'].append(
                        f"ARCH_HEALTH SAFETY KILL en sección {section.subdivision_id}"
                    )

                # ARCH_HUM: formal errors carry a fixed deduction (-0.2/1.0)
                # The penalty is eliminatory if score reaches 0.0
                # ARCH_HUM: los errores formales tienen una deducción fija (-0.2/1.0)
                # La penalización es eliminatoria si la nota llega a 0.0
                if exam.archetype_id == 'ARCH_HUM' and fb_category == 'FB_FORMAL':
                    item_final_score = max(
                        Decimal('0.0'),
                        item_final_score - Decimal('0.2')
                    )
                    item_feedback['justification'] = (
                        'PENALIZACIÓN FORMAL HUMANIDADES (-0.2): ' +
                        item_feedback.get('justification', '')
                    )
                    if item_final_score <= Decimal('0.0'):
                        item_feedback['kill_switch_activated'] = True
                        section_kill_activated = True
                        section_report['status'] = 'ANNULLED_BY_FORMAL_BREACH'
                        report['global_flags'].append(
                            f"ARCH_HUM FORMAL KILL en sección {section.subdivision_id}"
                        )

                # ARCH_SOC: verified real sources grant a +20% bonus (cap 1.0)
                # ARCH_SOC: las fuentes reales verificadas otorgan un bonus del +20% (tope 1.0)
                if (
                    exam.archetype_id == 'ARCH_SOC' and
                    'fuentes_reales' in item_feedback.get('justification', '').lower()
                ):
                    item_final_score = min(
                        Decimal('1.0'),
                        item_final_score * Decimal('1.2')
                    )
                    item_feedback['justification'] = (
                        '[MULTIPLICADOR FUENTES REALES +20%] ' +
                        item_feedback.get('justification', '')
                    )

                # -----------------------------------------------------------
                # BUILD ITEM REPORT (strict GRADING_REPORT contract)
                # CONSTRUIR INFORME DE ÍTEM (contrato estricto GRADING_REPORT)
                # Ref: V06DOC_TEMPLATES Sección 5
                # -----------------------------------------------------------
                section_report['items'].append({
                    'item_id':           str(item.id),
                    'item_score':        float(item_final_score),
                    'feedback_category': fb_category,
                    'justification':     item_feedback.get(
                        'justification',
                        item_feedback.get('feedback_justification', 'Evaluación completada.')
                    ),
                    'kill_switch_activated': item_feedback.get('kill_switch_activated', False),
                    'trace':             item_feedback.get('trace', []),
                    'pending_ai_refinement': item_feedback.get('pending_ai_refinement', False)
                })

                section_score += item_final_score

            # -------------------------------------------------------------------
            # FINALIZE SECTION SCORE
            # FINALIZAR NOTA DE SECCIÓN
            # -------------------------------------------------------------------
            if section_kill_activated:
                # Complete section annulment / Anulación completa de la sección
                section_normalized = Decimal('0.0')
            else:
                section_normalized = (
                    section_score / Decimal(str(section_items_count))
                ) if section_items_count > 0 else Decimal('0.0')

            section_report['section_score'] = float(section_normalized)
            report['sections'].append(section_report)
            section_scores[section.subdivision_id] = float(section_normalized)
            total_exam_score += section_normalized

        # =======================================================================
        # FINAL SCORE CALCULATION
        # CÁLCULO DE NOTA FINAL
        # =======================================================================
        final_score = (
            total_exam_score / Decimal(str(section_count))
        ) if section_count > 0 else Decimal('0.0')

        # =======================================================================
        # GATING LOGIC — ARCH_LANG Non-Compensation Rule
        # LÓGICA DE GATING — Regla de No-Compensación ARCH_LANG
        # Ref: V06DOC_ARCHETYPES (CertAcles/CLM-UGR: mínimo por destreza)
        # The pass threshold per skill is variable by convocatoria;
        # the platform uses 0.5 (50%) as the certified minimum from V06DOC_METADATA.
        # El umbral de superación por destreza es variable por convocatoria;
        # la plataforma usa 0.5 (50%) como mínimo certificado desde V06DOC_METADATA.
        # =======================================================================
        passed = final_score >= Decimal('0.5')

        if exam.archetype_id == 'ARCH_LANG':
            for sec_rep in report['sections']:
                sec_score = float(sec_rep.get('section_score', 0.0))
                if sec_score < 0.5:
                    passed = False
                    report['global_flags'].append(
                        f"GATING_FAILED: Destreza {sec_rep.get('subdivision_id')} "
                        f"no supera el mínimo certificado (50%). "
                        f"Nota obtenida: {sec_score:.2%}."
                    )

        # =======================================================================
        # QUALITATIVE SUMMARY (Professor Voice)
        # RESUMEN CUALITATIVO (Voz del Catedrático)
        # Ref: V06DOC_METADATA Sección 6 (Rol Docente)
        # =======================================================================
        report['qualitative_summary'] = GradingOrchestrator._generate_qualitative_feedback(
            score      = final_score,
            level      = exam.pedagogical_level,
            itinerary  = exam.itinerary_id,
            archetype  = exam.archetype_id,
            stats      = report['feedback_stats']
        )

        # =======================================================================
        # PERSIST SUBMISSION
        # PERSISTIR ENTREGA
        # =======================================================================
        submission.grading_report  = report
        submission.section_scores  = section_scores
        submission.final_score     = final_score
        submission.passed          = passed
        submission.graded_at       = timezone.now()
        submission.save()

        logger.info(
            f"GradingOrchestrator OK — Examen {str(exam.uuid)[:8]} | "
            f"Nota final: {float(final_score):.4f} | "
            f"Superado: {passed} | "
            f"Secciones: {section_count}"
        )

        return report

    @staticmethod
    def _generate_qualitative_feedback(score, level, itinerary, archetype, stats) -> str:
        """
        Generates the 'Professor Voice' qualitative summary.
        Tone adapts to pedagogical level and itinerary.
        Content adapts to archetype and dominant feedback category.
        ---
        Genera el resumen cualitativo 'Voz del Catedrático'.
        El tono se adapta al nivel pedagógico y al itinerario.
        El contenido se adapta al arquetipo y a la categoría de feedback dominante.
        Ref: V06DOC_METADATA Sección 6 (Rol Docente — Taxonomía de Respuesta).
        """
        score_float   = float(score)
        dominant_error = max(stats, key=stats.get) if any(stats.values()) else 'FB_CONCEPT'

        # Determine tone / Determinar tono
        if level == 'LVL_C' or itinerary in ('ITIN_MAI', 'ITIN_INV'):
            tone = 'ACADEMIC_RIGOROUS'
        elif level == 'LVL_A':
            tone = 'DIDACTIC_SUPPORTIVE'
        else:
            tone = 'PROFESSIONAL_NEUTRAL'

        # Archetype-specific label for feedback context
        # Etiqueta específica por arquetipo para el contexto de feedback
        archetype_context = {
            'ARCH_LANG':   'lingüística',
            'ARCH_HEALTH': 'clínica y de seguridad',
            'ARCH_TECH':   'técnica y procedimental',
            'ARCH_SOC':    'jurídica y social',
            'ARCH_HUM':    'humanística y crítica',
            'ARCH_SCI':    'científica y metodológica'
        }.get(archetype, 'académica')

        # Generate summary by tone and score / Generar resumen por tono y nota
        if tone == 'ACADEMIC_RIGOROUS':
            if score_float >= 0.9:
                return _(
                    f"Excelente dominio {archetype_context}. Su argumentación denota madurez crítica "
                    f"y precisión terminológica propia del nivel experto. Resultado sobresaliente."
                )
            elif score_float >= 0.7:
                return _(
                    f"Notable. Demuestra competencia sólida en el ámbito {archetype_context}, "
                    f"con algunos aspectos mejorables en precisión formal."
                )
            elif score_float >= 0.5:
                error_label = {
                    'FB_CONCEPT':    'conceptuales',
                    'FB_FORMAL':     'formales y de registro',
                    'FB_PROCEDURAL': 'procedimentales y metodológicos',
                    'FB_SAFETY':     'de seguridad crítica'
                }.get(dominant_error, 'generales')
                return _(
                    f"Suficiente. Competencia base demostrada, pero se detectan imprecisiones {error_label} "
                    f"que deben corregirse para acceder al nivel superior de especialización."
                )
            else:
                error_label = {
                    'FB_CONCEPT':    'conceptuales fundamentales',
                    'FB_FORMAL':     'formales y de registro académico',
                    'FB_PROCEDURAL': 'procedimentales y de método científico',
                    'FB_SAFETY':     'de protocolos de seguridad crítica'
                }.get(dominant_error, 'de base')
                return _(
                    f"Insuficiente. Carece del rigor exigido para la especialidad {archetype_context}. "
                    f"Se detectan deficiencias {error_label} que requieren revisión exhaustiva "
                    f"de los fundamentos de la materia."
                )

        elif tone == 'DIDACTIC_SUPPORTIVE':
            if score_float >= 0.8:
                return _("¡Muy buen trabajo! Has asimilado los conceptos clave y demuestras un nivel sólido. Sigue así.")
            elif score_float >= 0.5:
                return _(
                    "Aprobado. Tienes la base necesaria, pero hay aspectos que puedes mejorar. "
                    "Revisa los ítems marcados en rojo y consulta las justificaciones."
                )
            else:
                return _(
                    "No te desanimes. Identifica los conceptos donde has tenido más dificultades "
                    "y enfócate en reforzarlos. Cada intento es una oportunidad de aprendizaje."
                )

        else:  # PROFESSIONAL_NEUTRAL
            if score_float >= 0.8:
                return _("Competencia validada. Desempeño apto para el entorno profesional.")
            elif score_float >= 0.5:
                return _(
                    "Apto condicional. Cumple los requisitos mínimos pero requiere supervisión "
                    "en los aspectos marcados. Se recomienda consolidar antes de la práctica autónoma."
                )
            else:
                return _(
                    "No apto. No cumple con los estándares mínimos requeridos. "
                    "Revisión obligatoria del módulo completo antes de nueva evaluación."
                )
