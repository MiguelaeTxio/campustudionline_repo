from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Lista las tablas existentes de la app contents para sincronizar la migración'

    def handle(self, *args, **options):
        legacy_targets = [
            'contents_knowledgearea',
            'contents_discipline',
            'contents_maincategory',
            'contents_topic',
            'contents_freecontentcategory',
            'contents_freecontenttopic',
            'contents_contentmaterial_topic', # Tabla M2M oculta antigua
        ]
        
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE 'contents_%'")
            existing_tables = [row[0] for row in cursor.fetchall()]

        self.stdout.write(self.style.WARNING("ESTADO ACTUAL DE TABLAS LEGACY:"))
        found_any = False
        for target in legacy_targets:
            if target in existing_tables:
                self.stdout.write(self.style.ERROR(f"[EXISTE] {target}"))
                found_any = True
            else:
                self.stdout.write(self.style.SUCCESS(f"[BORRADA] {target}"))
        
        if not found_any:
             self.stdout.write(self.style.SUCCESS("\n¡TODAS LAS TABLAS LEGACY HAN SIDO BORRADAS!"))

