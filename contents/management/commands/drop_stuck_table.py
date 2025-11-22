from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Elimina la tabla contents_userstudynavigation que bloquea la migración'

    def handle(self, *args, **options):
        table = 'contents_userstudynavigation'
        with connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            try:
                self.stdout.write(f"Intentando eliminar {table}...")
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                self.stdout.write(self.style.SUCCESS(f"✓ {table} eliminada."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error: {e}"))
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
