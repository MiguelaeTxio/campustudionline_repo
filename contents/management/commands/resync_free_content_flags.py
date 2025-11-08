# /home/MiguelAeTxio/CampuStudiOnline/contents/management/commands/resync_free_content_flags.py
from django.core.management.base import BaseCommand
from django.db import transaction
from contents.models import ContentMaterial, Topic, MainCategory, Discipline, KnowledgeArea

class Command(BaseCommand):
    help = 'Recalcula y sincroniza todos los flags "has_free_content" en toda la jerarquía de contenidos.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Iniciando el proceso de resincronización de flags de contenido libre..."))

        # Paso 1: Resetear todos los flags a False. Es la forma más segura de empezar.
        self.stdout.write("Paso 1/3: Reseteando todos los flags existentes a False...")
        updated_ka = KnowledgeArea.objects.update(has_free_content=False)
        updated_d = Discipline.objects.update(has_free_content=False)
        updated_mc = MainCategory.objects.update(has_free_content=False)
        updated_t = Topic.objects.update(has_free_content=False)
        self.stdout.write(f" -> {updated_ka} Áreas, {updated_d} Disciplinas, {updated_mc} Categorías, {updated_t} Temas reseteados.")

        # Paso 2: Identificar la única fuente de verdad: los materiales marcados como libres.
        self.stdout.write("Paso 2/3: Identificando la jerarquía de los materiales genuinamente libres...")
        free_materials = ContentMaterial.objects.filter(is_free_content=True).select_related(
            'topic__main_category__discipline__knowledge_area'
        )
        
        if not free_materials.exists():
            self.stdout.write(self.style.SUCCESS("No se encontraron materiales de contenido libre. La base de datos está limpia. Proceso finalizado."))
            return

        nodes_to_update = {
            'knowledge_areas': set(),
            'disciplines': set(),
            'main_categories': set(),
            'topics': set()
        }

        # Paso 3: Recorrer cada material libre y marcar su jerarquía ascendente.
        for material in free_materials:
            current_topic = material.topic
            while current_topic:
                nodes_to_update['topics'].add(current_topic.pk)
                # Navegar hacia arriba en la jerarquía de Topic
                if current_topic.main_category:
                    nodes_to_update['main_categories'].add(current_topic.main_category.pk)
                    nodes_to_update['disciplines'].add(current_topic.main_category.discipline.pk)
                    nodes_to_update['knowledge_areas'].add(current_topic.main_category.discipline.knowledge_area.pk)
                    break 
                current_topic = current_topic.parent
        
        self.stdout.write(f" -> {len(free_materials)} materiales libres encontrados. Propagando flags hacia arriba...")

        # Aplicar las actualizaciones de forma masiva para eficiencia
        if nodes_to_update['knowledge_areas']:
            KnowledgeArea.objects.filter(pk__in=nodes_to_update['knowledge_areas']).update(has_free_content=True)
        if nodes_to_update['disciplines']:
            Discipline.objects.filter(pk__in=nodes_to_update['disciplines']).update(has_free_content=True)
        if nodes_to_update['main_categories']:
            MainCategory.objects.filter(pk__in=nodes_to_update['main_categories']).update(has_free_content=True)
        if nodes_to_update['topics']:
            Topic.objects.filter(pk__in=nodes_to_update['topics']).update(has_free_content=True)
        
        self.stdout.write(self.style.SUCCESS("Paso 3/3: Actualización completada."))
        self.stdout.write(self.style.SUCCESS(f"Total de nodos marcados como 'con contenido libre': "
                                            f"{len(nodes_to_update['knowledge_areas'])} Áreas, "
                                            f"{len(nodes_to_update['disciplines'])} Disciplinas, "
                                            f"{len(nodes_to_update['main_categories'])} Categorías, "
                                            f"{len(nodes_to_update['topics'])} Temas."))

        self.stdout.write(self.style.SUCCESS("\n¡Resincronización finalizada con éxito! Los datos de la jerarquía ahora son consistentes."))
