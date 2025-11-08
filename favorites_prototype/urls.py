# /home/MiguelAeTxio/CampuStudiOnline/favorites_prototype/urls.py
from django.urls import path
from . import views

app_name = 'favorites_prototype'

urlpatterns = [
    path('', views.test_tree_view, name='test_tree'),
    path('folder/<int:folder_id>/', views.folder_detail_view, name='folder_detail'),
    path('create-folder/', views.create_folder_view, name='create_folder'),
    path('delete-folder/<int:folder_id>/', views.delete_folder_view, name='delete_folder'),
    path('rename-form/<int:folder_id>/', views.rename_folder_form_view, name='rename_form'),
    path('rename-folder/<int:folder_id>/', views.rename_folder_view, name='rename_folder'),
]


