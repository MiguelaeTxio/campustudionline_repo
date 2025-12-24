from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import AcademicEvent
from messaging.push_utils import send_notification_to_user
import logging

logger = logging.getLogger("django")

@shared_task
def check_scheduled_reminders():
    """
    Comprueba eventos académicos que comienzan en las próximas 24 horas
    y envía notificaciones (Push y Email) si no se han enviado aún.
    """
    now = timezone.now()
    time_threshold = now + timedelta(hours=24)
    
    # Buscamos eventos futuros cercanos (entre ahora y +24h) sin recordatorio enviado
    events = AcademicEvent.objects.filter(
        start_time__gt=now,
        start_time__lte=time_threshold,
        reminder_sent=False
    ).select_related('user', 'subject')
    
    count = 0
    for event in events:
        try:
            # 1. Preparar datos
            time_str = event.start_time.strftime("%H:%M")
            if event.is_all_day:
                time_str = "Todo el día"
                
            subject_name = event.subject.name if event.subject else "Evento General"
            title = f"📅 Recordatorio: {event.title}"
            body = f"Mañana tienes: {event.get_event_type_display()} de {subject_name} a las {time_str}."
            
            # 2. Enviar Push Notification (Prioridad Alta)
            send_notification_to_user(
                user=event.user,
                title=title,
                body=body,
                url="/schedule/" # Enlace directo al calendario
            )
            
            # 3. Enviar Email (Respaldo)
            # Solo si el usuario tiene email válido.
            if event.user.email:
                send_mail(
                    subject=title,
                    message=body + "\n\nAccede a tu agenda en: https://www.campustudionline.com/schedule/",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[event.user.email],
                    fail_silently=True
                )
            
            # 4. Marcar como enviado
            event.reminder_sent = True
            event.save(update_fields=['reminder_sent'])
            count += 1
            
        except Exception as e:
            logger.error(f"Error enviando recordatorio para evento {event.id}: {e}")
            
    return f"Se enviaron {count} recordatorios de agenda."
