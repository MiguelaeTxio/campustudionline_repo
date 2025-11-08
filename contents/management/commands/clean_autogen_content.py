# /home/MiguelAeTxio/CampuStudiOnline/contents/management/commands/clean_autogen_content.py
from django.core.management.base import BaseCommand
from django.db import transaction
from contents.models import KnowledgeArea, ContentMaterial

class Command(BaseCommand):
    help = 'Limpia la categoría "Contenido Autogenerado" moviendo su contenido a una categoría correcta.'

    def handle(self, *args, **options):
        incorrect_name = "Contenido Autogenerado"
        correct_name = "Contenidos en CampuStudiOnline"
        try:
            incorrect_area = KnowledgeArea.objects.get(name=incorrect_name)
        except KnowledgeArea.DoesNotExist:
            self.stdout.write(self.style.SUCCESS(f"No se encontró el área incorrecta ('{incorrect_name}'). No se requiere acción."))
            return

        correct_area, _ = KnowledgeArea.objects.get_or_create(name=correct_name)
        
        with transaction.atomic():
            materials_to_move = ContentMaterial.objects.filter(topic__main_category__discipline__knowledge_area=incorrect_area)
            for material in materials_to_move:
                original_topic = material.topic
                if not original_topic: continue
                correct_discipline, _ = correct_area.disciplines.get_or_create(name=original_topic.main_category.discipline.name)
                correct_category, _ = correct_discipline.main_categories.get_or_create(name=original_topic.main_category.name)
                correct_topic, _ = correct_category.root_topics.get_or_create(name=original_topic.name, defaults={"parent": None})
                material.topic = correct_topic
                material.save(update_fields=["topic"])
            
            if not ContentMaterial.objects.filter(topic__main_category__discipline__knowledge_area=incorrect_area).exists():
                incorrect_area.delete()
                self.stdout.write(self.style.SUCCESS(f"Área incorrecta '{incorrect_name}' eliminada."))
