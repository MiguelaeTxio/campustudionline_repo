# /home/MiguelAeTxio/CampuStudiOnline/chat/models.py
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class ChatRoom(models.Model):
    name = models.CharField(
        max_length=255, unique=True, verbose_name="Nombre de la Sala"
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        max_length=255,
        help_text=_("Automatically generated from the name or context if left empty."),
    )
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    
    # --- Context Links (Polymorphic-like associations) ---
    target_subject = models.OneToOneField(
        'academic_structure.Subject',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='chat_room',
        verbose_name="Asignatura Vinculada",
        help_text="Si esta sala pertenece a una asignatura académica."
    )
    target_master_category = models.OneToOneField(
        'contents.FreeContentMasterCategory',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='chat_room',
        verbose_name="Categoría Maestra Vinculada",
        help_text="Si esta sala pertenece a una categoría maestra de contenido libre."
    )
    target_sub_category = models.OneToOneField(
        'contents.FreeContentSubCategory',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='chat_room',
        verbose_name="Subcategoría Vinculada",
        help_text="Si esta sala pertenece a una subcategoría de contenido libre."
    )
    # -----------------------------------------------------

    is_private = models.BooleanField(default=True, verbose_name="¿Es Privada?")
    
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_chat_rooms",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Creador",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    
    is_platform_default = models.BooleanField(
        default=False, verbose_name="¿Es Sala por Defecto de la Plataforma?"
    )

    def save(self, *args, **kwargs):
        # Logic to auto-generate slug from context if available
        if not self.slug:
            base_slug = ""
            if self.target_subject:
                base_slug = self.target_subject.slug
            elif self.target_sub_category:
                base_slug = self.target_sub_category.slug
            elif self.target_master_category:
                base_slug = self.target_master_category.slug
            else:
                base_slug = slugify(self.name)
            
            # Ensure slug fits and is unique
            base_slug = base_slug[:(255 - 5)]
            self.slug = base_slug
            counter = 1
            while ChatRoom.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                slug_limit = 255 - len(str(counter)) - 1
                self.slug = f"{base_slug[:slug_limit]}-{counter}"
                counter += 1
                
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("chat:room_detail", kwargs={"room_slug": self.slug})

    def __str__(self):
        if self.target_subject:
            return f"Sala: {self.target_subject.name}"
        if self.target_sub_category:
            return f"Sala: {self.target_sub_category.name}"
        if self.target_master_category:
            return f"Sala: {self.target_master_category.name}"
        return self.name

    class Meta:
        verbose_name = "Sala de Chat"
        verbose_name_plural = "Salas de Chat"
        ordering = ["-is_platform_default", "name"]


class RoomMembership(models.Model):
    STATUS_PENDING = "pending_approval"
    STATUS_MEMBER = "member"
    STATUS_REJECTED = "rejected"
    STATUS_INVITED = "invited"

    STATUS_CHOICES = [
        (STATUS_PENDING, _("Pending Approval")),
        (STATUS_MEMBER, _("Member")),
        (STATUS_REJECTED, _("Rejected")),
        (STATUS_INVITED, _("Invited")),
    ]

    ROLE_MEMBER = "member"
    ROLE_MODERATOR = "moderator"

    ROLE_CHOICES = [
        (ROLE_MEMBER, _("Member")),
        (ROLE_MODERATOR, _("Moderator")),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_memberships",
        verbose_name="Usuario",
    )
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="memberships",
        verbose_name="Sala",
    )
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Unión")
    is_silenced = models.BooleanField(default=False, verbose_name="¿Está Silenciado?")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_MEMBER,
        verbose_name="Estado de Membresía",
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_MEMBER,
        verbose_name="Rol en la Sala",
    )

    class Meta:
        unique_together = ("user", "room")
        verbose_name = "Membresía de Sala"
        verbose_name_plural = "Membresías de Sala"
        ordering = ["room", "date_joined"]

    def __str__(self):
        return f"{self.user.username} in {self.room.name} ({self.get_status_display()}) - Role: {self.get_role_display()}"


class ChatMessage(models.Model):
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Sala",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_chat_messages",
        verbose_name="Remitente (Usuario)",
    )
    sender_username_display = models.CharField(
        max_length=150,
        verbose_name="Nombre de Usuario del Remitente (para mostrar)",
    )
    content = models.TextField(verbose_name="Contenido del Mensaje")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Marca de Tiempo")
    is_deleted_by_moderator = models.BooleanField(
        default=False,
        verbose_name="¿Borrado por Moderador?",
        help_text=_("Checked if the message was deleted by a moderator or creator."),
    )

    def __str__(self):
        sender_name = (
            self.sender_username_display
            if self.sender_username_display
            else (_("Anonymous") if not self.sender else self.sender.username)
        )
        deleted_prefix = _("[DELETED] ") if self.is_deleted_by_moderator else ""
        return f"{deleted_prefix}[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {sender_name}: {self.content[:50]}"

    class Meta:
        verbose_name = "Mensaje de Chat"
        verbose_name_plural = "Mensajes de Chat"
        ordering = ["timestamp"]
