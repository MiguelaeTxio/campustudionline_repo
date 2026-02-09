# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_v2/management/commands/sync_subscriptions.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from assessment_v2.services.quotas import QuotaService

User = get_user_model()

class Command(BaseCommand):
    help = 'Sincroniza suscripciones para todos los usuarios existentes.'

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            QuotaService.get_or_create_default_subscription(user)
        self.stdout.write(self.style.SUCCESS('Sincronización completada.'))
