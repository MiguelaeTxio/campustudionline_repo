import logging
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q

from .forms import AdminEmailForm
from .models import MaintenanceSettings


@staff_member_required
def send_custom_email_view(request):
    User = get_user_model()
    logger = logging.getLogger(__name__)

    logger.debug(f"Request method: {request.method} a send_custom_email_view")
    form = AdminEmailForm(request.POST or None)
    email_sent_count = 0
    error_count = 0

    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            template_name_base = data["email_template"]
            
            # 1. SELECCIÓN DE DESTINATARIOS
            if data["user_selection_type"] == "all":
                recipients_list = User.objects.filter(is_active=True).exclude(email__isnull=True).exclude(email__exact="")
            elif data["user_selection_type"] == "selected":
                if data["selected_users"]:
                    recipients_list = data["selected_users"].exclude(email__isnull=True).exclude(email__exact="")
                else:
                    recipients_list = User.objects.none()
            else:
                recipients_list = User.objects.none()

            # 2. FILTRADO POR PREFERENCIAS (RGPD/LSSI)
            # Solo filtramos si es un correo comercial (Anuncio General)
            # Avisos de servicio y bienvenidas son transaccionales/críticos.
            ignored_users_count = 0
            
            if template_name_base == "admin_general_announcement":
                # Filtramos usuarios que NO aceptan marketing
                # Nota: UserProfile puede no existir para algunos usuarios antiguos, asumimos True por defecto si no existe
                # O usamos la relación inversa.
                initial_count = recipients_list.count()
                recipients_list = recipients_list.filter(
                    Q(userprofile__accepts_marketing=True) | Q(userprofile__isnull=True)
                )
                ignored_users_count = initial_count - recipients_list.count()
                if ignored_users_count > 0:
                    messages.info(request, f"Se han omitido {ignored_users_count} usuarios que han solicitado no recibir comunicaciones comerciales.")

            has_recipients = recipients_list.exists()

            if not has_recipients:
                messages.warning(request, "No se encontraron destinatarios válidos (activos y con email) para enviar el correo.")
            else:
                # 3. PREPARACIÓN DE CONTEXTO
                html_template = f"emails/{template_name_base}.html"
                txt_template = f"emails/{template_name_base}.txt"

                asunto_correo = data["asunto"]
                if template_name_base == "admin_manual_welcome":
                    asunto_correo = "¡Bienvenido/a a CampuStudiOnline!"

                # 4. ENVÍO EN BUCLE
                connection = get_connection() # Usar una sola conexión para todo el lote es más eficiente
                try:
                    connection.open()
                except Exception as e:
                    logger.error(f"Error conectando al servidor SMTP: {e}")
                    messages.error(request, f"Error crítico conectando al servidor de correo: {e}")
                    return redirect(request.path)

                for user_recipient in recipients_list:
                    try:
                        context = {
                            "user": user_recipient,
                            "site_url": getattr(settings, 'SITE_URL', 'https://www.campustudionline.com'),
                            "asunto_correo": asunto_correo,
                        }
                        # Contexto específico por plantilla
                        if template_name_base == "admin_service_outage":
                            context.update({
                                "fecha_hora_mantenimiento": data["fecha_hora_mantenimiento"],
                                "duracion_mantenimiento": data["duracion_mantenimiento"],
                                "mensaje_adicional": data["mensaje_adicional_mantenimiento"],
                            })
                        elif template_name_base == "admin_general_announcement":
                            context.update({
                                "message_body": data["cuerpo_mensaje_general"], # Usamos message_body estandarizado
                            })

                        # Renderizado
                        text_content = render_to_string(txt_template, context)
                        html_content = render_to_string(html_template, context)

                        msg = EmailMultiAlternatives(
                            asunto_correo,
                            text_content,
                            settings.DEFAULT_FROM_EMAIL,
                            [user_recipient.email],
                            connection=connection
                        )
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                        email_sent_count += 1
                    
                    except Exception as e:
                        error_count += 1
                        logger.error(f"Error enviando a {user_recipient.username}: {e}", exc_info=True)
                        # No mostramos error por usuario en UI si son muchos, saturaría.
                        # Pero si son pocos sí. Limitamos a 5 errores visibles.
                        if error_count <= 5:
                            messages.error(request, f"Error con {user_recipient.username}: {e}")

                connection.close()

                # 5. RESULTADOS
                if email_sent_count > 0:
                    messages.success(request, f"Se enviaron correctamente {email_sent_count} correos.")
                
                if error_count > 0:
                    messages.warning(request, f"Falló el envío de {error_count} correos. Revisa los logs para más detalle.")
                
                if email_sent_count == 0 and error_count == 0:
                    messages.info(request, "No se enviaron correos (verifique configuración).")

                return redirect(request.path)
        else:
            messages.error(request, "El formulario contiene errores.")
    
    context_render = {
        "form": form,
        "title": "Enviar Correo a Usuarios",
        "has_permission": request.user.is_staff,
        "opts": MaintenanceSettings._meta,
    }
    return render(request, "admin/global_settings/send_custom_email.html", context_render)
