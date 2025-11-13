# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/content_automation/management/commands/correct_academic_classification.py (V2)
import logging
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Count
from django.utils.text import slugify

from contents.models import ContentMaterial, KnowledgeArea, Discipline, MainCategory, Topic
from academic_structure.models import Subject

# Configurar un logger específico para este comando
logger = logging.getLogger('datacorrection')

class Command(BaseCommand):
    """
    (V2) Comando de gestión para corregir la clasificación de contenidos académicos.
    Incluye lógica para detectar, fusionar y eliminar Topics duplicados antes de
    la corrección para manejar inconsistencias en los datos.
    """
    help = "(V2) Corrige la clasificación de todos los ContentMaterial académicos y fusiona duplicados."

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Ejecuta el script en modo simulación sin aplicar cambios a la base de datos.'
        )
        parser.add_argument(
            '--no-cleanup',
            action='store_true',
            help='Evita el proceso de limpieza de categorías huérfanas después de la corrección.'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        no_cleanup = options['no_cleanup']
        
        if dry_run:
            self.stdout.write(self.style.WARNING("--- MODO SIMULACIÓN (DRY-RUN) ACTIVADO ---"))
            self.stdout.write(self.style.WARNING("No se realizarán cambios en la base de datos.\n"))
        else:
            self.stdout.write(self.style.SUCCESS("--- MODO EJECUCIÓN REAL ---"))
            self.stdout.write(self.style.WARNING("Los cambios se aplicarán a la base de datos.\n"))

        # --- FASE 1: CORRECCIÓN DE CLASIFICACIONES ---
        self.stdout.write(self.style.NOTICE("[FASE 1/2] Iniciando corrección de clasificaciones..."))

        academic_contents = ContentMaterial.objects.filter(is_free_content=False)
        total_contents = academic_contents.count()
        
        if total_contents == 0:
            self.stdout.write(self.style.SUCCESS("No se encontraron contenidos académicos para procesar. La base de datos está limpia."))
            return

        self.stdout.write(f"Se encontraron {total_contents} ContentMaterial académicos para procesar.")
        
        corrected_count = 0
        error_count = 0
        
        original_topics_to_check = set()

        for content in academic_contents.iterator():
            first_subject = content.subject.first()
            if not first_subject:
                self.stdout.write(self.style.ERROR(f"  -> ERROR: El contenido '{content.title}' (PK: {content.pk}) no tiene ninguna asignatura asociada. Se omite."))
                error_count += 1
                continue
            
            if content.topic:
                original_topics_to_check.add(content.topic)

            try:
                # 1. Crear/Obtener la jerarquía superior (Area, Discipline, MainCategory)
                academic_year = first_subject.academic_year
                degree = academic_year.degree
                branch = degree.branch
                
                area, _ = KnowledgeArea.objects.get_or_create(
                    name=branch.name, defaults={'slug': slugify(branch.name)}
                )
                discipline, _ = Discipline.objects.get_or_create(
                    knowledge_area=area, name=degree.name, defaults={'slug': slugify(f"{area.name}-{degree.name}")}
                )
                main_cat_name = f"{academic_year.year}º Curso"
                main_cat, _ = MainCategory.objects.get_or_create(
                    discipline=discipline, name=main_cat_name, defaults={'slug': slugify(f"{discipline.name}-{main_cat_name}")}
                )
                
                # 2. Lógica robusta para manejar Topics duplicados
                subject_name = first_subject.name
                candidate_topics = Topic.objects.filter(name=subject_name, main_category=main_cat)
                
                target_topic = None
                if candidate_topics.count() > 1:
                    self.stdout.write(self.style.WARNING(f"    -> DUPLICADO DETECTADO: {candidate_topics.count()} Topics para '{subject_name}'. Fusionando..."))
                    target_topic = candidate_topics.first()
                    duplicates_to_delete = candidate_topics.exclude(pk=target_topic.pk)
                    
                    # Re-mapear cualquier contenido que apunte a los duplicados
                    contents_to_remap = ContentMaterial.objects.filter(topic__in=duplicates_to_delete)
                    if contents_to_remap.exists():
                        self.stdout.write(f"      -> Re-mapeando {contents_to_remap.count()} contenido(s) al Topic canónico.")
                        if not dry_run:
                            contents_to_remap.update(topic=target_topic)
                    
                    if not dry_run:
                        duplicates_to_delete.delete()

                elif candidate_topics.count() == 1:
                    target_topic = candidate_topics.first()
                else: # No existe el topic
                    if not dry_run:
                        target_topic = Topic.objects.create(main_category=main_cat, name=subject_name)
                
                # 3. Aplicar la corrección
                if content.topic != target_topic:
                    self.stdout.write(f"  -> CORRIGIENDO: '{content.title}' -> Nuevo Topic PK: {target_topic.pk if target_topic else 'Será creado'}")
                    if not dry_run:
                        content.topic = target_topic
                        content.save(update_fields=['topic'])
                    corrected_count += 1
                else:
                    self.stdout.write(f"  -> VERIFICADO: '{content.title}' ya está clasificado correctamente. Se omite.")

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  -> ERROR INESPERADO procesando '{content.title}': {e}"))
                error_count += 1
                logger.exception(f"Error procesando {content.title}")

        self.stdout.write(self.style.SUCCESS(f"\n[FASE 1/2] Finalizada. {corrected_count} contenidos corregidos, {error_count} errores."))

        # --- FASE 2: LIMPIEZA DE CATEGORÍAS HUÉRFANAS ---
        if no_cleanup:
            self.stdout.write(self.style.WARNING("\nSe ha omitido la fase de limpieza de categorías huérfanas (--no-cleanup)."))
        else:
            self.stdout.write(self.style.NOTICE("\n[FASE 2/2] Iniciando limpieza de categorías huérfanas..."))
            self._perform_cleanup(original_topics_to_check, dry_run)

        if dry_run:
            self.stdout.write(self.style.WARNING("\n--- SIMULACIÓN FINALIZADA ---"))
            transaction.set_rollback(True) # Revertir la transacción en modo dry-run
        else:
            self.stdout.write(self.style.SUCCESS("\n--- CORRECCIÓN DE DATOS FINALIZADA ---"))

    def _perform_cleanup(self, topics_to_check, dry_run):
        """Limpia jerarquías intelectuales que hayan quedado sin contenidos."""
        topic_ids = {t.id for t in topics_to_check if t}
        topics = Topic.objects.filter(id__in=topic_ids).annotate(
            content_count=Count('content_materials')
        )
        cleaned_count = 0
        
        for topic in topics:
            if topic.content_count == 0:
                self.stdout.write(f"  -> LIMPIANDO Topic Huérfano: '{topic.name}'")
                if not dry_run:
                    try:
                        topic.delete()
                        cleaned_count += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"    -> Error al limpiar '{topic.name}': {e}"))
        
        self.stdout.write(self.style.SUCCESS(f"[FASE 2/2] Finalizada. Se limpiaron {cleaned_count} jerarquías huérfanas."))

