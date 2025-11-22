from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Limpia tablas obsoletas antes de la migración destructiva'

    def handle(self, *args, **options):
        tables_to_purge = [
            # Tablas hijas primero
            'contents_contentmaterial_topic', # Si existe
            'contents_topic',
            'contents_freecontenttopic',
            # Tablas intermedias
            'contents_maincategory',
            'contents_freecontentcategory',
            # Tablas padres
            'contents_discipline',
            'contents_knowledgearea',
        ]

        with connection.cursor() as cursor:
            # Desactivar chequeo de FK temporalmente para asegurar borrado
            cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
            
            for table in tables_to_purge:
                try:
                    self.stdout.write(f"Intentando vaciar {table}...")
                    cursor.execute(f"DELETE FROM {table}")
                    self.stdout.write(self.style.SUCCESS(f"✓ {table} vaciada."))
                except Exception as e:
                    # Si la tabla no existe (ya borrada o nombre incorrecto), ignoramos
                    if "1146" in str(e): # Table doesn't exist
                        self.stdout.write(self.style.WARNING(f"- La tabla {table} no existe, saltando."))
                    else:
                        self.stdout.write(self.style.ERROR(f"Error en {table}: {e}"))
            
            cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
            
        self.stdout.write(self.style.SUCCESS("Limpieza de tablas legacy completada."))
