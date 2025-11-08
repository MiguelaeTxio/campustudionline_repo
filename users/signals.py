# /users/signals.py

import logging
from django.conf import settings

# Eliminamos la importación del User de Django, ya no lo usamos.
# from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string

# Importamos UserProfile desde nuestros modelos locales
from .models import UserProfile

logger = logging.getLogger(__name__)


# --- Señal para el correo de bienvenida ---
# Corregido para apuntar a settings.AUTH_USER_MODEL
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        user = instance
        logger.info(
            f"Nuevo user creado: {user.username} (ID: {user.pk}). Preparando correo de bienvenida."
        )

        try:
            # Usamos getattr para acceder de forma segura a settings
            site_url = getattr(settings, "SITE_URL", "https://tu-sitio.com")
            if not getattr(settings, "SITE_URL", None):
                logger.warning(
                    "SITE_URL no está definida en settings.py. Usando un placeholder."
                )

            context = {
                "user": user,
                "site_url": site_url,
            }

            subject = "¡Bienvenido/a a CampuStudiOnline!"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]

            text_content = render_to_string("emails/welcome_email.txt", context)
            html_content = render_to_string("emails/welcome_email.html", context)

            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")

            logger.debug(f"Intentando enviar correo de bienvenida a {user.email}...")
            msg.send()

            logger.info(
                f"Correo de bienvenida para {user.username} ({user.email}) procesado para envío."
            )

        except Exception as e:
            logger.error(
                f"ERROR al procesar o enviar correo de bienvenida a {user.username} ({user.email}): {e}",
                exc_info=True,
            )


# --- Señal para crear/actualizar el perfil de user (movida desde models.py) ---
# También apunta a settings.AUTH_USER_MODEL, como debe ser.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Crea un UserProfile cuando se crea un nuevo CustomUser,
    o guarda el perfil existente cuando el CustomUser se guarda.
    """
    if created:
        UserProfile.objects.create(user=instance)
        logger.info(
            f"Perfil de user creado para el nuevo user {instance.username}."
        )
    else:
        # Usamos hasattr para evitar un error si el perfil no existe por alguna razón
        if hasattr(instance, "userprofile"):
            instance.userprofile.save()
        else:
            # Caso de seguridad: si un user existe pero su perfil fue eliminado
            UserProfile.objects.create(user=instance)
            logger.warning(
                f"Se ha creado un perfil para el user existente {instance.username} porque no tenía uno."
            )
