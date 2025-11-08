# /home/MiguelAeTxio/CampuStudiOnline/academic_chat/models.py
import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.utils.text import slugify


class AcademicChatLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    subject = models.OneToOneField(
        "academic_structure.Subject",
        on_delete=models.CASCADE,
        related_name="academic_chat_link",
        verbose_name="Asignatura Vinculada",
    )

    chat_room = models.OneToOneField(
        "chat.ChatRoom",
        on_delete=models.CASCADE,
        related_name="academic_chat_link",
        verbose_name="Sala de Chat Asociada",
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="academic_chat_links",
        verbose_name="Grupo de Permisos",
        help_text=_("Grupo que otorga acceso a esta sala de chat."),
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Slug para URL",
        help_text=_(
            "Identificador único para la URL de la sala de chat, generado automáticamente."
        ),
    )

    enrolled_students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="enrolled_in_academic_chats",
        blank=True,
        verbose_name="Alumnos Matriculados (Verificados)",
        help_text=_(
            "Usuarios verificados como alumnos para esta asignatura. Gestionado por administradores."
        ),
    )

    access_code = models.CharField(
        max_length=12,
        unique=True,
        blank=True,
        verbose_name="Código de Acceso de Invitado",
        help_text=_(
            "Código único para que usuarios no matriculados (invitados) puedan unirse a la sala."
        ),
    )

    class Meta:
        verbose_name = "Vínculo de Chat Académico"
        verbose_name_plural = "Vínculos de Chat Académico"
        ordering = ["subject__name"]

    def __str__(self):
        return f"Chat link for: {self.subject.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            subject = self.subject
            base_slug_str = f"{subject.academic_year.degree.branch.university.code}-{subject.academic_year.degree.name}-{subject.name}-year-{subject.year}"
            base_slug = slugify(base_slug_str)

            max_len = self._meta.get_field("slug").max_length
            base_slug = base_slug[:max_len]

            proposed_slug = base_slug
            counter = 1
            while (
                type(self)
                .objects.filter(slug=proposed_slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                suffix = f"-{counter}"
                truncated_slug = base_slug[: (max_len - len(suffix))]
                proposed_slug = f"{truncated_slug}{suffix}"
                counter += 1
            self.slug = proposed_slug

        if not self.access_code:
            while True:
                code = uuid.uuid4().hex[:10].upper()
                if not type(self).objects.filter(access_code=code).exists():
                    self.access_code = code
                    break

        super().save(*args, **kwargs)


class AcademicChatMessage(models.Model):
    chat_link = models.ForeignKey(
        AcademicChatLink,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Vínculo de Chat Académico",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_academic_chat_messages",
        verbose_name="Remitente",
    )
    sender_username_display = models.CharField(
        max_length=150,
        verbose_name="Nombre de usuario del remitente (para visualización)",
    )
    content = models.TextField(verbose_name="Contenido del mensaje")
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Marca de tiempo"
    )
    is_deleted_by_moderator = models.BooleanField(
        default=False,
        verbose_name="¿Borrado por moderador?",
        help_text=_("Marcado si el mensaje fue borrado por un moderador."),
    )

    class Meta:
        verbose_name = "Mensaje de Chat Académico"
        verbose_name_plural = "Mensajes de Chat Académico"
        ordering = ["timestamp"]

    def __str__(self):
        sender_name = (
            self.sender_username_display
            if self.sender_username_display
            else (_("Anonymous") if not self.sender else self.sender.username)
        )
        deleted_prefix = _("[DELETED] ") if self.is_deleted_by_moderator else ""
        return f"{deleted_prefix}[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {sender_name}: {self.content[:50]}"


class PendingEnrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        db_index=True, verbose_name="Email del usuario a matricular"
    )
    academic_chat_link = models.ForeignKey(
        AcademicChatLink,
        on_delete=models.CASCADE,
        related_name="pending_enrollments",
        verbose_name="Vínculo de Chat Académico",
    )
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="added_pending_enrollments",
        verbose_name="Añadido por",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )

    class Meta:
        verbose_name = "Matrícula Pendiente"
        verbose_name_plural = "Matrículas Pendientes"
        ordering = ["-created_at", "email"]
        unique_together = ("email", "academic_chat_link")

    def __str__(self):
        return f"Pending enrollment for '{self.email}' in '{self.academic_chat_link.subject.name}'"
