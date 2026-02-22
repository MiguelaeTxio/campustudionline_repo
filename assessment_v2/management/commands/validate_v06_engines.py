# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/management/commands/validate_v06_engines.py
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

# Silenciar logs para limpieza total en Android
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("google").setLevel(logging.ERROR)

class Command(BaseCommand):
    help = 'Validación V06 con rotación forzada y enfriamiento de 60s ante errores de cuota.'

    TARGETS = {
        'SUB-LIN-CERT': 'Lengua Francesa V',
        'SUB-LIN-PROF': 'Traducción Especializada',
        'SUB-LIN-LIT':  'Literatura española del Siglo de Oro',
        'SUB-SAN-MED':  'Bases de la Medicina Interna II',
        'SUB-SAN-CUID': 'Enfermería del Adulto',
        'SUB-SAN-BIO':  'Farmacología aplicada',
        'SUB-SAN-PSY':  'Psicometría',
        'SUB-SAN-VET':  'Zoología',
        'SUB-TEC-SOFT': 'Algorítmica',
        'SUB-TEC-CIVIL':'Ingeniería Marítima',
        'SUB-TEC-INDUS':'Transmisión de Calor',
        'SUB-TEC-PURE': 'Métodos Numéricos',
        'SUB-TEC-CHEM': 'Operaciones de Separación',
        'SUB-SOC-JUR':  'Derecho del Trabajo y Seguridad Social',
        'SUB-SOC-ECON': 'Contabilidad Financiera',
        'SUB-SOC-BEHAV':'Sistema Político Español',
        'SUB-SOC-COMM': 'Teoría de la Comunicación',
        'SUB-HUM-HIST': 'Historia Universal Contemporánea I',
        'SUB-HUM-PHIL': 'La lógica y su filosofía',
        'SUB-HUM-EDU':  'Atención a la diversidad en el aula',
        'SUB-ART-CREA': 'Metodologías del dibujo',
        'SUB-ART-MUS':  'Historia de la música'
    }

    def rotate_api_key(self):
        settings = AutomationSettings.load()
        current_key = settings.active_api_key
        next_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).exclude(id=current_key.id if current_key else None).first()
        if next_key:
            settings.active_api_key = next_key
            settings.save()
            self.stdout.write(self.style.WARNING(f"      [ROTACIÓN] Usando nueva llave: {next_key.name}"))
            return True
        return False

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("\n=== VALIDACIÓN V06: PROTOCOLO DE RESILIENCIA EXTREMA ==="))
        
        connection.ensure_connection()
        temp_user, _ = CustomUser.objects.get_or_create(username='tester_v06_final', defaults={'email': 'final@v06.com'})
        
        success_count = 0
        total = len(self.TARGETS)

        for i, (sub_arch, query_name) in enumerate(self.TARGETS.items(), 1):
            start_time = time.time()
            self.stdout.write(f"\n[{i}/{total}] PROCESANDO: {sub_arch} ({query_name})")
            
            try:
                # 1. LOCALIZACIÓN
                connection.ensure_connection()
                subject = Subject.objects.filter(name__icontains=query_name).first()
                if not subject:
                    self.stdout.write(self.style.ERROR(f"      [!] ERROR: Asignatura no encontrada."))
                    continue
                
                material = subject.content_materials.first() or ContentMaterial.objects.filter(title__icontains=query_name).first()
                if not material:
                    self.stdout.write(self.style.ERROR(f"      [!] ERROR: Sin material generado."))
                    continue

                # 2. IA - CLASIFICACIÓN CON ENFRIAMIENTO Y ROTACIÓN
                metadata = None
                attempts = 2
                while attempts > 0:
                    try:
                        self.stdout.write(f"      [IA] Clasificando...", ending="")
                        metadata = AcademicDeductor.get_context_metadata(subject)
                        self.stdout.write(self.style.SUCCESS(f" OK ({metadata['archetype_id']})"))
                        break
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"\n      [!] INCIDENCIA IA: {e}"))
                        self.stdout.write(self.style.NOTICE("      [!] Activando Protocolo de Enfriamiento (60s)..."))
                        time.sleep(60) # Espera un minuto completo para resetear cuota de Google
                        if self.rotate_api_key():
                            attempts -= 1
                            self.stdout.write("      [!] Reintentando con nueva llave...")
                        else:
                            self.stdout.write(self.style.ERROR("      [!] No hay más llaves disponibles."))
                            break
                
                if not metadata: continue

                # 3. BASE DE DATOS - ESCRITURA AISLADA
                with transaction.atomic():
                    connection.ensure_connection()
                    ContentCopy.objects.filter(user=temp_user, subject_context=subject).delete()
                    copy = ContentCopy.objects.create(original_content=material, user=temp_user, subject_context=subject, html_content="Validated")
                    
                    m_map = {'SUB-LIN': 'ARCH_LANG', 'SUB-SAN': 'ARCH_HEALTH', 'SUB-TEC': 'ARCH_TECH', 'SUB-SOC': 'ARCH_SOC', 'SUB-HUM': 'ARCH_HUM', 'SUB-ART': 'ARCH_HUM'}
                    arch = m_map.get(sub_arch[:7], 'ARCH_LANG')
                    
                    strategy = ExamFactory.get_strategy(archetype_id=arch, sub_archetype_id=sub_arch)
                    exam = Exam.objects.create(user=temp_user, content_copy=copy, archetype_id=arch, sub_archetype_id=sub_arch, status='READY')
                    
                    plan = strategy.get_section_plan()
                    for idx, s in enumerate(plan):
                        ExamSection.objects.create(exam=exam, subdivision_id=s['subdivision_id'], title=s['title'], order=idx)
                    
                    self.stdout.write(self.style.SUCCESS(f"      [DB] ÉXITO: {len(plan)} secciones integradas."))
                    success_count += 1

                # CADENCIA DE SEGURIDAD (Minimiza riesgo de Throttling)
                self.stdout.write("      [RELOJ] Esperando 10 segundos de cadencia...")
                time.sleep(10)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"      [!] FALLO CRÍTICO EN ASIGNATURA: {e}"))
                connection.close()

        self.stdout.write(self.style.MIGRATE_HEADING(f"\n=== RESUMEN: {success_count}/{total} MOTORES VALIDADOS ==="))
        temp_user.delete()
