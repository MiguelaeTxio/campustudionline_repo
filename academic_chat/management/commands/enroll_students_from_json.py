# /home/MiguelAeTxio/CampuStudiOnline/academic_chat/management/commands/enroll_students_from_json.py
import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import transaction

from academic_chat.models import AcademicChatLink, PendingEnrollment


class Command(BaseCommand):
    help = "Matricula estudiantes en una sala de chat académica desde un archivo JSON."

    def add_arguments(self, parser):
        parser.add_argument(
            "chat_slug", type=str, help="El slug de la sala de chat académica."
        )
        parser.add_argument(
            "json_filename",
            type=str,
            help="El nombre del archivo JSON ubicado en /home/MiguelAeTxio/CampuStudiOnline/data/",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        chat_slug = options["chat_slug"]
        json_filename = options["json_filename"]
        base_path = "/home/MiguelAeTxio/CampuStudiOnline/data"
        json_file_path = os.path.join(base_path, json_filename)

        self.stdout.write(
            self.style.NOTICE(
                f"Iniciando proceso de matrícula para la sala '{chat_slug}'..."
            )
        )

        try:
            chat_link = AcademicChatLink.objects.get(slug=chat_slug)
            self.stdout.write(f"Sala de chat encontrada: '{chat_link.subject.name}'")
        except AcademicChatLink.DoesNotExist:
            raise CommandError(
                f"Error: La sala de chat con slug '{chat_slug}' no existe."
            )

        if not os.path.exists(json_file_path):
            raise CommandError(
                f"Error: El archivo JSON no se encuentra en la ruta '{json_file_path}'."
            )

        try:
            with open(json_file_path, "r", encoding="utf-8") as f:
                student_data = json.load(f)
        except json.JSONDecodeError:
            raise CommandError(
                f"Error: Formato de JSON inválido en el archivo '{json_file_path}'."
            )
        except Exception as e:
            raise CommandError(f"Error al leer el archivo: {e}")

        if not isinstance(student_data, list):
            raise CommandError(
                "Error: El contenido del archivo JSON debe ser una lista de objetos."
            )

        User = get_user_model()
        enrolled_count = 0
        pending_count = 0
        skipped_count = 0

        self.stdout.write(f"Procesando {len(student_data)} registros del archivo...")

        for item in student_data:
            email = item.get("email")
            if not email:
                self.stdout.write(
                    self.style.WARNING(f"  - Saltando registro sin email: {item}")
                )
                skipped_count += 1
                continue

            email = email.strip().lower()
            try:
                validate_email(email)
            except ValidationError:
                self.stdout.write(
                    self.style.WARNING(
                        f"  - Saltando email con formato inválido: {email}"
                    )
                )
                skipped_count += 1
                continue

            user = User.objects.filter(email__iexact=email).first()
            if user:
                if user not in chat_link.enrolled_students.all():
                    chat_link.enrolled_students.add(user)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  - Matriculado (Ipso Facto): '{user.username}' ({email})"
                        )
                    )
                    enrolled_count += 1
                else:
                    self.stdout.write(
                        f"  - Ya matriculado: '{user.username}' ({email})"
                    )
                    skipped_count += 1
            else:
                _, created = PendingEnrollment.objects.get_or_create(
                    email=email,
                    academic_chat_link=chat_link,
                    defaults={"added_by": None},
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  - Matrícula pendiente creada para: {email}"
                        )
                    )
                    pending_count += 1
                else:
                    self.stdout.write(
                        f"  - Matrícula pendiente ya existía para: {email}"
                    )
                    skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS("\n--- Proceso de Matrícula Finalizado ---")
        )
        self.stdout.write(f"Total de registros procesados: {len(student_data)}")
        self.stdout.write(f"Usuarios matriculados inmediatamente: {enrolled_count}")
        self.stdout.write(f"Nuevas matrículas pendientes creadas: {pending_count}")
        self.stdout.write(
            f"Registros omitidos (inválidos, ya matriculados o pendientes): {skipped_count}"
        )
