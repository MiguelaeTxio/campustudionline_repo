# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/management/commands/validate_v06_engines.py
"""
Management command: validate_v06_engines
Validates that all 82 certified sub-archetypes have a functional exam engine by locating
real subjects with generated material already in the database (no fixed list, no data population).
Uses get_exam_skeleton() — the actual BaseExamStrategy API — instead of the non-existent get_section_plan().
Complies with V06DOC_SUBARCHETYPES v5.9 (82 sub-archetypes) and V06DOC_STRUCTURE v5.9.
---
Comando de gestión: validate_v06_engines
Valida que los 82 subarquetipos certificados tienen un motor de examen funcional, localizando
asignaturas reales con material ya generado en la base de datos (sin lista fija, sin poblar datos).
Usa get_exam_skeleton() — la API real de BaseExamStrategy — en lugar del inexistente get_section_plan().
Cumple con V06DOC_SUBARCHETYPES v5.9 (82 subarquetipos) y V06DOC_STRUCTURE v5.9.
"""
import time
import logging
from django.core.management.base import BaseCommand
from django.db import transaction, connection
from academic_structure.models import Subject
from assessment_v2.services.engine.factory import ExamFactory
from assessment_v2.models.main import Exam, ExamSection
from assessment_v2.services.engine.logic import AcademicDeductor
from users.models import CustomUser
from contents.models import ContentCopy, ContentMaterial
from orchestrator.models import AutomationSettings, ApiKey

# Silenciar logs de librerías externas para legibilidad en Android
# Silence external library logs for Android readability
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("google").setLevel(logging.ERROR)


