# /home/MiguelAeTxio/CampuStudiOnline/contents/management/commands/ensure_free_content_structure.py
from django.core.management.base import BaseCommand
from django.db import transaction
from contents.models import KnowledgeArea, Discipline

class Command(BaseCommand):
    help = 'Asegura que la estructura jerárquica para el contenido libre exista en la base de datos.'

    REQUIRED_DISCIPLINES = [
        'Historia de la Música',
        'Biografías',
        'Formación Profesional',
        'Desarrollo Personal',
        'General'
    ]
    ROOT_AREA_NAME = 'Contenidos en CampuStudiOnline'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"--- Iniciando verificación de la estructura para Contenido Libre ---"))

        # 1. Asegurar que el Área de Conocimiento raíz exista.
        root_area, created = KnowledgeArea.objects.get_or_create(name=self.ROOT_AREA_NAME)
        if created:
            self.stdout.write(f"  [+] Creada Área de Conocimiento raíz: '{self.ROOT_AREA_NAME}'")
        else:
            self.stdout.write(f"  [*] El Área de Conocimiento raíz '{self.ROOT_AREA_NAME}' ya existe.")

        # 2. Iterar y asegurar que cada Disciplina requerida exista.
        created_count = 0
        existing_count = 0
        for discipline_name in self.REQUIRED_DISCIPLINES:
            discipline, created = Discipline.objects.get_or_create(
                knowledge_area=root_area,
                name=discipline_name
            )
            if created:
                self.stdout.write(f"    [+] Creada Disciplina: '{discipline_name}'")
                created_count += 1
            else:
                existing_count += 1
        
        if existing_count > 0:
            self.stdout.write(f"\n  [*] {existing_count} Disciplinas requeridas ya existían.")

        self.stdout.write(self.style.SUCCESS(f"\n--- Verificación completada. {created_count} nuevas Disciplinas creadas. ---"))
