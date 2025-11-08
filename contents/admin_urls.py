# /home/MiguelAeTxio/CampuStudiOnline/contents/admin_urls.py
from django.urls import path
from . import admin_views

app_name = 'contents_admin'

urlpatterns = [
    path('ajax/load-subcategories/', admin_views.ajax_load_subcategories, name='ajax_load_subcategories'),
]
