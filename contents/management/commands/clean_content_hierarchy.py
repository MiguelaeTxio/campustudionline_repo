# /home/MiguelAeTxio/CampuStudiOnline/contents/management/commands/clean_content_hierarchy.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from contents.models import KnowledgeArea, Discipline, MainCategory, Topic

class Command(BaseCommand):
    help = "Poda la jerarquía de categorías de contenido, eliminando nodos vacíos."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("--- Iniciando Proceso de Poda de Jerarquía ---"))
        total_pruned = 0
        while True:
            pruned_in_pass = 0
            empty_leaf_topics = Topic.objects.annotate(subtopic_count=Count('subtopics'), content_count=Count('content_materials')).filter(subtopic_count=0, content_count=0)
            count, _ = empty_leaf_topics.delete()
            if count > 0:
                pruned_in_pass += count
            
            count, _ = MainCategory.objects.annotate(root_topic_count=Count('root_topics')).filter(root_topic_count=0).delete()
            if count > 0:
                pruned_in_pass += count

            count, _ = Discipline.objects.filter(main_categories__isnull=True).delete()
            if count > 0:
                pruned_in_pass += count

            count, _ = KnowledgeArea.objects.filter(disciplines__isnull=True).delete()
            if count > 0:
                pruned_in_pass += count

            if pruned_in_pass == 0:
                break
            else:
                total_pruned += pruned_in_pass
        self.stdout.write(self.style.SUCCESS(f"\n--- Proceso de Poda FINALIZADO. Total de {total_pruned} nodos eliminados. ---"))
