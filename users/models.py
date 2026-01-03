import random
import string
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomUser(AbstractUser):
    """
    Este es el modelo de usuario principal del proyecto.
    """
    groups = models.ManyToManyField(
        Group,
        verbose_name="Grupos",
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="Permisos de usuario",
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="customuser_set",
        related_query_name="user",
    )
    affiliated_university = models.ForeignKey(
        "academic_structure.University",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="university_members",
        verbose_name="Institución afiliada (verificada)",
        help_text=_(
            "Afiliación institucional verificada por un administrador. No editable por el usuario en su perfil."
        ),
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Usuario",
    )
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Teléfono"
    )
    degree = models.CharField(max_length=150, blank=True, verbose_name="Carrera")
    current_year = models.CharField(
        max_length=50, blank=True, verbose_name="Curso Actual"
    )
    university = models.CharField(
        max_length=200, blank=True, verbose_name="Institución"
    )
    hobbies = models.TextField(
        blank=True, verbose_name="Gustos e Intereses"
    )
    work_experience = models.TextField(
        blank=True, verbose_name="Experiencia Laboral"
    )
    public_personal_description = models.TextField(
        blank=True,
        verbose_name="Descripción personal para el portafolio",
        help_text=_("Una breve introducción sobre ti para mostrar en tu portafolio."),
    )
    professional_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Título profesional o Headline",
        help_text=_(
            "Ej: Desarrollador Web Fullstack, Estudiante de Marketing Digital."
        ),
    )
    show_phone_in_portfolio = models.BooleanField(
        default=False, verbose_name="Mostrar teléfono en el portafolio público"
    )
    show_degree_in_portfolio = models.BooleanField(
        default=False, verbose_name="Mostrar carrera en el portafolio público"
    )
    show_current_year_in_portfolio = models.BooleanField(
        default=False, verbose_name="Mostrar curso actual en el portafolio público"
    )
    show_university_in_portfolio = models.BooleanField(
        default=False, verbose_name="Mostrar institución en el portafolio público"
    )
    show_hobbies_in_portfolio = models.BooleanField(
        default=False,
        verbose_name="Mostrar gustos e intereses en el portafolio público",
    )
    show_work_experience_in_portfolio = models.BooleanField(
        default=False,
        verbose_name="Mostrar experiencia laboral en el portafolio público",
    )
    show_chat_rooms_in_portfolio = models.BooleanField(
        default=False,
        verbose_name="Mostrar mi directorio de salas de chat en el portafolio público",
    )
    show_personal_description_in_portfolio = models.BooleanField(
        default=True, verbose_name="Mostrar descripción personal en el portafolio"
    )
    show_professional_title_in_portfolio = models.BooleanField(
        default=True, verbose_name="Mostrar título profesional en el portafolio"
    )
    show_short_messages_in_portfolio = models.BooleanField(
        default=True, verbose_name="Mostrar mensajes cortos en el portafolio público"
    )
    show_user_links_in_portfolio = models.BooleanField(
        default=True,
        verbose_name="Mostrar mis enlaces de interés en el portafolio público",
    )
    public_key = models.TextField(
        blank=True,
        null=True,
        verbose_name="Clave Pública para Cifrado",
        help_text=_(
            "Clave pública del usuario, en formato JWK, para el cifrado de mensajes."
        ),
    )
    encrypted_private_key = models.TextField(
        blank=True,
        null=True,
        verbose_name="Clave Privada Cifrada",
        help_text=_(
            "Clave privada del usuario, cifrada con su contraseña, para recuperación entre dispositivos."
        ),
    )
    encryption_salt = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Sal para Cifrado",
        help_text=_(
            "Sal criptográfica única para este usuario, usada para derivar la clave de cifrado. No cambiar manualmente."
        ),
    )
    blocked_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="blocked_by",
        blank=True,
        verbose_name="Usuarios Bloqueados",
        help_text=_("Otros usuarios que este perfil ha decidido bloquear."),
    )
    last_checked_chat_activity = models.DateTimeField(
        default=timezone.now,
        verbose_name="Última revisión de actividad en chat",
        help_text=_(
            "Registra la última vez que el usuario revisó la actividad de sus salas de chat en su portafolio."
        ),
    )
    favorite_content = models.ManyToManyField(
        "contents.ContentMaterial",
        related_name="favorited_by",
        blank=True,
        verbose_name="Contenido Favorito",
        help_text=_("Contenido que el usuario ha marcado como favorito."),
    )
    ia_requests_today = models.IntegerField(
        default=0,
        verbose_name="Peticiones de IA hoy",
        help_text=_(
            "Contador de peticiones a la API de IA realizadas hoy por el usuario."
        ),
    )
    last_ia_request_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de última petición de IA",
        help_text=_("Fecha de la última petición para reiniciar el contador diario."),
    )
    
    # --- CAMPOS DE SISTEMA DE REFERIDOS (Refactorizado) ---
    pending_referral_code = models.CharField(
        max_length=4, 
        null=True, 
        blank=True, 
        verbose_name="Código de referido pendiente",
        help_text=_("Código temporal almacenado durante el registro y antes de la activación.")
    )
    referred_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referrals',
        verbose_name="Referido por (Comercial)",
        help_text=_("El comercial dueño del código con el que este usuario se registró.")
    )
    has_claimed_copy_incentive = models.BooleanField(
        default=False,
        verbose_name="Incentivo de Copia Reclamado",
        help_text=_("True si ya se ha contabilizado la conversión por primera copia.")
    )
    has_claimed_assessment_incentive = models.BooleanField(
        default=False,
        verbose_name="Incentivo de Evaluación Reclamado",
        help_text=_("True si ya se ha contabilizado la conversión por primera evaluación.")
    )
    
    accepts_marketing = models.BooleanField(
        default=True,
        verbose_name="Acepta comunicaciones comerciales",
        help_text=_("Indica si el usuario desea recibir correos administrativos no críticos.")
    )

    profile_created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación del perfil"
    )
    profile_updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización del perfil"
    )

    def __str__(self):
        return _("Profile of %(username)s") % {"username": self.user.username}

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
        ordering = ["user__username"]


