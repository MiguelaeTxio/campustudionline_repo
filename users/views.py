# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/users/views.py
from django.core.signing import TimestampSigner, BadSignature
from django.shortcuts import get_object_or_404
# /home/MiguelAeTxio/CampuStudiOnline/users/views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, views as auth_views
from django.contrib.auth import get_user_model

User = get_user_model()
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm,
)
from .models import UserProfile, ArchivedKey, RecommendationCode
from django.utils import timezone
from .decorators import commercial_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.db import transaction
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMultiAlternatives, mail_admins
from .tokens import account_activation_token
from django.contrib.auth.tokens import default_token_generator

from .tasks import cleanup_inactive_user, send_meta_conversion_event
import hashlib
import time



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_multipart_email(
    subject_template, text_template, html_template, context, to_email
):
    """
    Renderiza y envía un correo electrónico con versión HTML y de texto plano.
    """
    subject = render_to_string(subject_template, context).strip()
    text_content = render_to_string(text_template, context)
    html_content = render_to_string(html_template, context)

    msg = EmailMultiAlternatives(subject, text_content, to=[to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# --- VISTAS GENERALES ---
def home_view(request):
    """
    Renderiza la página de inicio.
    """
    show_tour = not request.COOKIES.get("home_tour_completed", False)
    # --- META PIXEL EVENT CONSUMPTION ---
    pixel_event = request.session.pop("meta_pixel_event", None)
    # ------------------------------------
    return render(
        request, "home.html", {"page_title": "Inicio", "show_tour": show_tour, "meta_event": pixel_event}
    )


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Disallow: /cuentas/",
        "Disallow: /sala-estudio/",
        "Disallow: /chat/",
        "Disallow: /mensajes/",
        "Allow: /",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


# --- VISTAS DE REGISTRO Y ACTIVACIÓN ---
def register(request):
    form = UserRegistrationForm()
    return render(
        request,
        "users/register.html",
        {"form": form, "page_title": "Registro de Usuario"},
    )


@require_POST
def validate_registration_view(request):
    """
    Validates the registration data and prepares the activation flow.
    -----------------------------------------------------------------
    Valida los datos de registro y prepara el flujo de activación.
    """
    User = get_user_model()
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "status": "error",
                "errors": {"__all__": "Formato de solicitud inválido."},
            },
            status=400,
        )

    form = UserRegistrationForm(data)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # --- LÓGICA DE REFERIDOS (VERSIÓN CORREGIDA AAAA) ---
        # Store the referral code in the profile for consumption after activation.
        # ------------------------------------------------------------------------
        # Almacena el código de referido en el perfil para su consumo tras la activación.
        referral_code = form.cleaned_data.get("referral_code")
        if referral_code:
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.pending_referral_code = referral_code
            profile.save()
        # ----------------------------------------------------

        current_site = get_current_site(request)
        
        context = {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        }

        send_multipart_email(
            "users/emails/account_activation_subject.txt",
            "users/emails/account_activation_body.txt",
            "users/emails/account_activation_body.html",
            context,
            user.email,
        )

        cleanup_inactive_user.apply_async(args=[user.id], countdown=600)

        redirect_url = reverse("users:registration_pending")
        return JsonResponse({"status": "success", "redirect_url": redirect_url})
    else:
        errors = form.errors.get_json_data()
        if "email" in errors and any(
            e.get("code") == "inactive_account" for e in errors["email"]
        ):
            try:
                user_email = data.get("email", "")
                inactive_user = User.objects.get(
                    email__iexact=user_email, is_active=False
                )

                current_site = get_current_site(request)
                
                context = {
                    "user": inactive_user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(inactive_user.pk)),
                    "token": account_activation_token.make_token(inactive_user),
                    "protocol": "https" if request.is_secure() else "http",
                }

                send_multipart_email(
                    "users/emails/account_reactivation_subject.txt",
                    "users/emails/account_reactivation_body.txt",
                    "users/emails/account_reactivation_body.html",
                    context,
                    inactive_user.email,
                )

                redirect_url = reverse("users:registration_pending")
                return JsonResponse({"status": "success", "redirect_url": redirect_url})

            except User.DoesNotExist:
                return JsonResponse(
                    {
                        "status": "error",
                        "errors": {"__all__": ["Ha ocurrido un error inesperado."]},
                    },
                    status=400,
                )

        return JsonResponse(
            {"status": "error", "errors": json.loads(form.errors.as_json())}, status=400
        )


