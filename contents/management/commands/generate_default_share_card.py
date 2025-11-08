# /contents/management/commands/generate_default_share_card.py
# ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from contents.utils import generate_share_image_bytes


class Command(BaseCommand):
    """
    Comando de gestión para generar la imagen de compartición por defecto
    y guardarla como un archivo estático en la carpeta 'static/' del proyecto.
    """

    help = "Genera la imagen de compartición por defecto (og_branded_default.png)."

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.NOTICE(
                "Iniciando la generación de la imagen de compartición por defecto..."
            )
        )

        # 1. Generar los bytes de la imagen
        try:
            image_bytes = generate_share_image_bytes()
            if not image_bytes:
                self.stderr.write(
                    self.style.ERROR(
                        "La función 'generate_share_image_bytes' no devolvió datos. Abortando."
                    )
                )
                return
            self.stdout.write(
                self.style.SUCCESS(" -> Bytes de la imagen generados correctamente.")
            )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(
                    f"Se produjo un error al generar los bytes de la imagen: {e}"
                )
            )
            return

        # 2. Definir la ruta de destino en la carpeta 'static' raíz del proyecto.
        destination_dir = os.path.join(settings.BASE_DIR, "static", "images")
        destination_path = os.path.join(destination_dir, "og_branded_default.png")

        # Asegurarse de que el directorio de destino existe
        os.makedirs(destination_dir, exist_ok=True)
        self.stdout.write(f" -> Ruta de destino: {destination_path}")

        # 3. Escribir los bytes en el archivo
        try:
            with open(destination_path, "wb") as f:
                f.write(image_bytes)
            self.stdout.write(
                self.style.SUCCESS("\n¡Éxito! La imagen ha sido guardada.")
            )
            self.stdout.write(
                self.style.NOTICE(
                    "El siguiente paso es ejecutar 'collectstatic' para publicarla."
                )
            )
        except IOError as e:
            self.stderr.write(
                self.style.ERROR(
                    f"\nSe produjo un error de E/S al guardar el archivo: {e}"
                )
            )
