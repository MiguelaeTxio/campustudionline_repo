from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from users.models import RecommendationCode
import random
import string

class Command(BaseCommand):
    help = 'Genera un lote de códigos de recomendación únicos para un comercial específico.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nombre de usuario del Comercial (Vendor)')
        parser.add_argument('amount', type=int, help='Cantidad de códigos a generar')

    def handle(self, *args, **options):
        username = options['username']
        amount = options['amount']
        User = get_user_model()

        # 1. Validar Usuario
        try:
            vendor = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'Error: El usuario "{username}" no existe.')

        # 2. Advertencia de Grupo (no bloqueante, pero informativa)
        if not vendor.groups.filter(name='Comerciales').exists():
            self.stdout.write(self.style.WARNING(f'AVISO: El usuario "{username}" no pertenece al grupo "Comerciales".'))

        created_count = 0
        self.stdout.write(f"Iniciando generación de {amount} códigos para {vendor.username}...")

        # 3. Generación
        chars = string.ascii_uppercase + string.digits
        
        for _ in range(amount):
            attempts = 0
            while True:
                code = ''.join(random.choices(chars, k=4))
                if not RecommendationCode.objects.filter(code=code).exists():
                    RecommendationCode.objects.create(
                        code=code,
                        vendor=vendor
                    )
                    created_count += 1
                    break
                
                attempts += 1
                if attempts > 100:
                    raise CommandError("No se pudieron generar códigos únicos. El espacio de nombres podría estar saturado.")

        self.stdout.write(self.style.SUCCESS(f'ÉXITO: Se han generado y asignado {created_count} nuevos códigos a {vendor.username}.'))
