import logging
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages

from .forms import AdminEmailForm
from .models import MaintenanceSettings

logger = logging.getLogger(__name__)


@staff_member_required
def send_custom_email_view(request):
    # --- START OF FIX ---
    User = get_user_model()
    # --- END OF FIX ---

    logger.debug(f"Request method: {request.method} a send_custom_email_view")
    form = AdminEmailForm(request.POST or None)
    email_sent_count = 0

    if request.method == "POST":
        logger.debug(f"POST data recibido: {request.POST}")
        if form.is_valid():
            logger.debug("Formulario de envío de correo ES VÁLIDO.")
            logger.debug(f"Datos del formulario validados: {form.cleaned_data}")

            data = form.cleaned_data
            recipients_list = []

            if data["user_selection_type"] == "all":
                logger.debug(
                    "Opción seleccionada: Enviar a TODOS los usuarios activos."
                )
                recipients_list = User.objects.filter(
                    is_active=True, email__isnull=False
                ).exclude(email__exact="")
            elif data["user_selection_type"] == "selected":
                logger.debug("Opción seleccionada: Enviar a USUARIOS SELECCIONADOS.")
                if data["selected_users"]:
                    logger.debug(
                        f"IDs de usuarios seleccionados: {[user.id for user in data['selected_users']]}"
                    )
                    recipients_list = (
                        data["selected_users"]
                        .filter(email__isnull=False)
                        .exclude(email__exact="")
                    )
                else:
                    logger.debug(
                        "Ningún usuario específico fue seleccionado en el formulario."
                    )
                    recipients_list = User.objects.none()

            logger.debug(
                f"Número de destinatarios válidos encontrados: {recipients_list.count() if hasattr(recipients_list, 'count') else len(recipients_list)}"
            )
            has_recipients = (
                recipients_list.exists()
                if hasattr(recipients_list, "exists")
                else bool(recipients_list)
            )

            if not has_recipients:
                logger.warning(
                    "No se encontraron destinatarios válidos para enviar el correo."
                )
                messages.warning(
                    request,
                    "No se encontraron destinatarios válidos para enviar el correo.",
                )
            else:
                template_name_base = data["email_template"]
                html_template = f"emails/{template_name_base}.html"
                txt_template = f"emails/{template_name_base}.txt"

                asunto_correo = data["asunto"]
                if template_name_base == "admin_manual_welcome":
                    asunto_correo = "¡Bienvenido/a a CampuStudiOnline!"

                logger.info(
                    f"Preparando para enviar correos. Plantilla base: '{template_name_base}', Asunto: '{asunto_correo}'"
                )

                for user_recipient in recipients_list:
                    logger.debug(
                        f"Procesando destinatario: {user_recipient.username} ({user_recipient.email})"
                    )
                    context = {
                        "user": user_recipient,
                        "site_url": settings.SITE_URL,
                        "asunto_correo": asunto_correo,
                    }
                    if template_name_base == "admin_service_outage":
                        context.update(
                            {
                                "fecha_hora_mantenimiento": data[
                                    "fecha_hora_mantenimiento"
                                ],
                                "duracion_mantenimiento": data[
                                    "duracion_mantenimiento"
                                ],
                                "mensaje_adicional": data[
                                    "mensaje_adicional_mantenimiento"
                                ],
                            }
                        )
                    elif template_name_base == "admin_general_announcement":
                        context.update(
                            {
                                "cuerpo_mensaje": data["cuerpo_mensaje_general"],
                            }
                        )

                    try:
                        text_content = render_to_string(txt_template, context)
                        html_content = render_to_string(html_template, context)

                        connection_instance = get_connection(fail_silently=True)
                        logger.debug(
                            f"AdminView: EMAIL_BACKEND en uso (instancia): {type(connection_instance)}"
                        )
                        logger.debug(
                            f"AdminView: settings.EMAIL_BACKEND es: {settings.EMAIL_BACKEND}"
                        )

                        msg = EmailMultiAlternatives(
                            asunto_correo,
                            text_content,
                            settings.DEFAULT_FROM_EMAIL,
                            [user_recipient.email],
                        )
                        msg.attach_alternative(html_content, "text/html")

                        logger.debug(
                            f"Intentando enviar correo a {user_recipient.email}..."
                        )
                        msg.send()
                        email_sent_count += 1
                        logger.info(
                            f"Admin Mail: Correo '{template_name_base}' procesado para envío a {user_recipient.username} ({user_recipient.email})"
                        )

                    except Exception as e:
                        logger.error(
                            f"Admin Mail: Error CRÍTICO al preparar o enviar correo a {user_recipient.username}: {e}",
                            exc_info=True,
                        )
                        messages.error(
                            request,
                            f"Error al enviar correo a {user_recipient.username}: {e}",
                        )

                if email_sent_count > 0:
                    messages.success(
                        request,
                        f"Se han procesado {email_sent_count} correos para envío (revisa SendGrid y logs).",
                    )
                elif not any(
                    m.level == messages.WARNING
                    and "No se encontraron destinatarios" in str(m)
                    for m in messages.get_messages(request)
                ):
                    messages.info(
                        request, "No se procesaron correos para envío. Revisa los logs."
                    )
                return redirect(request.path)
        else:
            logger.warning("Formulario de envío de correo NO ES VÁLIDO.")
            logger.warning(f"Errores del formulario: {form.errors.as_json()}")

    context_render = {
        "form": form,
        "title": "Enviar Correo a Usuarios",
        "has_permission": request.user.is_staff,
        "opts": MaintenanceSettings._meta,
    }
    return render(
        request, "admin/global_settings/send_custom_email.html", context_render
    )
