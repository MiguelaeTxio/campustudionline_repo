# /home/MiguelAeTxio/CampuStudiOnline/content_automation/management/commands/test_schema_generation.py
import json
from django.core.management.base import BaseCommand, CommandError

from academic_structure.models import Subject
from core.services.prompt_generators import generate_master_schema_prompt
from core.services.gemini_service import generate_text_content


class Command(BaseCommand):
    help = (
        "Genera un master_schema de prueba para una asignatura existente por su nombre, "
        "permitiendo controlar el parámetro max_output_tokens."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "subject_name",
            type=str,
            help="El NOMBRE de la asignatura para la cual generar el schema.",
        )
        parser.add_argument(
            "--max_tokens",
            type=int,
            default=None,
            help="Valor para max_output_tokens. Si no se especifica, se usa el default del servicio.",
        )
        parser.add_argument(
            "--output_file",
            type=str,
            default="master_schema_pruebas.txt",
            help="Ruta del archivo de salida para el schema generado.",
        )

    def handle(self, *args, **options):
        subject_name = options["subject_name"]
        max_tokens_override = options["max_tokens"]
        output_file = options["output_file"]
        
        try:
            subject = Subject.objects.filter(name__iexact=subject_name).first()
            if not subject:
                raise Subject.DoesNotExist
            self.stdout.write(
                self.style.SUCCESS(f"Asignatura encontrada: '{subject.name}' (ID: {subject.pk})")
            )
        except Subject.DoesNotExist:
            raise CommandError(f"La asignatura con el nombre '{subject_name}' no existe.")

        topic_description = subject.name
        degree = subject.academic_year.degree
        academic_context = (
            f"- Universidad: {degree.branch.university.name}\n"
            f"- Rama: {degree.branch.name}\n"
            f"- Titulación: {degree.name} ({degree.get_degree_type_display()})"
        )

        prompt = generate_master_schema_prompt(topic_description, academic_context)

        self.stdout.write("Generando master_schema con la API de Gemini...")
        
        if max_tokens_override is not None:
            self.stdout.write(self.style.WARNING(f"Usando max_output_tokens override: {max_tokens_override}"))

        success, schema_or_error, finish_reason = generate_text_content(
            prompt, max_tokens_override=max_tokens_override
        )

        if success:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Master_schema generado con éxito. Razón de finalización: {finish_reason}"
                )
            )
            if finish_reason == 'MAX_TOKENS':
                self.stdout.write(self.style.ERROR("ADVERTENCIA: La salida fue truncada por MAX_TOKENS."))

            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(schema_or_error)
                self.stdout.write(
                    self.style.SUCCESS(f"Resultado guardado en '{output_file}'")
                )
            except IOError as e:
                self.stderr.write(
                    self.style.ERROR(f"No se pudo escribir en el archivo de salida: {e}")
                )
        else:
            self.stderr.write(
                self.style.ERROR(f"Fallo al generar el master_schema: {schema_or_error}")
            )
