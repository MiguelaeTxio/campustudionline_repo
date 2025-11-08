# announcements/urls.py
from django.urls import path
from . import views

app_name = "announcements"  # Espacio de nombres

urlpatterns = [
    path(
        "", views.announcement_list, name="announcement_list"
    ),  # Root URL for the announcements app
    path(
        "new/", views.create_announcement, name="create_announcement"
    ),  # URL para crear un anuncio
]
