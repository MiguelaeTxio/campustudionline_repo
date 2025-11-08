# /home/MiguelAeTxio/CampuStudiOnline/messaging/models.py
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class SharedContent(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")
    title_snapshot = models.CharField(max_length=255)
    description_snapshot = models.TextField(blank=True)
    url_snapshot = models.URLField(max_length=2048)
    shared_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shared_contents"
    )
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contenido Compartido en Chat"
        verbose_name_plural = "Contenidos Compartidos en Chat"
        ordering = ["-shared_at"]

    def __str__(self):
        return _("'%(title)s' shared by %(username)s") % {
            "title": self.title_snapshot,
            "username": self.shared_by.username,
        }


class DirectChatSession(models.Model):
    user1 = models.ForeignKey(
        User, related_name="chat_sessions_as_user1", on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        User, related_name="chat_sessions_as_user2", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_hidden_by_user1 = models.BooleanField(default=False)
    is_hidden_by_user2 = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user1", "user2")
        ordering = ["-updated_at"]
        verbose_name = "Sesión de Chat Directo"
        verbose_name_plural = "Sesiones de Chat Directo"

    def save(self, *args, **kwargs):
        if self.user1_id > self.user2_id:
            self.user1, self.user2 = self.user2, self.user1
        super().save(*args, **kwargs)

    def get_other_user(self, current_user):
        if self.user1 == current_user:
            return self.user2
        elif self.user2 == current_user:
            return self.user1
        return None

    def unread_message_count_for_user(self, user):
        if user in (self.user1, self.user2):
            return self.messages.filter(sender__ne=user, is_read=False).count()
        return 0


class DirectMessage(models.Model):
    session = models.ForeignKey(
        DirectChatSession, related_name="messages", on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        User, related_name="sent_direct_messages", on_delete=models.CASCADE
    )
    content = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    reply_to = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="replies"
    )
    shared_content = models.ForeignKey(
        SharedContent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="associated_messages",
    )

    class Meta:
        ordering = ["timestamp"]
        verbose_name = "Mensaje Directo"
        verbose_name_plural = "Mensajes Directos"

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=["is_read", "read_at"])


class Browser(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="UUID del Navegador",
    )
    user_agent = models.CharField(
        max_length=255,
        verbose_name="Agente de Usuario",
        help_text=_("Browser's User-Agent string for identification."),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Navegador Registrado"
        verbose_name_plural = "Navegadores Registrados"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Browser {self.uuid}"


class PushEndpoint(models.Model):
    browser = models.OneToOneField(
        Browser,
        on_delete=models.CASCADE,
        related_name="push_endpoint",
        verbose_name="Navegador",
    )
    endpoint = models.URLField(
        max_length=512, unique=True, verbose_name="URL del Endpoint"
    )
    keys = models.JSONField(verbose_name="Claves de Cifrado")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Endpoint de Notificación Push"
        verbose_name_plural = "Endpoints de Notificación Push"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Endpoint for {self.browser_id}"


class UserSubscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="push_subscriptions",
        verbose_name="Usuario",
    )
    browser = models.ForeignKey(
        Browser,
        on_delete=models.CASCADE,
        related_name="user_subscriptions",
        verbose_name="Navegador",
    )
    device_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Alias del Dispositivo",
        help_text=_(
            "Automatically generated descriptive name (e.g., 'Chrome on Windows')."
        ),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Suscripción Activa",
        help_text=_(
            "Allows the user to disable notifications on this device without losing the subscription."
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "browser")
        verbose_name = "Suscripción de Usuario"
        verbose_name_plural = "Suscripciones de Usuario"
        ordering = ["user", "-created_at"]

    def __str__(self):
        return _("Subscription of %(username)s on %(device)s") % {
            "username": self.user.username,
            "device": self.device_name or self.browser_id,
        }
