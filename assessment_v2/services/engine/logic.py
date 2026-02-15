# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/logic.py
import re
from academic_structure.models import Subject

class AcademicDeductor:
    """
    Service for heuristic deduction of academic parameters.
    Servicio de deducción heurística de parámetros académicos según el estándar de la plataforma.
    """

    @staticmethod
    def deduce_archetype(subject):
        """
        Deduces the ARCH_ID based on the subject name and academic branch.
        """
        name = subject.name.lower()
        branch_name = subject.academic_year.degree.branch.name.lower()

        # 1. Languages
        if re.search(r'(lengua|idioma|language)', name):
            return 'ARCH_LANG'
        
        # 2. Health Sciences
        if any(keyword in branch_name for keyword in ['salud', 'medicina', 'enfermería', 'veterinaria']):
            return 'ARCH_HEALTH'
        
        # 3. Technical Sciences & Engineering
        if any(keyword in branch_name for keyword in ['ingeniería', 'técnica', 'arquitectura', 'ciencias']):
            return 'ARCH_TECH'

        # 4. Arts & Humanities
        if any(keyword in branch_name for keyword in ['artes', 'humanidades', 'filosofía', 'historia']):
            return 'ARCH_HUM'

        return 'ARCH_SOC'

    @staticmethod
    def deduce_itinerary(subject):
        """
        Deduces the ITIN_ID based on terminology and subject type.
        """
        name = subject.name.lower()
        
        if re.search(r'\bmaior\b', name):
            return 'ITIN_MAI'
        if re.search(r'\bminor\b', name):
            return 'ITIN_MIN'
        
        # Fallback by official subject type
        if subject.subject_type in [Subject.SubjectType.CORE, Subject.SubjectType.MANDATORY]:
            return 'ITIN_MAI'
        
        return 'ITIN_MIN'

    @staticmethod
    def deduce_level(subject):
        """
        Deduces the LVL_ID (Pedagogical Level).
        """
        name = subject.name.lower()
        year = subject.academic_year.year if subject.academic_year else 1

        # 1. Semantic detection
        if re.search(r'(inicial|básico|basico|a1|a2|intro)', name):
            return 'LVL_A'
        if re.search(r'(intermedio|b1|b2)', name):
            return 'LVL_B'
        if re.search(r'(avanzado|superior|c1|c2)', name):
            return 'LVL_C'

        # 2. Year-based fallback
        if year <= 2:
            return 'LVL_A'
        if year == 3:
            return 'LVL_B'
        
        return 'LVL_C'

    @classmethod
    def get_context_metadata(cls, subject):
        """
        Returns the full metadata pack for the Exam Contract.
        """
        return {
            'archetype_id': cls.deduce_archetype(subject),
            'itinerary_id': cls.deduce_itinerary(subject),
            'pedagogical_level': cls.deduce_level(subject),
        }
