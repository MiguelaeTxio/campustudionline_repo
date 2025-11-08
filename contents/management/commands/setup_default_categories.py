# /home/MiguelAeTxio/CampuStudiOnline/contents/management/commands/setup_default_categories.py
from django.core.management.base import BaseCommand
from django.db import transaction
from contents.models import KnowledgeArea, Discipline, MainCategory, Topic


class Command(BaseCommand):
    help = (
        'Asegura la existencia de la jerarquía de categorías por defecto ("General").'
    )

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Crea la jerarquía de categorías "General" si no existe,
        usando get_or_create para ser idempotente (seguro de ejecutar varias veces).
        """
        self.stdout.write(
            self.style.NOTICE("Iniciando la configuración de categorías por defecto...")
        )

        try:
            # Nivel 1: Área de Conocimiento
            area, created_area = KnowledgeArea.objects.get_or_create(
                name="General"
            )
            if created_area:
                self.stdout.write(
                    self.style.SUCCESS(" -> Creada Área de Conocimiento: General")
                )
            else:
                self.stdout.write(" -> Área de Conocimiento 'General' ya existía.")

            # Nivel 2: Disciplina
            discipline, created_discipline = Discipline.objects.get_or_create(
                name="General", knowledge_area=area
            )
            if created_discipline:
                self.stdout.write(self.style.SUCCESS(" -> Creada Disciplina: General"))
            else:
                self.stdout.write(" -> Disciplina 'General' ya existía.")

            # Nivel 3: Categoría Principal
            category, created_category = MainCategory.objects.get_or_create(
                name="General", discipline=discipline
            )
            if created_category:
                self.stdout.write(
                    self.style.SUCCESS(" -> Creada Categoría Principal: General")
                )
            else:
                self.stdout.write(" -> Categoría Principal 'General' ya existía.")

            # Nivel 4: Tema (Raíz)
            topic, created_topic = Topic.objects.get_or_create(
                name="General", main_category=category
            )
            if created_topic:
                self.stdout.write(self.style.SUCCESS(" -> Creado Tema Raíz: General"))
            else:
                self.stdout.write(" -> Tema Raíz 'General' ya existía.")

            self.stdout.write(
                self.style.SUCCESS(
                    "\nConfiguración de categorías por defecto completada exitosamente."
                )
            )

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Ocurrió un error inesperado: {e}"))
            raise
