# /home/MiguelAeTxio/CampuStudiOnline/messaging/push_utils.py
import json
import logging
from pywebpush import webpush, WebPushException
from django.conf import settings
from .models import UserSubscription
from django.contrib.staticfiles.storage import staticfiles_storage

logger = logging.getLogger("push_debugger")


def send_notification_to_user(
    user, title, body, url=None, encrypted_message_payload=None
):
    """
    Finds a user's active subscriptions in their browsers and sends
    a push notification to each one.
    Uses the "Fort Knox" architecture.
    """
    logger.info(
        f"[Fort Knox] Initiating send_notification_to_user for: '{user.username}'"
    )

    # The new logic: find active UserSubscriptions and preload related
    # models for efficiency.
    user_subscriptions = UserSubscription.objects.filter(
        user=user, is_active=True
    ).select_related("browser__push_endpoint")

    if not user_subscriptions.exists():
        logger.warning(
            f"[Fort Knox] No active subscriptions found for "
            f"'{user.username}'. Aborting send."
        )
        return

    logger.info(
        f"[Fort Knox] Found {user_subscriptions.count()} subscriptions "
        f"for '{user.username}'. Building payload."
    )

    try:
        icon_path = staticfiles_storage.url("images/web-app-manifest-192x192.png")
        icon_url = f"https://www.campustudionline.com{icon_path}"
    except Exception as e:
        logger.error(f"CRITICAL: Failed to generate icon URL: {e}", exc_info=True)
        icon_url = "https://www.campustudionline.com/static/images/web-app-manifest-192x192.png"
        logger.warning(f"Using fallback icon URL: {icon_url}")

    default_url = "https://www.campustudionline.com/"
    final_url = url if url else default_url

    payload = {
        "title": title,
        "body": body,
        "icon": icon_url,
        "data": {"url": final_url},
    }

    if encrypted_message_payload:
        payload["data"]["encrypted_message_payload"] = encrypted_message_payload
        payload["data"]["recipient_id"] = user.id
        logger.info("[Fort Knox] Encrypted payload added to the notification.")

    payload_json_string = json.dumps(payload, ensure_ascii=False, indent=2)
    logger.debug(f"[Fort Knox] Notification payload:\n{payload_json_string}")

    for sub in user_subscriptions:
        logger.info(
            f"[Fort Knox] Processing UserSubscription ID: {sub.id} "
            f"for Browser ID: {sub.browser.uuid}"
        )

        if not hasattr(sub.browser, "push_endpoint"):
            logger.warning(
                f"[Fort Knox] Subscription {sub.id} does not have an "
                f"associated PushEndpoint. Skipping."
            )
            continue

        push_endpoint = sub.browser.push_endpoint
        logger.debug(f"  -> Endpoint: {push_endpoint.endpoint}")

        try:
            subscription_info = {
                "endpoint": push_endpoint.endpoint,
                "keys": push_endpoint.keys,
            }

            webpush(
                subscription_info=subscription_info,
                data=json.dumps(payload),
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims={"sub": f"mailto:{settings.VAPID_ADMIN_EMAIL}"},
            )
            logger.info(f"SUCCESS: Notification sent to {sub.device_name}.")

        except WebPushException as ex:
            response_text = ex.response.text if ex.response else "N/A"
            response_status = ex.response.status_code if ex.response else "N/A"
            logger.error(f"FAILURE WebPushException for UserSub {sub.id}: {ex}")
            logger.error(f"  -> Code: {response_status}, Resp: {response_text}")

            # --- START: CORRECTED Automatic Sanitization Logic ---
            error_string = str(ex)
            if "Push failed: 404" in error_string or "Push failed: 410" in error_string:
                status_code_str = "404" if "404" in error_string else "410"
                logger.warning(
                    f"[Sanitization] Subscription {sub.id} for browser "
                    f"{sub.browser.uuid} returned a {status_code_str} error. "
                    f"It is considered obsolete and will be deleted."
                )
                try:
                    sub.delete()
                    logger.info(
                        f"[Sanitization] Subscription {sub.id} deleted successfully."
                    )
                except Exception as delete_exc:
                    logger.error(
                        f"[Sanitization] Error while trying to delete obsolete subscription {sub.id}: {delete_exc}",
                        exc_info=True,
                    )
            # --- END: CORRECTED Automatic Sanitivation Logic ---

        except Exception as e:
            logger.error(
                f"UNEXPECTED FAILURE processing UserSub {sub.id}: {e}", exc_info=True
            )

    logger.info(f"[Fort Knox] Sending process for '{user.username}' finished.")
