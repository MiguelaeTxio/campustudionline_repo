# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/contents/urls.py
from django.urls import path
from . import views

app_name = "contents"

urlpatterns = [
    # --- Material Content URLs ---
    path("create/", views.create_content, name="create_content"),
    path("<uuid:pk>/edit/", views.edit_content, name="edit_content"),
    path("<uuid:pk>/delete/", views.delete_content, name="delete_content"),
    
    # [NUEVA RUTA] Ruta específica para cuando se accede a un material desde una asignatura.
    path("from-subject/<uuid:subject_pk>/material/<uuid:pk>/", views.content_detail, name="content_detail_academic"),
    
    # Ruta genérica para acceso directo o desde contenido libre.
    path("<uuid:pk>/", views.content_detail, name="content_detail"),

    # --- Personal Workspace & Favorites (Arquitectura PAIR) ---
    path("workspace/", views.personal_workspace_view, name="personal_workspace"),
    path("workspace/folder/<uuid:folder_id>/", views.favorite_folder_detail_view, name="favorite_folder_detail"),
    
    # --- HTMX CRUD Endpoints ---
    path("workspace/create-folder/", views.create_folder_htmx_view, name="create_folder"),
    path("workspace/delete-folder/<uuid:folder_id>/", views.delete_folder_htmx_view, name="delete_folder"),
    path("workspace/rename-form/<uuid:folder_id>/", views.rename_folder_form_htmx_view, name="rename_folder_form"),
    path("workspace/rename-folder/<uuid:folder_id>/", views.rename_folder_htmx_view, name="rename_folder"),
    path("workspace/move-element/", views.move_element_htmx_view, name="move_element"),
    path("workspace/remove-material/<uuid:material_id>/from/<uuid:folder_id>/", views.remove_material_from_folder_htmx_view, name="remove_material_from_folder"),
    path("workspace/toggle-favorite/<uuid:pk>/", views.toggle_favorite_htmx_view, name="toggle_favorite_htmx"),
    path("workspace/get-folder-options/", views.get_folder_options_htmx_view, name="get_folder_options_htmx"),
    
    # --- SEO & Social Share Image URLs ---
    path("share_image/<uuid:pk>/", views.generate_share_image, name="generate_share_image"),
    path("share_image/default/", views.generate_default_share_image, name="generate_default_share_image"),

]
