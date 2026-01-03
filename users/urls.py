"""
Custom URL definitions for the users application.
Standard authentication URLs (login, logout, etc.) are handled
by 'django.contrib.auth.urls' included in core/urls.py,
but we override those we need to customize.
"""
from django.urls import path, include
from . import views as user_views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path(
        "unsubscribe/<str:token>/",
        user_views.unsubscribe_view,
        name="unsubscribe",
    ),

    # User-facing URLs (HTML pages)
    # =======================================
    path("register/", user_views.register, name="register"),
    path(
        "register/pending/",
        TemplateView.as_view(template_name="users/registration_pending.html"),
        name="registration_pending",
    ),
    path(
        "activate/<uidb64>/<token>/",
        user_views.activate_account_view,
        name="activate_account",
    ),
    path(
        "reactivate/<uidb64>/<token>/",
        user_views.reactivate_account_view,
        name="reactivate_account",
    ),
    # --- Overriding Django's authentication views ---
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="users/emails/password_reset_email.html",
            subject_template_name="users/emails/password_reset_subject.txt",
            success_url="/cuentas/password_reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "reset/<uidb64>/<token>/",
        user_views.CustomPasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url="/cuentas/login/",
        ),
        name="password_reset_confirm",
    ),
    # Include the rest of Django's auth URLs. Ours take precedence.
    path("", include("django.contrib.auth.urls")),
    path("setup-security/", user_views.setup_security, name="setup_security"),
    # --- Account and Profile Management Routes ---
    path("account/", user_views.account_detail, name="account_detail"),
    path(
        "account/settings/",
        user_views.account_settings,
        name="account_settings",
    ),
    path("account/profile/", user_views.edit_profile, name="edit_profile"),
    path(
        "account/delete/",
        user_views.request_deletion,
        name="request_deletion",
    ),
    path(
        "account/delete/confirm/",
        user_views.delete_account,
        name="delete_account",
    ),
    path(
        "block/<str:username>/",
        user_views.toggle_block_user,
        name="toggle_block_user",
    ),
        # --- Commercial Dashboard ---
    path(
        "commercial/dashboard/",
        user_views.commercial_dashboard,
        name="commercial_dashboard",
    ),
    path(
        "commercial/request-codes/",
        user_views.request_new_code_batch,
        name="request_new_code_batch",
    ),

# --- API URLs ---
    path(
        "api/validate-registration/",
        user_views.validate_registration_view,
        name="validate_registration",
    ),
    path(
        "api/save-crypto-keys/",
        user_views.save_crypto_keys,
        name="save_crypto_keys",
    ),
    path(
        "api/verify-password/",
        user_views.verify_password,
        name="verify_password",
    ),
]
