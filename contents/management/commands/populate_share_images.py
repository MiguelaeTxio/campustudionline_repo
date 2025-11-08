# /home/MiguelAeTxio/CampuStudiOnline/contents/management/commands/populate_share_images.py
from django.core.management.base import BaseCommand
from django.db.models import Q
from contents.models import ContentMaterial
from contents.utils import generate_and_save_share_image


class Command(BaseCommand):
    """
    Comando de gestión para generar las imágenes de compartición para
    todos los objetos ContentMaterial que actualmente no la tengan.
    """

    help = "Genera las imágenes de compartición para todos los contenidos existentes que no la tengan."

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.NOTICE(
                "Iniciando la generación de imágenes de compartición para contenidos existentes..."
            )
        )

        materials_without_image = ContentMaterial.objects.filter(
            Q(share_image__isnull=True) | Q(share_image="")
        )

        total_to_process = materials_without_image.count()

        if total_to_process == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    "¡Perfecto! Todos los contenidos ya tienen su imagen de compartición. No se requiere ninguna acción."
                )
            )
            return

        self.stdout.write(
            f"Se han encontrado {total_to_process} contenidos que necesitan una imagen."
        )

        successfully_generated = 0
        errors = 0
        for i, material in enumerate(materials_without_image.order_by("id")):
            self.stdout.write(
                f'  Procesando material {i + 1}/{total_to_process}: "{material.title}" (ID: {material.id})...',
                ending="",
            )
            try:
                generate_and_save_share_image(material)
                self.stdout.write(self.style.SUCCESS(" OK"))
                successfully_generated += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f" ¡FALLÓ! Error: {e}"))
                errors += 1

        self.stdout.write(self.style.NOTICE("\n" + ("-" * 50)))
        self.stdout.write(self.style.SUCCESS(f"Proceso completado."))
        self.stdout.write(f" -> Imágenes generadas con éxito: {successfully_generated}")
        if errors > 0:
            self.stdout.write(
                self.style.ERROR(f" -> Fallos durante el proceso: {errors}")
            )
        self.stdout.write(self.style.NOTICE(("-" * 50)))
