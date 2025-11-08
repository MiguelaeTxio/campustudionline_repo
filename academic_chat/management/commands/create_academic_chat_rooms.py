# /home/MiguelAeTxio/CampuStudiOnline/academic_chat/management/commands/create_academic_chat_rooms.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import Group
from academic_structure.models import Subject
from chat.models import ChatRoom
from academic_chat.models import AcademicChatLink


def generate_safe_chat_room_name(subject):
    """
    Genera un nombre de sala seguro en el formato:
    {Titulación} - {Asignatura} - {Año}
    y lo trunca de forma segura si excede los 255 caracteres.
    """
    base_name = f"{subject.academic_year.degree.name} - {subject.name} - {subject.year}"
    if len(base_name) > 255:
        base_name = f"{base_name[:252]}..."
    return base_name


class Command(BaseCommand):
    """
    Comando que crea una única sala de chat y su grupo de permisos asociado por asignatura,
    utilizando una lógica de 3 pasos para garantizar la unicidad absoluta de los nombres.
    """

    help = "Crea salas de chat y grupos de permisos con una lógica de 3 pasadas para garantizar unicidad."

    def add_arguments(self, parser):
        parser.add_argument(
            "--purge",
            action="store_true",
            help="Elimina TODAS las salas de chat académicas, vínculos y grupos de permisos asociados. ¡USAR CON PRECAUCIÓN!",
        )

    def handle(self, *args, **options):
        if options["purge"]:
            self.stdout.write(
                self.style.WARNING(
                    "Opción --purge detectada. Purgando datos existentes..."
                )
            )
            links_deleted, _ = AcademicChatLink.objects.all().delete()
            rooms_deleted, _ = ChatRoom.objects.filter(
                description__startswith="Sala de chat académica"
            ).delete()
            groups_deleted, _ = Group.objects.filter(
                name__startswith="ac_chat_subject_"
            ).delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f"-> Se han eliminado {links_deleted} vínculos, {rooms_deleted} salas y {groups_deleted} grupos de permisos."
                )
            )

        self.stdout.write(
            self.style.NOTICE(
                "--- Iniciando creación de salas y grupos (Lógica de 3 Pasadas) ---"
            )
        )

        self.stdout.write(
            self.style.NOTICE("Paso 1/3: Construyendo mapa de asignaturas únicas...")
        )
        subjects_to_process = {}
        all_subjects = Subject.objects.select_related("academic_year__degree").order_by(
            "academic_year__degree__name", "semester"
        )
        for subject in all_subjects:
            conceptual_key = (subject.academic_year.degree_id, subject.name, subject.year)
            if conceptual_key not in subjects_to_process:
                subjects_to_process[conceptual_key] = subject
        self.stdout.write(
            self.style.SUCCESS(
                f"Paso 1 completado. {len(subjects_to_process)} asignaturas únicas a procesar."
            )
        )

        self.stdout.write(
            self.style.NOTICE(
                "\nPaso 2/3: Generando nombres de sala y resolviendo colisiones..."
            )
        )
        final_creation_map = {}
        used_names = set()
        for subject_representative in subjects_to_process.values():
            base_name = generate_safe_chat_room_name(subject_representative)
            final_name = base_name
            counter = 1
            while final_name in used_names:
                suffix = f"_{counter}"
                truncated_base = base_name[: (255 - len(suffix))]
                final_name = f"{truncated_base}{suffix}"
                counter += 1
            used_names.add(final_name)
            final_creation_map[subject_representative] = final_name
        self.stdout.write(
            self.style.SUCCESS(
                f"Paso 2 completado. {len(final_creation_map)} nombres de sala únicos listos."
            )
        )

        self.stdout.write(
            self.style.NOTICE(
                "\nPaso 3/3: Creando grupos, salas y vínculos en la base de datos..."
            )
        )
        links_created_count = 0
        groups_created_count = 0

        with transaction.atomic():
            for subject, room_name in final_creation_map.items():
                try:
                    group_name = f"ac_chat_subject_{subject.id.hex}"
                    new_group, created = Group.objects.get_or_create(name=group_name)
                    if created:
                        groups_created_count += 1

                    new_chat_room = ChatRoom.objects.create(
                        name=room_name,
                        description=f"Sala de chat académica para la asignatura '{subject.name}' de la titulación '{subject.academic_year.degree.name}'.",
                        is_private=True,
                    )

                    AcademicChatLink.objects.create(
                        subject=subject, chat_room=new_chat_room, group=new_group
                    )
                    links_created_count += 1
                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(
                            f"Error fatal al procesar la asignatura '{subject.name}': {e}"
                        )
                    )

        self.stdout.write(self.style.SUCCESS(f"\nProceso de creación finalizado."))
        self.stdout.write(self.style.SUCCESS("\n--- Resumen Final ---"))
        self.stdout.write(f"  - Grupos de Permisos Creados: {groups_created_count}")
        self.stdout.write(
            f"  - Salas de Chat y Vínculos Creados: {links_created_count}"
        )
