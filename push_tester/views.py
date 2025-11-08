import logging
import os
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from .forms import PushTestForm
from messaging.push_utils import send_notification_to_user

# Get our custom logger configured in settings.py
logger = logging.getLogger("push_debugger")


class SuperuserRequiredMixin(UserPassesTestMixin):
    """
    Mixin to restrict access to superusers only.
    """

    def test_func(self):
        return self.request.user.is_superuser


class PushTestView(SuperuserRequiredMixin, View):
    """
    View for testing the sending of push notifications.
    Accessible only by superusers.
    """

    template_name = "push_tester/test_page.html"
    form_class = PushTestForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_to_notify = form.cleaned_data["user"]
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]

            logger.info(
                "===================================================================="
            )
            logger.info(
                f"START OF PUSH NOTIFICATION TEST. Target User: {user_to_notify.username}"
            )
            logger.info(
                "===================================================================="
            )

            # --- FORENSIC LOGGING OF THE CONFIGURATION ---
            logger.debug("--- Configuration Check (settings.py) ---")
            logger.debug(f"DEBUG flag: {settings.DEBUG}")

            try:
                storages_backend = settings.STORAGES["staticfiles"]["BACKEND"]
                logger.debug(f"STORAGES['staticfiles']['BACKEND']: {storages_backend}")
            except (KeyError, AttributeError):
                logger.warning("STORAGES['staticfiles']['BACKEND'] is not defined.")

            vapid_public_key = getattr(settings, "VAPID_PUBLIC_KEY", "NOT FOUND")
            vapid_private_key = getattr(settings, "VAPID_PRIVATE_KEY", "NOT FOUND")
            vapid_admin_email = getattr(settings, "VAPID_ADMIN_EMAIL", "NOT FOUND")

            logger.debug(f"VAPID_PUBLIC_KEY: {vapid_public_key}")
            logger.debug(
                f"VAPID_PRIVATE_KEY: (Showing only first 5 and last 5 chars for security) "
                f"{vapid_private_key[:5]}...{vapid_private_key[-5:] if isinstance(vapid_private_key, str) else 'N/A'}"
            )
            logger.debug(f"VAPID_ADMIN_EMAIL: {vapid_admin_email}")
            logger.debug("--- End of Configuration Check ---")

            try:
                send_notification_to_user(user=user_to_notify, title=title, body=body)
                messages.success(
                    request,
                    f"Notification send attempt for '{user_to_notify.username}' completed. Check the log file for details.",
                )
                logger.info(
                    "Call to send_notification_to_user finished without exceptions."
                )

            except Exception as e:
                logger.error(
                    f"UNEXPECTED EXCEPTION in view when calling send_notification_to_user: {e}",
                    exc_info=True,
                )
                messages.error(
                    request,
                    f"A catastrophic error occurred while trying to send the notification. Check the log.",
                )

            logger.info(
                "===================================================================="
            )
            logger.info("END OF PUSH NOTIFICATION TEST.")
            logger.info(
                "===================================================================="
            )

            return redirect("push_tester:test_page")

        return render(request, self.template_name, {"form": form})


class ViewLogFileView(SuperuserRequiredMixin, View):
    """
    A secure view to display the content of the debug log file.
    """

    def get(self, request, *args, **kwargs):
        log_file_path = os.path.join(settings.BASE_DIR, "logs", "push_debug.log")
        try:
            with open(log_file_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Return the content as plain text
            return HttpResponse(content, content_type="text/plain; charset=utf-8")
        except FileNotFoundError:
            message = f"Log file not found at the expected path:\n{log_file_path}\n\nMake sure you have sent at least one test notification for it to be generated."
            return HttpResponse(
                message, content_type="text/plain; charset=utf-8", status=404
            )
        except Exception as e:
            message = (
                f"An unexpected error occurred while reading the log file:\n{str(e)}"
            )
            return HttpResponse(
                message, content_type="text/plain; charset=utf-8", status=500
            )
