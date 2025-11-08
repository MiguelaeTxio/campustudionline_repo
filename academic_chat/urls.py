# /home/MiguelAeTxio/CampuStudiOnline/academic_chat/urls.py
from django.urls import path
from . import views

app_name = "academic_chat"

urlpatterns = [
    path("room/<slug:chat_slug>/", views.academic_chat_room, name="academic_chat_room"),
    path(
        "room/<slug:chat_slug>/enviar/",
        views.send_academic_chat_message_api,
        name="send_academic_chat_message_api",
    ),
    path(
        "room/<slug:chat_slug>/updates/",
        views.get_academic_chat_updates_api,
        name="get_academic_chat_updates_api",
    ),
    path(
        "room/<slug:chat_slug>/delete_message/<int:message_id>/",
        views.delete_academic_chat_message,
        name="delete_academic_chat_message",
    ),
    path("", views.university_list_view, name="university_list"),
    path("<slug:university_slug>/", views.branch_list_view, name="branch_list"),
    path(
        "<slug:university_slug>/<slug:branch_slug>/",
        views.degree_list_view,
        name="degree_list",
    ),
    path(
        "<slug:university_slug>/<slug:branch_slug>/<slug:degree_slug>/",
        views.academic_year_list_view,
        name="academic_year_list",
    ),
    path(
        "<slug:university_slug>/<slug:branch_slug>/<slug:degree_slug>/<int:year>/",
        views.academic_chat_list_view,
        name="academic_chat_list",
    ),
]
