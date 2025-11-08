# /home/MiguelAeTxio/CampuStudiOnline/contents/management/commands/update_content_format.py
import frontmatter
from django.core.management.base import BaseCommand
from django.db import transaction
from contents.models import ContentMaterial


class Command(BaseCommand):
    """
    Comando de gestión para actualizar el formato de los ContentMaterial existentes,
    añadiendo un bloque de metadatos YAML al inicio del campo markdown_content.
    """

    help = "Actualiza el contenido Markdown existente para incluir metadatos YAML."

    def add_arguments(self, parser):
        """
        Añade argumentos al comando.
        """
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simula la ejecución sin guardar ningún cambio en la base de datos.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Lógica principal del comando.
        """
        is_dry_run = options["dry_run"]

        self.stdout.write(self.style.NOTICE("---[CSO-UPDATE-SCRIPT-START]---"))

        if is_dry_run:
            self.stdout.write(
                self.style.WARNING(
                    ">>> MODO SIMULACIÓN (DRY-RUN) ACTIVADO. No se guardarán cambios."
                )
            )

        all_content_materials = ContentMaterial.objects.select_related(
            "subject__academic_year__degree__branch__university",
            "topic__main_category__discipline__knowledge_area",
        ).all()

        updated_count = 0
        skipped_count = 0

        for material in all_content_materials:
            if (
                material.markdown_content
                and material.markdown_content.strip().startswith("---")
            ):
                self.stdout.write(f"Saltando ID {material.pk}: ya tiene formato YAML.")
                skipped_count += 1
                continue

            subject = material.subject
            topic = material.topic

            metadata = {
                "titulo_curso": material.title,
                "descripcion_corta": material.short_description or "",
                "tipo_contenido": "academic_structure",
            }

            if subject:
                degree = subject.academic_year.degree
                branch = degree.branch
                university = branch.university
                metadata["contexto_academico"] = {
                    "universidad": university.name,
                    "rama": branch.name,
                    "titulacion": f"{degree.name} ({degree.get_degree_type_display()})",
                    "curso_semestre": f"Año {subject.year}, Semestre {subject.semester}",
                    "tipo_asignatura": subject.get_subject_type_display(),
                    "subject_slug": subject.slug,
                }

            if topic:
                main_category = topic.main_category
                discipline = main_category.discipline
                area = discipline.knowledge_area
                metadata["clasificacion_intelectual"] = {
                    "area": area.name,
                    "disciplina": discipline.name,
                    "categoria": main_category.name,
                    "topico_especifico": topic.name,
                }

            new_post = frontmatter.Post(material.markdown_content or "", **metadata)
            new_content_markdown = frontmatter.dumps(new_post)

            if not is_dry_run:
                material.markdown_content = new_content_markdown
                material.save(update_fields=["markdown_content"])

            self.stdout.write(
                self.style.SUCCESS(f"Procesado ID {material.pk}: '{material.title}'")
            )
            updated_count += 1

        self.stdout.write(self.style.NOTICE("\n--- Resumen de la Operación ---"))
        self.stdout.write(f"Contenidos actualizados: {updated_count}")
        self.stdout.write(f"Contenidos omitidos (ya tenían formato): {skipped_count}")
        if is_dry_run:
            self.stdout.write(
                self.style.WARNING(
                    ">>> Recordatorio: Los cambios anteriores solo fueron una simulación."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    ">>> ¡Operación completada! Los cambios se han guardado en la base de datos."
                )
            )

        self.stdout.write(self.style.NOTICE("---[CSO-UPDATE-SCRIPT-END]---"))