class ArchivedKey(models.Model):
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="archived_keys",
        verbose_name="Perfil de Usuario",
    )
    encrypted_private_key = models.TextField(
        verbose_name="Clave Privada Cifrada Archivada",
        help_text=_(
            "Una clave privada anterior, cifrada con la contraseña del usuario en ese momento."
        ),
    )
    archived_at = models.DateTimeField(
        default=timezone.now, verbose_name="Fecha de Archivado"
    )

    def __str__(self):
        return _("Clave archivada para %(username)s el %(date)s") % {
            "username": self.profile.user.username,
            "date": self.archived_at.strftime("%Y-%m-%d %H:%M"),
        }

    class Meta:
        verbose_name = "Clave Archivada"
        verbose_name_plural = "Claves Archivadas"
        ordering = ["-archived_at"]


class RecommendationCode(models.Model):
    """
    Código único de recomendación (activo fungible) gestionado por un comercial.
    """
    code = models.CharField(
        max_length=4,
        unique=True,
        db_index=True,
        verbose_name="Código de Conversión",
        help_text="Código alfanumérico de 4 caracteres (Ej: 4A7K)."
    )
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vendor_codes',
        limit_choices_to={'groups__name': 'Comerciales'},
        verbose_name="Comercial (Vendor)"
    )
    redeemed_by = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='redeemed_code',
        verbose_name="Canjeado por (Usuario)"
    )
    date_redeemed = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Canje"
    )

    def __str__(self):
        status = "USADO" if self.redeemed_by else "DISPONIBLE"
        return f"{self.code} ({status}) - {self.vendor.username}"

    class Meta:
        verbose_name = "Código de Recomendación"
        verbose_name_plural = "Códigos de Recomendación"

    @classmethod
    def generate_batch(cls, vendor, amount=10):
        if not vendor.groups.filter(name='Comerciales').exists():
            return 0

        chars = string.ascii_uppercase + string.digits
        created_count = 0
        
        for _ in range(amount):
            for _ in range(100):
                code = ''.join(random.choices(chars, k=4))
                if not cls.objects.filter(code=code).exists():
                    cls.objects.create(code=code, vendor=vendor)
                    created_count += 1
                    break
        return created_count
