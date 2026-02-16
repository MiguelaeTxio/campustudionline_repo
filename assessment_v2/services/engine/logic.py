# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/services/engine/logic.py
import re
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

        # 1. Semantic detection
        if re.search(r'(avanzado|superior|c1|c2| nivel iii\b|\b iii\b)', name):
            return 'LVL_C'
        if re.search(r'(intermedio|b1|b2| nivel ii\b|\b ii\b)', name):
            return 'LVL_B'
        if re.search(r'(inicial|básico|basico|a1|a2|intro| nivel i\b|\b i\b)', name):
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
        return {
            'archetype_id': cls.deduce_archetype(subject, context_title),
            'itinerary_id': cls.deduce_itinerary(subject, context_title),
            'pedagogical_level': cls.deduce_level(subject, context_title),
        }
