# /home/MiguelAeTxio/CampuStudiOnline/messaging/urls.py
from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    # Conversation URLs
    path("", views.conversation_list, name="conversation_list"),
    path(
        "chat_with/<str:username>/",
        views.conversation_detail,
        name="conversation_detail",
    ),
    path("start/<str:username>/", views.start_chat, name="start_chat"),
    path(
        "hide/<int:session_id>/", views.hide_conversation, name="hide_conversation"
    ),
    # URL to send invitations via email
    path(
        "send-invite/<str:username>/",
        views.send_invitation,
        name="send_invitation",
    ),
    # API URL to save the push notification subscription
    path(
        "save-subscription/",
        views.save_webpush_subscription,
        name="save_webpush_subscription",
    ),
    # URLs for cryptography management
    path("save_public_key/", views.save_public_key, name="save_public_key"),
    path("get_keys/", views.get_crypto_keys, name="get_crypto_keys"),
    # --- URLS FOR POLLING API ---
    path("api/send/<str:username>/", views.send_message, name="api_send_message"),
    path(
        "api/fetch/<str:username>/",
        views.fetch_messages,
        name="api_fetch_messages",
    ),
    path(
        "api/action/<str:username>/",
        views.message_action,
        name="api_message_action",
    ),
    # URLs for content sharing
    path(
        "api/get-study-copies/",
        views.get_study_copies,
        name="api_get_study_copies",
    ),
    path(
        "api/get-study-copy-details/<uuid:copy_id>/",
        views.get_study_copy_details,
        name="api_get_study_copy_details",
    ),
    path(
        "api/share-content/<str:username>/",
        views.share_content,
        name="api_share_content",
    ),
]
