# /home/MiguelAeTxio/CampuStudiOnline/contents/study_room_urls.py
from django.urls import path
from django.views.generic import RedirectView
from . import study_room_views

app_name = "study_room"

urlpatterns = [
    # --- Raíz y Navegación Académica ---
    path("directory/", study_room_views.user_copies_list, name="copy_directory_root"),
    path("directory/academic/<slug:area_slug>/", study_room_views.user_copies_list, name="copy_directory_area"),
    path("directory/academic/<slug:area_slug>/<slug:discipline_slug>/", study_room_views.user_copies_list, name="copy_directory_discipline"),
    
    # --- Navegación de Contenido Libre ---
    path("directory/free/<slug:master_slug>/", study_room_views.user_copies_list, name="free_master_directory"),
    path("directory/free/<slug:master_slug>/<slug:sub_slug>/", study_room_views.user_copies_list, name="free_sub_directory"),

    # --- Gestión de Copias y Anotaciones ---
    path("content/<uuid:pk>/in-subject/<uuid:subject_pk>/create-copy/", study_room_views.create_content_copy, name="create_content_copy"),
    path("content/<uuid:pk>/create-copy/", study_room_views.create_content_copy, name="create_free_content_copy"), # Para contenido libre
    path("copy/<uuid:pk>/", RedirectView.as_view(pattern_name="study_room:edit_copy", permanent=False), name="detail_copy"),
    path("copy/<uuid:pk>/edit/", study_room_views.edit_copy, name="edit_copy"),
    path("copy/<uuid:pk>/visibility/", study_room_views.change_copy_visibility, name="change_copy_visibility"),
    path("copy/<uuid:pk>/delete/", study_room_views.delete_copy, name="delete_copy"),
    path("copy/<uuid:pk>/annotation/create/", study_room_views.create_annotation, name="create_annotation"),
    path("annotation/<uuid:pk>/delete/", study_room_views.delete_annotation, name="delete_annotation"),
]
