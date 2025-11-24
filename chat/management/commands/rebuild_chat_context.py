from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from chat.models import ChatRoom, RoomMembership
from academic_chat.models import AcademicChatLink
from contents.models import ContentCopy

User = get_user_model()

class Command(BaseCommand):
    help = 'Reconstruye las salas de chat globales y contextuales basadas en datos existentes.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Iniciando reconstrucción del ecosistema de chat...'))

        # FASE 1: SALAS GLOBALES
        self.stdout.write('Fase 1: Procesando Salas Globales...')
        self.process_global_rooms()

        # FASE 2: MIGRACIÓN LEGACY (AcademicChatLink)
        self.stdout.write('Fase 2: Migrando enlaces de chat académicos antiguos...')
        self.migrate_legacy_links()

        # FASE 3: CONTEXTUALIZACIÓN RETROACTIVA (ContentCopy)
        self.stdout.write('Fase 3: Procesando copias de estudio para membresías retroactivas...')
        self.process_content_copies()

        self.stdout.write(self.style.SUCCESS('Reconstrucción completada con éxito.'))

    def process_global_rooms(self):
        global_rooms = ["CampuStudiOnline", "Ayuda de eLCampus"]
        users = User.objects.filter(is_active=True)
        count = 0

        for room_name in global_rooms:
            room, created = ChatRoom.objects.get_or_create(
                name=room_name,
                defaults={
                    'is_private': False,
                    'description': f"Sala global: {room_name}",
                    'is_platform_default': True
                }
            )
            if created:
                self.stdout.write(f" - Creada sala global: {room_name}")
            
            # Bulk create membresías sería más eficiente, pero iteramos para seguridad por ahora
            memberships_to_create = []
            existing_members = set(RoomMembership.objects.filter(room=room).values_list('user_id', flat=True))
            
            for user in users:
                if user.id not in existing_members:
                    memberships_to_create.append(
                        RoomMembership(
                            user=user,
                            room=room,
                            status=RoomMembership.STATUS_MEMBER
                        )
                    )
            
            if memberships_to_create:
                RoomMembership.objects.bulk_create(memberships_to_create)
                count += len(memberships_to_create)
        
        self.stdout.write(f" - Añadidos {count} usuarios a salas globales.")

    def migrate_legacy_links(self):
        links = AcademicChatLink.objects.select_related('chat_room', 'subject').all()
        updated_count = 0
        
        for link in links:
            room = link.chat_room
            if not room.target_subject:
                room.target_subject = link.subject
                # Actualizar descripción si es genérica
                if not room.description or room.description == "":
                    room.description = f"Sala de estudio para la asignatura: {link.subject.name}"
                room.save()
                updated_count += 1
        
        self.stdout.write(f" - Migradas {updated_count} salas desde AcademicChatLink.")

    def process_content_copies(self):
        copies = ContentCopy.objects.select_related(
            'subject_context', 
            'original_content__sub_category__master_category',
            'user'
        ).all()
        
        processed = 0
        
        # Agrupar operaciones por usuario/sala para evitar duplicados en el proceso
        # Pero dado el volumen desconocido, procesamos una a una con get_or_create_context_room
        
        for copy in copies:
            try:
                room = self._resolve_room_for_copy(copy)
                if room:
                    _, created = RoomMembership.objects.get_or_create(
                        user=copy.user,
                        room=room,
                        defaults={'status': RoomMembership.STATUS_MEMBER}
                    )
                    if created:
                        processed += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error procesando copia {copy.id}: {e}"))

        self.stdout.write(f" - Creadas {processed} nuevas membresías contextuales.")

    def _resolve_room_for_copy(self, copy):
        # Lógica replicada de signals.py para atomicidad del comando
        target_subject = copy.subject_context
        original = copy.original_content
        target_sub_category = original.sub_category
        target_master_category = original.master_category
        
        if target_subject:
            return self._get_or_create_context_room(target_subject=target_subject)
        elif target_sub_category:
            return self._get_or_create_context_room(target_sub_category=target_sub_category)
        elif target_master_category:
            return self._get_or_create_context_room(target_master_category=target_master_category)
        return None

    def _get_or_create_context_room(self, target_subject=None, target_sub_category=None, target_master_category=None):
        # 1. Buscar existente
        if target_subject:
            room = ChatRoom.objects.filter(target_subject=target_subject).first()
            name_base = str(target_subject)
        elif target_sub_category:
            room = ChatRoom.objects.filter(target_sub_category=target_sub_category).first()
            name_base = f"{target_sub_category.master_category.name} - {target_sub_category.name}"
        elif target_master_category:
            room = ChatRoom.objects.filter(target_master_category=target_master_category).first()
            name_base = target_master_category.name
        else:
            return None

        if room:
            return room

        # 2. Crear nueva
        defaults = {
            'is_private': True,
            'is_platform_default': False,
        }
        
        if target_subject:
            defaults['target_subject'] = target_subject
            defaults['description'] = f"Sala de estudio para la asignatura: {target_subject.name}"
        elif target_sub_category:
            defaults['target_sub_category'] = target_sub_category
            defaults['description'] = f"Sala de interés para: {target_sub_category.name}"
        elif target_master_category:
            defaults['target_master_category'] = target_master_category
            defaults['description'] = f"Sala de interés para: {target_master_category.name}"

        try:
            room = ChatRoom.objects.create(name=name_base, **defaults)
        except IntegrityError:
            # Fallback por colisión de nombre
            suffix = ""
            if target_subject: suffix = f" ({target_subject.slug})"
            elif target_sub_category: suffix = f" ({target_sub_category.slug})"
            elif target_master_category: suffix = f" ({target_master_category.slug})"
            
            final_name = f"{name_base}{suffix}"[:255]
            room = ChatRoom.objects.create(name=final_name, **defaults)
            
        return room
