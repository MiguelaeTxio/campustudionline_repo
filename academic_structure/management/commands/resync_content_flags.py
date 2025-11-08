from django.core.management.base import BaseCommand
from django.db.models import Exists, OuterRef
from django.db import transaction
from academic_structure.models import University, Branch, Degree, AcademicYear, Subject
from contents.models import ContentMaterial

class Command(BaseCommand):
    help = 'Recalculates and synchronizes the `has_public_content` flag across the entire academic hierarchy.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Iniciando la resincronización de los flags 'has_public_content'..."))

        with transaction.atomic():
            # Nivel 1: Asignaturas (La fuente de verdad)
            self.stdout.write("Nivel 1: Actualizando Asignaturas (Subjects)...")
            
            # [CORRECCIÓN] Se usa el nombre de campo correcto 'subject' (singular) en lugar de 'subjects'.
            public_content_exists = ContentMaterial.objects.filter(
                subject=OuterRef('pk'), 
                is_public=True
            )
            
            updated_subjects_true = Subject.objects.annotate(
                has_public=Exists(public_content_exists)
            ).filter(has_public=True).exclude(has_public_content=True).update(has_public_content=True)
            
            updated_subjects_false = Subject.objects.annotate(
                has_public=Exists(public_content_exists)
            ).filter(has_public=False).exclude(has_public_content=False).update(has_public_content=False)

            self.stdout.write(self.style.SUCCESS(f"  -> {updated_subjects_true} asignaturas marcadas CON contenido."))
            self.stdout.write(self.style.SUCCESS(f"  -> {updated_subjects_false} asignaturas marcadas SIN contenido."))

            # Propagación ascendente
            self.sync_parent_model(AcademicYear, 'subjects', "Años Académicos")
            self.sync_parent_model(Degree, 'academic_years', "Titulaciones")
            self.sync_parent_model(Branch, 'degrees', "Ramas de Conocimiento")
            self.sync_parent_model(University, 'branches', "Universidades")

        self.stdout.write(self.style.SUCCESS("¡Resincronización completada con éxito!"))

    def sync_parent_model(self, parent_model, child_relation_name, level_name):
        self.stdout.write(f"Sincronizando Nivel: {level_name}...")

        child_model = parent_model._meta.get_field(child_relation_name).related_model
        child_fk_name = parent_model._meta.get_field(child_relation_name).field.name

        child_with_content_exists = child_model.objects.filter(
            **{f'{child_fk_name}': OuterRef('pk')},
            has_public_content=True
        )

        updated_parents_true = parent_model.objects.annotate(
            has_child=Exists(child_with_content_exists)
        ).filter(has_child=True).exclude(has_public_content=True).update(has_public_content=True)

        updated_parents_false = parent_model.objects.annotate(
            has_child=Exists(child_with_content_exists)
        ).filter(has_child=False).exclude(has_public_content=False).update(has_public_content=False)
        
        self.stdout.write(self.style.SUCCESS(f"  -> {updated_parents_true} {level_name.lower()} marcados CON contenido."))
        self.stdout.write(self.style.SUCCESS(f"  -> {updated_parents_false} {level_name.lower()} marcados SIN contenido."))