def activate_account_view(request, uidb64, token):
    User = get_user_model()
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is None:
        messages.error(request, "El enlace de activación es inválido (Usuario no encontrado).")
        return redirect("home")

    if user.is_active:
        messages.info(request, "Tu cuenta ya está activa. Puedes iniciar sesión.")
        return redirect("home")

    if not account_activation_token.check_token(user, token):
        messages.error(request, "El enlace de activación es inválido o ha expirado (Token incorrecto).")
        return redirect("home")

    user.is_active = True
    user.save()
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    # --- LÓGICA DE CONSUMO DE CÓDIGO DE REFERIDO (Refactorizada) ---
    try:
        profile = user.userprofile
        if profile.pending_referral_code:
            try:
                rec_code = RecommendationCode.objects.get(code=profile.pending_referral_code, redeemed_by__isnull=True)
                
                # Consumir el código
                rec_code.redeemed_by = user
                rec_code.date_redeemed = timezone.now()
                rec_code.save()
                
                # Asignar la atribución permanente
                profile.referred_by = rec_code.vendor
                profile.pending_referral_code = None # Limpiar el campo temporal
                profile.save()
                
                messages.info(request, f"Has sido invitado por {rec_code.vendor.username}. ¡Bienvenido!")

            except RecommendationCode.DoesNotExist:
                # El código ya fue usado por otro o es inválido, fallo silencioso para el usuario
                profile.pending_referral_code = None
                profile.save()
    except UserProfile.DoesNotExist:
        # No debería ocurrir si el registro funciona bien, pero es una salvaguarda
        pass
    # -----------------------------------------------------------------

    
    try:
        email_hash = hashlib.sha256(user.email.strip().lower().encode('utf-8')).hexdigest()
        event_id = f"reg_{user.id}_{int(time.time())}"
        
        user_details = {
            'email_hash': email_hash,
            'client_ip_address': get_client_ip(request),
            'client_user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'fbc': request.COOKIES.get('_fbc'),
            'fbp': request.COOKIES.get('_fbp'),
        }
        
        send_meta_conversion_event.delay(
            event_name='CompleteRegistration',
            user_details=user_details,
            event_id=event_id,
            source_url=request.build_absolute_uri()
        )
        
        request.session['meta_pixel_event'] = {
            'name': 'CompleteRegistration',
            'id': event_id
        }
        
    except Exception as e:
        print(f"Error triggering Meta Registration Event: {e}")

    messages.success(
        request,
        "¡Felicidades! Tu cuenta ha sido activada correctamente. Ya puedes usar la plataforma.",
    )
    return redirect("home")


def reactivate_account_view(request, uidb64, token):
    User = get_user_model()
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if (
        user is not None
        and not user.is_active
        and account_activation_token.check_token(user, token)
    ):
        messages.info(
            request,
            "Cuenta verificada. Por favor, establece una nueva contraseña para completar la reactivación.",
        )
        reset_token = default_token_generator.make_token(user)
        reset_url = reverse(
            "users:password_reset_confirm", kwargs={"uidb64": uidb64, "token": reset_token}
        )
        return redirect(reset_url)
    else:
        messages.error(
            request,
            "El enlace de reactivación es inválido o ha expirado. Por favor, intenta registrarte de nuevo.",
        )
        return redirect("home")


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    def form_valid(self, form):
        response = super().form_valid(form)
        self.user.is_active = True
        self.user.save()
        login(
            self.request, self.user, backend="django.contrib.auth.backends.ModelBackend"
        )
        messages.success(
            self.request,
            "¡Tu cuenta ha sido reactivada y tu contraseña actualizada! Ya estás dentro.",
        )
        return response


