# /users/management/commands/find_redundant_containers.py
# ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'.
# ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'.

import os
import re
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    """
    Este comando audita las plantillas del proyecto para encontrar aquellas
    que heredan de 'base.html' y contienen un <div class="container">
    redundante inmediatamente después del bloque de contenido.
    """

    help = "Audits templates to find redundant containers for refactoring."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                "--- Iniciando auditoría de plantillas para contenedores redundantes ---"
            )
        )

        project_root = settings.BASE_DIR
        templates_to_fix = []

        # Patrón para encontrar un <div class="container..."> después de {% block contenido %}
        # con espacios y saltos de línea intermedios.
        pattern = re.compile(
            r'{%\s*block\s+contenido\s*%}(.*?)<div\s+class="container',
            re.DOTALL | re.IGNORECASE,
        )

        for root, _, files in os.walk(project_root):
            for filename in files:
                if filename.endswith(".html"):
                    file_path = Path(root) / filename

                    # Ignoramos directorios que no nos interesan
                    if any(
                        part in str(file_path)
                        for part in ["/static/", "/.git/", "/staticfiles_production/"]
                    ):
                        continue

                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()

                        # Primero, verificamos si la plantilla hereda de base.html
                        if '{% extends "base.html" %}' in content:
                            # Si hereda, buscamos el patrón del contenedor redundante
                            match = pattern.search(content)
                            if match:
                                # Verificamos que no haya lógica compleja entre el bloque y el div
                                content_between = match.group(1).strip()
                                if not content_between or content_between.startswith(
                                    "{#"
                                ):
                                    relative_path = file_path.relative_to(project_root)
                                    templates_to_fix.append(str(relative_path))

                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"No se pudo leer el archivo {file_path}: {e}"
                            )
                        )

        if templates_to_fix:
            self.stdout.write(
                self.style.WARNING(
                    "\nSe encontraron los siguientes archivos con contenedores redundantes:"
                )
            )
            for path in sorted(templates_to_fix):
                self.stdout.write(f" - {path}")
            self.stdout.write(
                self.style.NOTICE(
                    '\nPor favor, revise estos archivos y elimine el <div class="container"> '
                    "y su correspondiente </div> de cierre."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "\nAuditoría completada. No se encontraron archivos con contenedores redundantes evidentes."
                )
            )

        self.stdout.write(self.style.SUCCESS("--- Auditoría finalizada ---"))
