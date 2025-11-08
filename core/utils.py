import logging
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from messaging.push_utils import send_notification_to_user

logger = logging.getLogger(__name__)


def send_unified_notification(user, subject_template, body_template_prefix, context):
    """
    Orchestrates sending notifications via both Email and Push.

    Args:
        user (User): The recipient user object.
        subject_template (str): Path to the text template for the email subject.
        body_template_prefix (str): Prefix of the path to the body templates
                                    ('.html' and '.txt' will be appended).
        context (dict): Context dictionary for rendering the templates.
    """
    try:
        # --- 1. Prepare Common Context and Content ---
        site_url = "https://www.campustudionline.com"
        context["user"] = user
        context["site_url"] = site_url

        # Build absolute URLs for the templates
        if "assessment_pk" in context:
            if "results" in body_template_prefix:
                action_path = reverse(
                    "assessment:view_results", kwargs={"pk": context["assessment_pk"]}
                )
            else:
                action_path = reverse(
                    "assessment:take_assessment",
                    kwargs={"pk": context["assessment_pk"]},
                )
            context["action_url"] = f"{site_url}{action_path}"

        # --- 2. Send Email ---
        logger.info(
            f"Enviando email a {user.email} con plantilla base {body_template_prefix}"
        )

        subject = render_to_string(subject_template, context).strip()
        text_content = render_to_string(f"{body_template_prefix}.txt", context)
        html_content = render_to_string(f"{body_template_prefix}.html", context)

        send_mail(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_content,
        )
        logger.info(
            f"Email para {body_template_prefix} enviado correctamente a {user.email}."
        )

        # --- 3. Send Push Notification ---
        logger.info(
            f"Enviando notificación push a {user.username} para {body_template_prefix}"
        )
        push_title = subject  # Reuse email subject as title
        push_body = context.get(
            "push_body", "Tienes una nueva notificación en CampuStudiOnline."
        )
        push_url = context.get("action_url", site_url)

        send_notification_to_user(
            user=user, title=push_title, body=push_body, url=push_url
        )
        logger.info(
            f"Notificación Push para {body_template_prefix} enviada correctamente a {user.username}."
        )

    except Exception as e:
        logger.error(
            f"Error en send_unified_notification para el usuario {user.id} "
            f"y plantilla {body_template_prefix}: {e}",
            exc_info=True,
        )