class Command(BaseCommand):
    help = (
        'Validación V06 — Protocolo de Resiliencia Extrema. '
        'Verifica los 82 motores certificados contra asignaturas reales en BD. '
        'No requiere poblar datos: trabaja con el catálogo existente (~2.500 asignaturas).'
    )

    # Catálogo certificado v5.9 — 82 subarquetipos agrupados por arquetipo
    # Certified catalogue v5.9 — 82 sub-archetypes grouped by archetype
    # Ref: V06DOC_SUBARCHETYPES.md (v5.9 — 2026-05-16)
    CERTIFIED_SUB_ARCHETYPES = {
        'ARCH_LANG': [
            'SUB-LIN-INSTR', 'SUB-LIN-MINOR', 'SUB-LIN-PHILO',
            'SUB-LIN-ECDO', 'SUB-LIN-NORM', 'SUB-LIN-TRA-TECH', 'SUB-LIN-TRA-LIT',
        ],
        'ARCH_HUM': [
            'SUB-HUM-HIST', 'SUB-HUM-PHIL', 'SUB-HUM-ART-HIST',
            'SUB-HUM-ART-CREA', 'SUB-HUM-MUS', 'SUB-HUM-ANTH',
        ],
        'ARCH_HEALTH': [
            'SUB-SAN-MED-CLIN', 'SUB-SAN-MED-BASIC',
            'SUB-SAN-MED-FISIO-GEN', 'SUB-SAN-MED-FISIO-NEURO',
            'SUB-SAN-CUID', 'SUB-SAN-ODON', 'SUB-SAN-FISIO',
            'SUB-SAN-BIOQUIM', 'SUB-SAN-FARM',
            'SUB-SAN-PSY-DIAG', 'SUB-SAN-PSY-EVAL',
            'SUB-SAN-PSY-MET', 'SUB-SAN-PSY-STAT',
            'SUB-SAN-VET-CLIN', 'SUB-SAN-VET-CIR',
            'SUB-SAN-NUT-DIET', 'SUB-SAN-NUT-BROM', 'SUB-SAN-NUT-SPUB',
        ],
        'ARCH_SOC': [
            'SUB-SOC-LAW-PROC-CIV', 'SUB-SOC-LAW-PROC-PEN',
            'SUB-SOC-LAW-DICT-CIV', 'SUB-SOC-LAW-DICT-PEN',
            'SUB-SOC-ECON-QUAN-STAT', 'SUB-SOC-ECON-QUAN-ECON',
            'SUB-SOC-ECON-MGMT-ACC', 'SUB-SOC-ECON-MGMT-STR', 'SUB-SOC-ECON-MGMT-ECO',
            'SUB-SOC-EDU-KIDS', 'SUB-SOC-EDU-SEC',
            'SUB-SOC-COMM-JOUR', 'SUB-SOC-COMM-AV',
            'SUB-SOC-GEOG-SIG', 'SUB-SOC-GEOG-TER', 'SUB-SOC-GEOG-FIS',
            'SUB-SOC-WORK-INT', 'SUB-SOC-WORK-POL', 'SUB-SOC-WORK-MED',
        ],
        'ARCH_TECH': [
            'SUB-TEC-SOFT-ALG', 'SUB-TEC-SOFT-DS', 'SUB-TEC-SOFT-SE',
            'SUB-TEC-CIVIL-STRUCT', 'SUB-TEC-CIVIL-CONC', 'SUB-TEC-CIVIL-STEEL',
            'SUB-TEC-INDUS-THERMO', 'SUB-TEC-INDUS-TMM', 'SUB-TEC-INDUS-DEM',
            'SUB-TEC-CHEM-BAL', 'SUB-TEC-CHEM-REACT',
            'SUB-TEC-PROJ-ARCH', 'SUB-TEC-PROJ-URB',
            'SUB-TEC-CONS-TECH', 'SUB-TEC-CONS-MAN',
            'SUB-TEC-PURE-ANAL', 'SUB-TEC-PURE-ALGSTR',
        ],
        'ARCH_SCI': [
            'SUB-SCI-BIO-GEN', 'SUB-SCI-BIO-ZOO', 'SUB-SCI-BIO-ECO',
            'SUB-SCI-CHEM-ORG', 'SUB-SCI-CHEM-INORG',
            'SUB-SCI-PHYS-EM', 'SUB-SCI-PHYS-QM',
            'SUB-SCI-GEOL-MIN', 'SUB-SCI-GEOL-STRAT', 'SUB-SCI-GEOL-MAP',
            'SUB-SCI-ENV-RES', 'SUB-SCI-ENV-CONT',
            'SUB-SCI-DATA-STAT', 'SUB-SCI-DATA-ML', 'SUB-SCI-DATA-BIG',
        ],
    }

    # Mapa inverso subarquetipo → arquetipo para búsqueda rápida
    # Reverse map sub-archetype → archetype for fast lookup
    _SUB_TO_ARCH = {
        sub: arch
        for arch, subs in CERTIFIED_SUB_ARCHETYPES.items()
        for sub in subs
    }

    def rotate_api_key(self):
        """
        Rotates to the next available non-quarantined API key.
        Returns True if rotation was successful, False if no keys are available.
        ---
        Rota a la siguiente clave API disponible no en cuarentena.
        Devuelve True si la rotación fue exitosa, False si no hay claves disponibles.
        """
        settings = AutomationSettings.load()
        current_key = settings.active_api_key
        next_key = ApiKey.objects.filter(
            is_enabled=True, is_quarantined=False
        ).exclude(
            id=current_key.id if current_key else None
        ).first()
        if next_key:
            settings.active_api_key = next_key
            settings.save()
            self.stdout.write(self.style.WARNING(
                f"      [ROTACIÓN] Usando nueva llave: {next_key.name}"
            ))
            return True
        return False

    def _find_subject_for_sub_archetype(self, sub_arch, arch):
        """
        Searches for a real subject in the database already classified under this
        sub-archetype by querying subjects that have generated material and then
        asking AcademicDeductor (with caching via metadata['sub_archetype_id']).
        Strategy: sample up to SAMPLE_LIMIT subjects with material from subjects
        whose branch/degree name hints at the archetype family, then classify.
        Returns (subject, material, metadata) or (None, None, None) if not found.
        ---
        Busca una asignatura real en BD ya clasificada bajo este subarquetipo,
        consultando asignaturas que tienen material generado y preguntando al
        AcademicDeductor (con caché via metadata['sub_archetype_id']).
        Estrategia: muestrear hasta SAMPLE_LIMIT asignaturas con material del
        arquetipo correspondiente, luego clasificar.
        Devuelve (asignatura, material, metadata) o (None, None, None) si no encontrado.
        """
        # Palabras clave por arquetipo para prefiltar en BD sin IA
        # Archetype keyword hints to pre-filter in DB without AI
        ARCH_KEYWORDS = {
            'ARCH_LANG':   ['lengua', 'idioma', 'traducción', 'filología', 'lingüística',
                            'francés', 'inglés', 'alemán', 'japonés', 'árabe', 'italiano',
                            'portugués', 'chino', 'ruso', 'literatura'],
            'ARCH_HUM':    ['historia', 'filosofía', 'arte', 'música', 'antropología',
                            'arqueología', 'bellas artes', 'patrimonio', 'humanidades'],
            'ARCH_HEALTH': ['medicina', 'enfermería', 'farmacología', 'anatomía',
                            'fisiología', 'bioquímica', 'psicología', 'veterinaria',
                            'nutrición', 'dietética', 'odontología', 'fisioterapia',
                            'salud', 'clínica', 'quirúrgica'],
            'ARCH_SOC':    ['derecho', 'economía', 'sociología', 'trabajo social',
                            'educación', 'pedagogía', 'periodismo', 'comunicación',
                            'geografía', 'ciencias políticas', 'relaciones laborales',
                            'contabilidad', 'empresa', 'administración'],
            'ARCH_TECH':   ['ingeniería', 'informática', 'computación', 'algorítmica',
                            'software', 'civil', 'industrial', 'química', 'arquitectura',
                            'construcción', 'estructuras', 'matemáticas', 'cálculo',
                            'álgebra', 'análisis matemático'],
            'ARCH_SCI':    ['biología', 'química', 'física', 'geología', 'ecología',
                            'genética', 'zoología', 'botánica', 'estadística',
                            'mineralogía', 'estratigrafía', 'cartografía',
                            'medioambiente', 'ciencias de datos', 'aprendizaje automático'],
        }

        SAMPLE_LIMIT = 30  # máximo de asignaturas a clasificar por subarquetipo

        keywords = ARCH_KEYWORDS.get(arch, [])

        # Construir queryset de asignaturas con material y keywords de arquetipo
        # Build queryset of subjects with material and archetype keywords
        from django.db.models import Q
        keyword_filter = Q()
        for kw in keywords:
            keyword_filter |= Q(name__icontains=kw)

        candidates = (
            Subject.objects
            .filter(keyword_filter)
            .filter(content_materials__isnull=False)
            .distinct()
            .order_by('?')  # muestra aleatoria / random sample
        )[:SAMPLE_LIMIT]

        for subject in candidates:
            material = subject.content_materials.first()
            if not material:
                continue
            try:
                metadata = AcademicDeductor.get_context_metadata(subject)
                if metadata.get('sub_archetype_id') == sub_arch:
                    return subject, material, metadata
            except Exception:
                continue

        return None, None, None

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(
            "\n=== VALIDACIÓN V06: PROTOCOLO DE RESILIENCIA EXTREMA ==="
        ))
        self.stdout.write(
            "    Modo: búsqueda dinámica en BD (~2.500 asignaturas disponibles).\n"
            "    No se poblan datos. SKIP si el subarquetipo no tiene asignatura con material aún.\n"
        )

        connection.ensure_connection()
        temp_user, _ = CustomUser.objects.get_or_create(
            username='tester_v06_final',
            defaults={'email': 'final@v06.com'}
        )

        success_count = 0
        skip_count    = 0
        fail_count    = 0

        all_sub_archetypes = [
            (arch, sub)
            for arch, subs in self.CERTIFIED_SUB_ARCHETYPES.items()
            for sub in subs
        ]
        total = len(all_sub_archetypes)

        for i, (arch, sub_arch) in enumerate(all_sub_archetypes, 1):
            self.stdout.write(f"\n[{i}/{total}] PROCESANDO: {sub_arch} (arquetipo: {arch})")

            try:
                # 1. LOCALIZACIÓN DINÁMICA — buscar asignatura real en BD
                #    DYNAMIC LOCATION — find real subject in DB
                connection.ensure_connection()
                self.stdout.write(f"      [BD] Buscando asignatura representativa...", ending="")

                subject, material, metadata = self._find_subject_for_sub_archetype(sub_arch, arch)

                if not subject:
                    self.stdout.write(self.style.WARNING(
                        f" SKIP — ninguna asignatura con material clasificada como {sub_arch} en BD."
                    ))
                    skip_count += 1
                    continue

                self.stdout.write(self.style.SUCCESS(
                    f" OK → '{subject.name}' | sub: {metadata['sub_archetype_id']}"
                ))

                # 2. INSTANCIAR STRATEGY Y VALIDAR SKELETON
                #    INSTANTIATE STRATEGY AND VALIDATE SKELETON
                with transaction.atomic():
                    connection.ensure_connection()
                    ContentCopy.objects.filter(user=temp_user, subject_context=subject).delete()
                    copy = ContentCopy.objects.create(
                        original_content=material,
                        user=temp_user,
                        subject_context=subject,
                        html_content="Validated"
                    )

                    strategy = ExamFactory.get_strategy(
                        archetype_id      = arch,
                        sub_archetype_id  = sub_arch,
                        pedagogical_level = metadata.get('pedagogical_level', 'LVL_B'),
                        itinerary_id      = metadata.get('itinerary_id', 'ITIN_MIN'),
                    )

                    # CORRECCIÓN TIPO A: usar get_exam_skeleton() — API real de BaseExamStrategy
                    # TYPE A FIX: use get_exam_skeleton() — actual BaseExamStrategy API
                    skeleton = strategy.get_exam_skeleton()

                    if not skeleton:
                        raise ValueError(
                            f"get_exam_skeleton() devolvió lista vacía para {sub_arch}."
                        )

                    exam = Exam.objects.create(
                        user             = temp_user,
                        content_copy     = copy,
                        archetype_id     = arch,
                        sub_archetype_id = sub_arch,
                        status           = 'READY'
                    )

                    for idx, section in enumerate(skeleton):
                        ExamSection.objects.create(
                            exam           = exam,
                            subdivision_id = section['subdivision_id'],
                            title          = section['title'],
                            order          = idx
                        )

                    self.stdout.write(self.style.SUCCESS(
                        f"      [DB] ÉXITO: {len(skeleton)} secciones integradas."
                    ))
                    success_count += 1

                # Cadencia de seguridad anti-throttling
                # Anti-throttling safety cadence
                self.stdout.write("      [RELOJ] Cadencia 10s...")
                time.sleep(10)

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"      [!] FALLO CRÍTICO: {e}"
                ))
                fail_count += 1
                connection.close()

        # Limpieza del usuario temporal / Cleanup temp user
        try:
            temp_user.delete()
        except Exception:
            pass

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\n=== RESUMEN VALIDACIÓN V06 ===\n"
            f"    ÉXITO : {success_count}/{total}\n"
            f"    SKIP  : {skip_count}/{total}  (subarquetipo sin asignatura en BD aún)\n"
            f"    FALLO : {fail_count}/{total}  (error de código o BD)\n"
            f"    TOTAL : {total} subarquetipos certificados\n"
        ))
