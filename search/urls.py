# /home/MiguelAeTxio/CampuStudiOnline/search/urls.py
from django.urls import path, re_path
from . import views

app_name = "search"

urlpatterns = [
    # --- Main Entry Points ---
    path("", views.search_home_view, name="search_home"),
    path("global/", views.global_search_view, name="global_search"),

    # --- NEW: Free Content Hierarchy URLs ---
    path("free/<slug:master_slug>/", views.free_content_category_detail_view, name="free_master_detail"),
    path("free/<slug:master_slug>/<slug:sub_slug>/", views.free_content_category_detail_view, name="free_sub_detail"),

    # --- REFACTORED: Academic Hierarchy URLs ---
    path("academic/<slug:area_slug>/", views.academic_category_detail_view, name="academic_area_detail"),
    path(
        "academic/<slug:area_slug>/<slug:discipline_slug>/",
        views.academic_category_detail_view,
        name="academic_discipline_detail",
    ),
    path(
        "academic/<slug:area_slug>/<slug:discipline_slug>/<slug:main_category_slug>/",
        views.academic_category_detail_view,
        name="academic_main_category_detail",
    ),
    re_path(
        r"^academic/(?P<area_slug>[-\w]+)/(?P<discipline_slug>[-\w]+)/(?P<main_category_slug>[-\w]+)/(?P<topic_slug_path>[-\w/]+)/$",
        views.academic_category_detail_view,
        name="academic_topic_detail",
    ),
]
