import os
import django
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime

# Configuración del entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

def send_test_emails():
    target_email = "nummenor@gmail.com"
    print(f"\n--- Iniciando prueba COMPLETA de envío de emails a {target_email} ---\n")

    user = User.objects.filter(email=target_email).first()
    if not user:
        user = User.objects.first()
        if not user:
            print("ERROR CRÍTICO: No hay usuarios en la base de datos.")
            return
    
    print(f"Usuario de contexto: {user.username} ({user.email})\n")

    emails_to_test = [
        # --- GRUPO 1: AUTH & USUARIOS ---
        {
            "name": "1. Bienvenida Automática",
            "template": "emails/welcome_email.html",
            "subject": "TEST: ¡Bienvenido/a a CampuStudiOnline!",
            "context": {'user': user, 'site_url': 'https://www.campustudionline.com'}
        },
        {
            "name": "2. Restablecer Contraseña",
            "template": "users/emails/password_reset_email.html",
            "subject": "TEST: Restablece tu contraseña",
            "context": {'user': user, 'protocol': 'https', 'domain': 'www.campustudionline.com', 'uid': 'uid', 'token': 'token'}
        },
        {
            "name": "3. Activación de Cuenta",
            "template": "users/emails/account_activation_body.html",
            "subject": "TEST: Activa tu cuenta",
            "context": {'user': user, 'protocol': 'https', 'domain': 'www.campustudionline.com', 'uid': 'uid', 'token': 'token'}
        },
        
        # --- GRUPO 2: EVALUACIONES (ASSESSMENT) ---
        {
            "name": "4. Evaluación Lista",
            "template": "assessment/email/assessment_ready_body.html",
            "subject": "TEST: Tu evaluación está lista",
            "context": {'user': user, 'content_title': 'Introducción a Python', 'action_url': 'https://www.campustudionline.com/assessment/take/1/'}
        },
        {
            "name": "5. Resultados Evaluación",
            "template": "assessment/email/results_ready_body.html",
            "subject": "TEST: Tus resultados están listos",
            "context": {'user': user, 'content_title': 'Introducción a Python', 'action_url': 'https://www.campustudionline.com/assessment/results/1/'}
        },

        # --- GRUPO 3: COMUNICACIÓN Y FEEDBACK ---
        {
            "name": "6. Invitación Mensajería",
            "template": "messaging/email/invitation_email.html",
            "subject": "TEST: Invitación a chatear",
            "context": {'recipient_name': user.username, 'sender_name': 'Alice_Test', 'chat_url': 'https://www.campustudionline.com/messaging/'}
        },
        {
            "name": "7. Nuevo Reporte Feedback (Admin)",
            "template": "feedback/email/new_report_notification.html",
            "subject": "TEST: Nuevo Reporte de Error",
            "context": {'content_title': 'Curso de Django', 'reporter_username': 'Bob_Tester', 'report_title': 'Video roto', 'report_description': 'No carga.', 'admin_url': '/admin/'}
        },

        # --- GRUPO 4: ADMINISTRACIÓN MANUAL ---
        {
            "name": "8. Anuncio General",
            "template": "emails/admin_general_announcement.html",
            "subject": "TEST: Anuncio General",
            "context": {'user': user, 'email_subject': 'Novedades', 'message_body': 'Hemos actualizado la plataforma.'}
        },
        {
            "name": "9. Bienvenida Manual (Admin)",
            "template": "emails/admin_manual_welcome.html",
            "subject": "TEST: Bienvenida Manual",
            "context": {'user': user, 'site_url': 'https://www.campustudionline.com'}
        },
        {
            "name": "10. Aviso de Mantenimiento",
            "template": "emails/admin_service_outage.html",
            "subject": "TEST: Mantenimiento Programado",
            "context": {
                'user': user, 
                'fecha_hora_mantenimiento': 'Domingo 20:00h', 
                'duracion_mantenimiento': '2 horas',
                'mensaje_adicional': 'No podrás acceder a tus cursos.'
            }
        },

        # --- GRUPO 5: ORQUESTADOR Y AUTOMATIZACIÓN (LOS FUGITIVOS) ---
        {
            "name": "11. Notificación Orquestador (Admin)",
            "template": "orchestrator/email/admin_notification.html",
            "subject": "TEST: [Automation] Claves API en Cuarentena",
            "context": {'title': 'Claves API en Cuarentena', 'message_body': 'Se han detectado 3 claves agotadas.', 'dashboard_url': '/admin/orchestrator/'}
        },
        {
            "name": "12. Contenido Completado (Usuario)",
            "template": "orchestrator/email/content_completion.html",
            "subject": "TEST: ¡Contenido Disponible!",
            "context": {'content_title': 'Historia del Arte', 'content_url': 'https://www.campustudionline.com/contents/1/'}
        }
    ]

    for email_data in emails_to_test:
        print(f"Enviando: {email_data['name']}...")
        try:
            html_content = render_to_string(email_data['template'], email_data['context'])
            text_content = strip_tags(html_content)
            
            send_mail(
                email_data['subject'],
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [target_email],
                html_message=html_content,
                fail_silently=False
            )
            print("  -> OK")
        except Exception as e:
            print(f"  -> ERROR: {e}")

    print("\n--- Prueba finalizada. Verifica los 12 correos en tu bandeja. ---")

if __name__ == "__main__":
    send_test_emails()
