# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/logic.py
import re
import logging
from decimal import Decimal
from django.utils import timezone
from django.utils.translation import gettext as _
from academic_structure.models import Subject
from orchestrator.models import AutomationSettings
from core.services.gemini_service import classify_subject_identity, AIServiceCriticalError

logger = logging.getLogger(__name__)

class AcademicDeductor:
    """
    Service for hybrid deduction of academic parameters (IA + Logic).
    Servicio de deducción híbrida de parámetros académicos (IA + Lógica).
    Ref: V06DOC_LOGIC_MAPPING V1.3.
    """

    @staticmethod
    def deduce_itinerary(subject, context_title=None):
        """
        Deduces the ITIN_ID based on terminology and subject type.
        Supports ITIN_ROT and ITIN_PROF for health and engineering.
        ---
        Deduce el ITIN_ID basándose en la terminología y el tipo de asignatura.
        Soporta ITIN_ROT e ITIN_PROF para salud e ingeniería.
        """
        name = (context_title or subject.name).lower()
        branch_name = subject.academic_year.degree.branch.name.lower()
        
        # 1. Detección Explícita (V06DOC_LOGIC_MAPPING)
        if re.search(r'\bmaior\b', name):
            return 'ITIN_MAI'
        if re.search(r'\bminor\b', name):
            return 'ITIN_MIN'
        
        # 2. Mapeo por Rama Académica (Itinerarios Específicos Hito 6)
        if any(k in branch_name for k in ['salud', 'medicina', 'enfermería', 'veterinaria']):
            return 'ITIN_ROT'
        if any(k in branch_name for k in ['ingeniería', 'técnica', 'arquitectura']):
            return 'ITIN_PROF'
        # Investigación (Investigador)
        if any(k in branch_name for k in ['investigac', 'doctoral']):
            return 'ITIN_INV'
        
        # 3. Fallback por tipo oficial de asignatura
        if subject.subject_type in [Subject.SubjectType.CORE, Subject.SubjectType.MANDATORY]:
            return 'ITIN_MAI'
        
        return 'ITIN_MIN'

    @staticmethod
    def deduce_level(subject, context_title=None):
        """
        Deduces the LVL_ID (Pedagogical Level).
        Deduce el LVL_ID (Nivel Pedagógico).
        """
        name = (context_title or subject.name).lower()
        year = subject.academic_year.year if subject.academic_year else 1

        # 1. Semantic detection (Including Roman Numerals from V06DOC_LEVELS)
        if re.search(r'(avanzado|superior|c1|c2|nivel iii\b|\biii\b|\biv\b)', name):
            return 'LVL_C'
        if re.search(r'(intermedio|b1|b2|nivel ii\b|\bii\b)', name):
            return 'LVL_B'
        if re.search(r'(inicial|básico|basico|a1|a2|intro|nivel i\b|\bi\b)', name):
            return 'LVL_A'

        # 2. Year-based fallback
        if year <= 2:
            return 'LVL_A'
        if year == 3:
            return 'LVL_B'
        
        return 'LVL_C'

    @classmethod
    def get_context_metadata(cls, subject, context_title=None):
        """
        Main entry point: Resolves identity via AI and parameters via Python.
        Punto de entrada principal: Resuelve identidad vía IA y parámetros vía Python.
        """
        # FASE 1: Identidad Cognitiva (IA)
        # Ref: V06DOC_LOGIC_MAPPING V1.3 Section 1
        settings = AutomationSettings.load()
        api_key = settings.active_api_key
        
        if not api_key:
            raise AIServiceCriticalError("No hay claves de API activas para la clasificación.")

        success, identity, _ = classify_subject_identity(
            subject_name=context_title or subject.name,
            branch_name=subject.academic_year.degree.branch.name,
            degree_name=subject.academic_year.degree.name,
            api_key=api_key
        )

        if not success:
            # Propagamos el error para que el orquestador ejecute el protocolo de reintentos de 10 min
            raise AIServiceCriticalError("Fallo en la clasificación IA de la asignatura.")

        archetype_id = identity.get('archetype_id', 'ARCH_SOC')
        sub_archetype_id = identity.get('sub_archetype_id', 'DEFAULT')
        target_language_code = identity.get('target_language_code', 'es')
        localized_sections = identity.get('localized_sections', {})

        # Validación estricta para asegurar que mapea a los nuevos arquetipos (HITO 6)
        VALID_ARCHETYPES = ['ARCH_LANG', 'ARCH_HEALTH', 'ARCH_TECH', 'ARCH_SOC', 'ARCH_HUM', 'ARCH_SCI']
        if archetype_id not in VALID_ARCHETYPES:
            archetype_id = 'ARCH_SOC'

        # FASE 2: Parámetros Deterministas (Python)
        # Ref: V06DOC_LOGIC_MAPPING V1.3 Section 2
        itinerary_id = cls.deduce_itinerary(subject, context_title)
        level_id = cls.deduce_level(subject, context_title)
        
        return {
            'archetype_id': archetype_id,
            'sub_archetype_id': sub_archetype_id,
            'itinerary_id': itinerary_id,
            'pedagogical_level': level_id,
            'target_language_code': target_language_code,
            'localized_sections': localized_sections,
        }

