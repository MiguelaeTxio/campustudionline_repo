import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.urls import reverse
from contents.models import ContentMaterial
from messaging.push_utils import send_notification_to_user
from .models import FeedbackReport
from .forms import FeedbackReportForm

# Usamos el logger de django por defecto
logger = logging.getLogger('django')

User = get_user_model()

@login_required
def report_content_error(request, content_pk):
    content = get_object_or_404(ContentMaterial, pk=content_pk)
    
    if request.method == 'POST':
        form = FeedbackReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.report_type = FeedbackReport.TYPE_CONTENT_ERROR
            report.content_material = content
            report.save()
            logger.info(f"[Feedback] Reporte {report.id} guardado. Iniciando notificaciones.")
            
            # --- Notificaciones al Superusuario ---
            try:
                # Obtener superusuarios
                superusers = User.objects.filter(is_superuser=True)
                logger.info(f"[Feedback] Encontrados {superusers.count()} superusuarios para notificar.")
                
                for su in superusers:
                    # 1. Notificación Push
                    try:
                        push_title = "⚠️ Nuevo Reporte de Contenido"
                        push_body = f"{request.user.username} reportó un error en '{content.title}'."
                        admin_url = reverse('admin:feedback_feedbackreport_change', args=[report.id])
                        
                        send_notification_to_user(
                            user=su,
                            title=push_title,
                            body=push_body,
                            url=admin_url
                        )
                        logger.info(f"[Feedback] Push enviado a {su.username}")
                    except Exception as push_e:
                         logger.error(f"[Feedback] Error enviando Push a {su.username}: {push_e}")
                    
                    # 2. Correo Electrónico
                    try:
                        send_mail(
                            subject=f"[CampuStudiOnline] Nuevo Reporte: {content.title}",
                            message=f"""
                            Se ha recibido un nuevo reporte de error.
                            
                            Usuario: {request.user.username}
                            Contenido: {content.title}
                            Asunto: {report.title}
                            Descripción:
                            {report.description}
                            
                            Gestionar en admin: https://www.campustudionline.com{admin_url}
                            """,
                            from_email=None,
                            recipient_list=[su.email],
                            fail_silently=False 
                        )
                        logger.info(f"[Feedback] Email enviado a {su.email}")
                    except Exception as mail_e:
                        logger.error(f"[Feedback] Error enviando Email a {su.email}: {mail_e}")

            except Exception as e:
                logger.error(f"[Feedback] Error general en bloque de notificaciones: {e}", exc_info=True)

            messages.success(request, "Gracias por tu reporte. Lo revisaremos lo antes posible.")
            return redirect(content.get_absolute_url())
    else:
        initial_data = {'title': f"Error en: {content.title}"}
        form = FeedbackReportForm(initial=initial_data)
    
    return render(request, 'feedback/report_form.html', {
        'form': form,
        'content_material': content,
        'is_content_report': True
    })

@login_required
def submit_general_feedback(request):
    if request.method == 'POST':
        form = FeedbackReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.report_type = FeedbackReport.TYPE_SUGGESTION
            report.save()
            messages.success(request, "Gracias por tu feedback. Tu opinión es muy importante para nosotros.")
            return redirect('home')
    else:
        form = FeedbackReportForm()
    
    return render(request, 'feedback/report_form.html', {
        'form': form,
        'is_content_report': False
    })
