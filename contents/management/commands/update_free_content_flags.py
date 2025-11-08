from django.core.management.base import BaseCommand
from django.db import transaction
from contents.models import ContentMaterial, Topic, MainCategory, Discipline, KnowledgeArea

class Command(BaseCommand):
    help = (
        "Synchronizes the 'has_free_content' flag for all intellectual "
        "hierarchy models based on existing public, non-academic content."
    )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("Starting synchronization of 'has_free_content' flags...")
        )

        with transaction.atomic():
            # Paso 1: Reiniciar todos los flags a False para un estado limpio.
            self.stdout.write("--> Resetting all flags to False...")
            KnowledgeArea.objects.all().update(has_free_content=False)
            Discipline.objects.all().update(has_free_content=False)
            MainCategory.objects.all().update(has_free_content=False)
            Topic.objects.all().update(has_free_content=False)
            self.stdout.write("    Done.")

            # Paso 2: Identificar todo el contenido libre y público.
            free_materials = ContentMaterial.objects.filter(
                subjects__isnull=True, is_public=True
            ).select_related("topic")
            
            if not free_materials.exists():
                self.stdout.write(self.style.WARNING("No free public content found. Synchronization finished."))
                return

            self.stdout.write(f"--> Found {free_materials.count()} free public materials to process.")

            # Paso 3: Recolectar todos los nodos de la jerarquía que deben ser marcados.
            topics_to_update = set()
            main_categories_to_update = set()
            disciplines_to_update = set()
            knowledge_areas_to_update = set()

            for material in free_materials:
                topic = material.topic
                if not topic:
                    continue

                # Marcar toda la cadena de Topics padres
                current_topic = topic
                while current_topic:
                    topics_to_update.add(current_topic.pk)
                    current_topic = current_topic.parent

                # Marcar la jerarquía superior
                root_category = topic.get_root_category()
                if root_category:
                    main_categories_to_update.add(root_category.pk)
                    disciplines_to_update.add(root_category.discipline.pk)
                    knowledge_areas_to_update.add(root_category.discipline.knowledge_area.pk)

            # Paso 4: Actualizar los flags en la base de datos de forma masiva.
            self.stdout.write("--> Applying 'True' flag to relevant hierarchy nodes...")
            if knowledge_areas_to_update:
                KnowledgeArea.objects.filter(pk__in=knowledge_areas_to_update).update(has_free_content=True)
                self.stdout.write(f"    Updated {len(knowledge_areas_to_update)} Knowledge Areas.")

            if disciplines_to_update:
                Discipline.objects.filter(pk__in=disciplines_to_update).update(has_free_content=True)
                self.stdout.write(f"    Updated {len(disciplines_to_update)} Disciplines.")

            if main_categories_to_update:
                MainCategory.objects.filter(pk__in=main_categories_to_update).update(has_free_content=True)
                self.stdout.write(f"    Updated {len(main_categories_to_update)} Main Categories.")

            if topics_to_update:
                Topic.objects.filter(pk__in=topics_to_update).update(has_free_content=True)
                self.stdout.write(f"    Updated {len(topics_to_update)} Topics.")

        self.stdout.write(
            self.style.SUCCESS("\nSynchronization complete. 'has_free_content' flags are now up to date.")
        )
