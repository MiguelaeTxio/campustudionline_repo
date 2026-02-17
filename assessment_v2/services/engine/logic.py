# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/logic.py
import re
from decimal import Decimal
from django.utils import timezone
from academic_structure.models import Subject

class AcademicDeductor:
    """
    Service for heuristic deduction of academic parameters.
    Servicio de deducción heurística de parámetros académicos según el estándar de la plataforma.
    """

    @staticmethod
    def deduce_archetype(subject, context_title=None):
        """
        Deduces the ARCH_ID based on the subject name and academic branch.
        Deduce el ARCH_ID basándose en el nombre de la asignatura y la rama académica.
        """
        name = (context_title or subject.name).lower()
        branch_name = subject.academic_year.degree.branch.name.lower()

        # 1. Languages
        if re.search(r'(lengua|idioma|language|lingüística|translation)', name):
            return 'ARCH_LANG'
        
        # 2. Health Sciences
        if any(keyword in branch_name for keyword in ['salud', 'medicina', 'enfermería', 'veterinaria', 'farmacia', 'odontología']):
            return 'ARCH_HEALTH'
        
        # 3. Technical Sciences & Engineering
        if any(keyword in branch_name for keyword in ['ingeniería', 'técnica', 'arquitectura', 'ciencias', 'física', 'matemática']):
            return 'ARCH_TECH'

        # 4. Arts & Humanities
        if any(keyword in branch_name for keyword in ['artes', 'humanidades', 'filosofía', 'historia', 'educación', 'bellas']):
            return 'ARCH_HUM'

        return 'ARCH_SOC'

    @staticmethod
    def deduce_sub_archetype(archetype_id, subject, context_title=None):
        """
        Deduces the specific Sub-Archetype (22 specializations) based on V06DOC_SUBARCHETYPES.
        ---
        Deduce el Sub-Arquetipo específico (22 especialidades) basado en V06DOC_SUBARCHETYPES.
        """
        name = (context_title or subject.name).lower()
        
        # TECH Mapping / Mapeo TECH
        if archetype_id == 'ARCH_TECH':
            if re.search(r'(software|informát|computac|programac|datos)', name): return 'SUB-TEC-SOFT'
            if re.search(r'(civil|camin|estruct|geotec|hidrául)', name): return 'SUB-TEC-CIVIL'
            if re.search(r'(indus|termodin|máquin|eléctr|energ)', name): return 'SUB-TEC-INDUS'
            if re.search(r'(químic|reacc|cinét)', name): return 'SUB-TEC-CHEM'
            return 'SUB-TEC-PURE'

        # HEALTH Mapping / Mapeo SALUD
        if archetype_id == 'ARCH_HEALTH':
            if re.search(r'(medicin|cirug|patolog|clínic)', name): return 'SUB-SAN-MED'
            if re.search(r'(enfermer|cuidad|nanda|dietét)', name): return 'SUB-SAN-CUID'
            if re.search(r'(bioquím|farmac|laborat|analít)', name): return 'SUB-SAN-BIO'
            if re.search(r'(psicolog|psiquia|conduct|mente)', name): return 'SUB-SAN-PSY'
            return 'SUB-SAN-VET'

        # LANG Mapping / Mapeo LENGUAS
        if archetype_id == 'ARCH_LANG':
            if re.search(r'(técnic|profes|fines|business)', name): return 'SUB-LIN-PROF'
            if re.search(r'(literat|filolog|crític|poes)', name): return 'SUB-LIN-LIT'
            return 'SUB-LIN-CERT'

        # SOC Mapping / Mapeo SOCIALES
        if archetype_id == 'ARCH_SOC':
            if re.search(r'(derech|juríd|legal|norma|boe)', name): return 'SUB-SOC-JUR'
            if re.search(r'(econom|ade|contab|finan|auditor)', name): return 'SUB-SOC-ECON'
            if re.search(r'(sociolog|polít|estado|antrop)', name): return 'SUB-SOC-BEHAV'
            return 'SUB-SOC-COMM'

        # HUM Mapping / Mapeo HUMANIDADES
        if archetype_id == 'ARCH_HUM':
            if re.search(r'(histori|arqueol|antig|cronol)', name): return 'SUB-HUM-HIST'
            if re.search(r'(filosof|lógic|ética|metaf)', name): return 'SUB-HUM-PHIL'
            if re.search(r'(educac|pedagog|didáct|lomloe|dua)', name): return 'SUB-HUM-EDU'
            if re.search(r'(músic|armon|solfe|audit)', name): return 'SUB-ART-MUS'
            return 'SUB-ART-CREA'

        return 'DEFAULT'

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
        Returns the full metadata pack for the Exam Contract.
        Devuelve el paquete completo de metadatos para el Contrato de Examen.
        """
        archetype_id = cls.deduce_archetype(subject, context_title)
        return {
            'archetype_id': archetype_id,
            'sub_archetype_id': cls.deduce_sub_archetype(archetype_id, subject, context_title),
            'itinerary_id': cls.deduce_itinerary(subject, context_title),
            'pedagogical_level': cls.deduce_level(subject, context_title),
        }

class GradingOrchestrator:
    """
    Orchestrates the grading process for a submission.
    Ensures compliance with V06DOC_BLOCKS (Section 2: CDS-KILL Annulment).
    ---
    Orquesta el proceso de calificación de una entrega.
    Garantiza el cumplimiento de V06DOC_BLOCKS (Sección 2: Anulación por CDS-KILL).
    """

    @staticmethod
    def grade_submission(submission, strategy):
        """
        Grades all items and sections, applying section-level kill-switches.
        ---
        Califica todos los ítems y secciones, aplicando interruptores de anulación (kill-switches).
        """
        responses = submission.student_responses.get('responses', {})
        report = {"sections": [], "global_flags": []}
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
                "status": "COMPLETED"
            }

            for item in section.items.all():
                student_input = responses.get(str(item.id))
                item_raw_score, item_feedback = strategy.grade_item(item, student_input)
                
                # Apply Rigor Adjustment (Ref: V06DOC_LEVELS)
                # Aplicar Ajuste de Rigor (Ref: V06DOC_LEVELS)
                item_final_score = strategy.apply_rigor_adjustment(item_raw_score)
                
                # Check for Section-Level Kill Switch (Ref: V06DOC_BLOCKS)
                # Comprobar Interruptor de Anulación de Sección
                if item_feedback.get('kill_switch_activated', False):
                    section_kill_activated = True
                    section_report['status'] = "ANNULLED_BY_SAFETY_BREACH"
                    report['global_flags'].append(f"KILL_SWITCH triggered in {section.subdivision_id}")

                section_report['items'].append({
                    "id": item.id,
                    "score": float(item_final_score),
                    "feedback": item_feedback
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
        
        submission.grading_report = report
        submission.final_score = final_score
        submission.passed = final_score >= Decimal('0.5')
        submission.graded_at = timezone.now()
        submission.save()

        return report
