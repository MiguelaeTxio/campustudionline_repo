# /users/management/commands/setup_groups.py
# ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from academic_structure.models import University, Branch, Degree, Subject
from orchestrator.models import PendingContentTask


class Command(BaseCommand):
    """
    Crea el grupo de 'Colaboradores' y le asigna todos los permisos
    necesarios para gestionar la aplicación 'academic_structure'.
    """

    help = "Crea el grupo de Colaboradores con los permisos necesarios para la app academic_structure."

    def handle(self, *args, **options):
        GROUP_NAME = "Colaboradores"

        # 1. Crear el grupo si no existe
        group, created = Group.objects.get_or_create(name=GROUP_NAME)
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Grupo '{GROUP_NAME}' creado exitosamente.")
            )
        else:
            self.stdout.write(self.style.WARNING(f"Grupo '{GROUP_NAME}' ya existía."))

        # 2. Definir los modelos de 'academic_structure' para los que se necesitan permisos
        models_to_permit = [University, Branch, Degree, Subject, PendingContentTask]

        # 3. Recolectar todos los permisos para esos modelos
        permissions = []
        for model in models_to_permit:
            content_type = ContentType.objects.get_for_model(model)
            model_permissions = Permission.objects.filter(content_type=content_type)
            permissions.extend(model_permissions)
            self.stdout.write(
                f"  - Obteniendo {model_permissions.count()} permisos para el modelo '{model._meta.verbose_name}'"
            )

        # 4. Asignar la lista completa de permisos al grupo
        group.permissions.set(permissions)

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSe han asignado/actualizado {len(permissions)} permisos al grupo '{GROUP_NAME}'."
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "El grupo 'Colaboradores' está configurado correctamente."
            )
        )
