# /chat/urls.py

from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.chat_index, name="index"),
    path("create/", views.create_room, name="create_room"),
    path("room/<slug:room_slug>/", views.room_detail, name="room_detail"),
    
    # --- URLs para la API de Polling HTTP ---
    path(
        "api/room/<slug:room_slug>/send/",
        views.send_chat_message_api,
        name="send_message_api",
    ),
    path(
        "api/room/<slug:room_slug>/updates/",
        views.get_chat_updates_api,
        name="get_updates_api",
    ),
    path(
        "api/room/<slug:room_slug>/delete_message/<int:message_id>/",
        views.delete_message,
        name="delete_message",
    ),
    
    # --- URLs de gestión ---
    path("room/<slug:room_slug>/leave/", views.leave_room, name="leave_room"),
    path(
        "room/<slug:room_slug>/request_join/",
        views.request_join,
        name="request_join",
    ),
    path(
        "membership_request/<int:membership_id>/manage/<str:action>/",
        views.manage_membership,
        name="manage_membership",
    ),
    path(
        "room/<slug:room_slug>/toggle_moderator/<int:user_id_to_toggle>/",
        views.toggle_moderator,
        name="toggle_moderator",
    ),
    path(
        "room/<slug:room_slug>/toggle_silence/<int:user_id_to_silence>/",
        views.toggle_silence,
        name="toggle_silence",
    ),
]