@login_required
def account_detail(request):
    return render(request, "users/account_detail.html", {"page_title": "Mi Cuenta"})


@login_required
def account_settings(request):
    if request.method == "POST":
        form_user = UserEditForm(request.POST, instance=request.user)
        if form_user.is_valid():
            form_user.save()
            messages.success(
                request, "¡La configuración de tu cuenta ha sido actualizada!"
            )
            return redirect("users:account_settings")
    else:
        form_user = UserEditForm(instance=request.user)

    return render(
        request,
        "users/account_settings.html",
        {"page_title": "Configuración de la Cuenta", "form_user": form_user},
    )


@login_required
def edit_profile(request):
    if request.method == "POST":
        form_profile = ProfileEditForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        if form_profile.is_valid():
            form_profile.save()
            messages.success(request, "¡Tu profile ha sido actualizado!")
            return redirect("users:edit_profile")
    else:
        form_profile = ProfileEditForm(instance=request.user.userprofile)

    return render(
        request,
        "users/edit_profile.html",
        {"page_title": "Editar Perfil y Privacidad", "form_profile": form_profile},
    )


@login_required
def request_deletion(request):
    return render(
        request,
        "users/confirm_deletion.html",
        {"page_title": "Confirmar Eliminación de Cuenta"},
    )


@login_required
@require_POST
def delete_account(request):
    user = request.user
    password = request.POST.get("password")

    if not password:
        messages.error(
            request, "Debes introducir tu contraseña para confirmar la eliminación."
        )
        return redirect("users:request_deletion")

    if not user.check_password(password):
        messages.error(request, "La contraseña introducida es incorrecta.")
        return redirect("users:request_deletion")

    user.is_active = False
    user.save()

    logout(request)

    messages.success(
        request, "Tu cuenta ha sido eliminada. Esperamos verte de nuevo pronto."
    )

    return redirect("home")


@login_required
@require_POST
def toggle_block_user(request, username):
    User = get_user_model()
    user_to_toggle = get_object_or_404(User, username=username)
    profile = request.user.userprofile
    if user_to_toggle == request.user:
        messages.error(request, "No puedes bloquearte a ti mismo.")
        return redirect("home")
    if user_to_toggle in profile.blocked_users.all():
        profile.blocked_users.remove(user_to_toggle)
        messages.success(request, f"Has desbloqueado a {user_to_toggle.username}.")
    else:
        profile.blocked_users.add(user_to_toggle)
        messages.success(request, f"Has bloqueado a {user_to_toggle.username}.")
    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def setup_security(request):
    return render(
        request,
        "users/setup_security.html",
        {"page_title": "Configuración de Seguridad"},
    )


@require_POST
@login_required
@transaction.atomic
def save_crypto_keys(request):
    try:
        data = json.loads(request.body)
        public_key = data.get("public_key")
        encrypted_private_key = data.get("encrypted_private_key")
        encryption_salt = data.get("encryption_salt")

        if not all([public_key, encrypted_private_key, encryption_salt]):
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Faltan datos (clave pública, privada o sal).",
                },
                status=400,
            )

        profile = request.user.userprofile

        if profile.encrypted_private_key and profile.encrypted_private_key.strip():
            ArchivedKey.objects.create(
                profile=profile, encrypted_private_key=profile.encrypted_private_key
            )

        profile.public_key = public_key
        profile.encrypted_private_key = encrypted_private_key
        profile.encryption_salt = encryption_salt
        profile.save()

        ArchivedKey.objects.get_or_create(
            profile=profile, encrypted_private_key=encrypted_private_key
        )

        return JsonResponse(
            {
                "status": "success",
                "message": "Claves guardadas y archivadas correctamente.",
            }
        )

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@login_required
@require_POST
def verify_password(request):
    try:
        data = json.loads(request.body)
        password = data.get("password")

        if not password:
            return JsonResponse(
                {"status": "error", "message": "No se proporcionó la contraseña."},
                status=400,
            )

        user = request.user
        if user.check_password(password):
            return JsonResponse(
                {"status": "success", "message": "Contraseña verificada correctamente."}
            )
        else:
            return JsonResponse(
                {"status": "error", "message": "La contraseña es incorrecta."},
                status=403,
            )

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "status": "error",
                "message": "Error en el formato de la solicitud (JSON inválido).",
            },
            status=400,
        )
    except Exception as e:
        return JsonResponse(
            {"status": "error", "message": f"Ocurrió un error inesperado: {str(e)}"},
            status=500,
        )

