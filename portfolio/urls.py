# portfolio/urls.py
from django.urls import path
from . import views

app_name = "portfolio"

urlpatterns = [
    path(
        "<str:username>/",
        views.public_portfolio_detail,
        name="public_portfolio_detail",
    ),
    path("messages/new/", views.create_short_message, name="create_short_message"),
    path(
        "messages/<int:pk>/delete/",
        views.delete_short_message,
        name="delete_short_message",
    ),
    path("links/new/", views.create_user_link, name="create_user_link"),
    path(
        "links/<int:pk>/delete/",
        views.delete_user_link,
        name="delete_user_link",
    ),
    path(
        "settings/chat-privacy/",
        views.update_chat_privacy_settings,
        name="update_chat_privacy_settings",
    ),
]