class GradingOrchestrator:
    """
    Orchestrates the grading process for a submission.
    Ensures compliance with V06DOC_BLOCKS (Section 2: CDS-KILL Annulment).
    Enriches the report with Feedback Taxonomy (V06DOC_METADATA).
    ---
    Orquesta el proceso de calificación de una entrega.
    Garantiza el cumplimiento de V06DOC_BLOCKS (Sección 2: Anulación por CDS-KILL).
    Enriquece el informe con Taxonomía de Feedback (V06DOC_METADATA).
    """

    @staticmethod
    def grade_submission(submission, strategy):
        """
        Grades all items and sections, applying section-level kill-switches.
        Generates a qualitative report based on the Professor Role.
        ---
        Califica todos los ítems y secciones, aplicando interruptores de anulación (kill-switches).
        Genera un informe cualitativo basado en el Rol del Catedrático.
        """
        responses = submission.student_responses.get('responses', {})
        report = {
            "sections": [], 
            "global_flags": [],
            "feedback_stats": {
                "FB_CONCEPT": 0, "FB_FORMAL": 0, "FB_PROCEDURAL": 0, "FB_SAFETY": 0
            },
            "qualitative_summary": ""
        }
        total_exam_score = Decimal('0.0')
        exam = submission.exam
        
        sections = exam.sections.all().prefetch_related('items')
        
        for section in sections:
            section_score = Decimal('0.0')
            section_items_count = section.items.count()
            section_kill_activated = False
            section_report = {
                "subdivision_id": section.subdivision_id,
                "title": section.title,
                "items": [],
                "status": "COMPLETED",
                "section_score": 0.0
            }

            for item in section.items.all():
                student_input = responses.get(str(item.id))
                item_raw_score, item_feedback = strategy.grade_item(item, student_input)
                
                # Apply Rigor Adjustment (Ref: V06DOC_LEVELS)
                # Aplicar Ajuste de Rigor (Ref: V06DOC_LEVELS)
                item_final_score = strategy.apply_rigor_adjustment(item_raw_score)
                
                # Feedback Taxonomy Counting
                fb_category = item_feedback.get('feedback_category', 'FB_CONCEPT')
                if fb_category in report['feedback_stats']:
                    report['feedback_stats'][fb_category] += 1
                
                # Check for Section-Level Kill Switch (Ref: V06DOC_BLOCKS)
                # Comprobar Interruptor de Anulación de Sección
                if item_feedback.get('kill_switch_activated', False):
                    section_kill_activated = True
                    section_report['status'] = "ANNULLED_BY_SAFETY_BREACH"
                    report['global_flags'].append(f"KILL_SWITCH triggered in {section.subdivision_id}")
                    # Safety Feedback Priority
                    report['feedback_stats']['FB_SAFETY'] += 1

                section_report['items'].append({
                    "id": item.id,
                    "score": float(item_final_score),
                    "feedback": item_feedback,
                    "feedback_category": fb_category
                })
                section_score += item_final_score

            # Finalize section score / Finalizar nota de sección
            if section_kill_activated:
                section_score = Decimal('0.0') # Anulación completa de la fase / Phase annulment
            
            section_normalized = (section_score / section_items_count) if section_items_count > 0 else Decimal('0.0')
            section_report['section_score'] = float(section_normalized)
            report['sections'].append(section_report)
            total_exam_score += section_normalized

        # Final Exam Score (Average of sections)
        final_score = (total_exam_score / sections.count()) if sections.count() > 0 else Decimal('0.0')
        
        # Generate Qualitative Summary (Professor Role)
        report['qualitative_summary'] = GradingOrchestrator._generate_qualitative_feedback(
            final_score, exam.pedagogical_level, exam.itinerary_id, report['feedback_stats']
        )
        
        submission.grading_report = report
        submission.final_score = final_score
        submission.passed = final_score >= Decimal('0.5')
        submission.graded_at = timezone.now()
        submission.save()

        return report

    @staticmethod
    def _generate_qualitative_feedback(score, level, itinerary, stats):
        """
        Generates the 'Professor's Voice' summary based on academic level and itinerary.
        ---
        Genera el resumen 'Voz del Catedrático' basado en el nivel académico e itinerario.
        """
        score_float = float(score)
        
        # 1. Define Tone / Definir Tono
        if level == 'LVL_C' or itinerary == 'ITIN_MAI' or itinerary == 'ITIN_INV':
            tone = "ACADEMIC_RIGOROUS" # Severo, exigente, terminología precisa
        elif level == 'LVL_A':
            tone = "DIDACTIC_SUPPORTIVE" # Constructivo, orientador
        else:
            tone = "PROFESSIONAL_NEUTRAL" # Objetivo, funcional

        # 2. Select Template / Seleccionar Plantilla
        if tone == "ACADEMIC_RIGOROUS":
            if score_float >= 0.9:
                return _("Excelente dominio. Su argumentación denota madurez crítica y precisión terminológica propia del nivel experto.")
            elif score_float >= 0.5:
                return _("Suficiente. Demuestra competencia base, pero se detectan imprecisiones formales que deben depurarse para el nivel superior.")
            else:
                fail_focus = "conceptuales" if stats['FB_CONCEPT'] > stats['FB_FORMAL'] else "formales"
                return _(f"Insuficiente. Carece del rigor exigido para la especialidad. Revise urgentemente las bases {fail_focus}.")
        
        elif tone == "DIDACTIC_SUPPORTIVE":
            if score_float >= 0.8:
                return _("¡Muy buen trabajo! Has asimilado los conceptos clave y vas por buen camino.")
            elif score_float >= 0.5:
                return _("Aprobado. Tienes la base, pero necesitas practicar más para ganar seguridad.")
            else:
                return _("No te desanimes. Enfócate en repasar los conceptos fundamentales marcados en rojo.")
        
        else: # PROFESSIONAL
            if score_float >= 0.8:
                return _("Competencia validada. Desempeño apto para el entorno profesional.")
            elif score_float >= 0.5:
                return _("Apto condicional. Cumple requisitos mínimos pero requiere supervisión.")
            else:
                return _("No apto. No cumple con los estándares mínimos de seguridad o técnica.")