# --- VISTAS COMERCIALES ---
@login_required
@commercial_required
def commercial_dashboard(request):
    """
    Dashboard para usuarios del grupo 'Comerciales'.
    Muestra métricas de sus códigos y conversiones.
    """
    vendor = request.user
    
    # Métricas de Códigos
    available_codes = RecommendationCode.objects.filter(vendor=vendor, redeemed_by__isnull=True).order_by('code')
    used_codes = RecommendationCode.objects.filter(vendor=vendor, redeemed_by__isnull=False).select_related('redeemed_by').order_by('-date_redeemed')
    
    # Métricas de Conversión
    registration_conversions = used_codes.count()
    
    copy_conversions = vendor.referrals.filter(has_claimed_copy_incentive=True).count()
    assessment_conversions = vendor.referrals.filter(has_claimed_assessment_incentive=True).count()
    
    context = {
        'page_title': 'Dashboard Comercial',
        'available_codes': available_codes,
        'used_codes': used_codes,
        'registration_conversions': registration_conversions,
        'copy_conversions': copy_conversions,
        'assessment_conversions': assessment_conversions,
    }
    
    return render(request, "users/commercial_dashboard.html", context)


@require_POST
@login_required
@commercial_required
def request_new_code_batch(request):
    """
    Gestiona la solicitud de un nuevo lote de códigos por parte de un comercial.
    Es un autoservicio condicional: solo funciona si no tiene códigos disponibles.
    Notifica a los administradores para auditoría.
    """
    commercial = request.user
    
    if RecommendationCode.objects.filter(vendor=commercial, redeemed_by__isnull=True).exists():
        messages.error(request, "Aún tienes códigos disponibles. Debes agotarlos antes de solicitar un nuevo lote.")
        return redirect("users:commercial_dashboard")
        
    batch_size = 5
    codes_created = RecommendationCode.generate_batch(vendor=commercial, amount=batch_size)
    
    if codes_created > 0:
        subject = f"Auditoría: Nuevo lote de códigos para {commercial.username}"
        message = f"""El sistema ha generado automáticamente un nuevo lote de {codes_created} códigos de recomendación para el comercial '{commercial.username}'.
        
Este es un correo de notificación para fines de auditoría y seguimiento de pagos. No se requiere ninguna acción inmediata."""
        try:
            mail_admins(subject, message, fail_silently=False)
        except Exception as e:
            print(f"ERROR: No se pudo enviar el email de auditoría de códigos. {e}")
            
        messages.success(request, f"Se ha generado un nuevo lote de {codes_created} códigos.")
    else:
        messages.error(request, "No se pudieron generar nuevos códigos en este momento. Por favor, contacta con un administrador.")
        
    return redirect("users:commercial_dashboard")


def unsubscribe_view(request, token):
    signer = TimestampSigner()
    try:
        # Validar el token. No ponemos max_age para que el link sea perpetuo (UX estándar en bajas)
        user_id = signer.unsign(token)
        user = get_object_or_404(User, pk=user_id)
        
        # Actualizar preferencia
        if hasattr(user, 'userprofile'):
            user.userprofile.accepts_marketing = False
            user.userprofile.save()
            
        return render(request, 'users/unsubscribe.html', {'user_name': user.username})
        
    except (BadSignature, User.DoesNotExist):
        # Si el token es inválido, redirigimos a home o mostramos error genérico
        # para no filtrar información de usuarios.
        messages.error(request, "El enlace de baja no es válido o ha expirado.")
        return redirect('home')
