# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/core/urls.py
from django.contrib import admin
from django.urls import path, include, re_path, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from users import views as user_views
from core import views as core_views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import (
    StaticPublicViewSitemap,
    UniversitySitemap,
    BranchSitemap,
    DegreeSitemap,
    AcademicYearSitemap,
    SubjectSitemap,
    PublicContentMaterialSitemap,
    FreeContentCategorySitemap,
    FreeContentSubCategorySitemap
)
from contents import study_room_urls as study_room_urls_module
from messaging.views import ServiceWorkerView
from django.views.i18n import JavaScriptCatalog

from django.contrib.auth import views as auth_views

sitemaps_dict = {
    "static_public": StaticPublicViewSitemap,
    "universities": UniversitySitemap,
    "branches": BranchSitemap,
    "degrees": DegreeSitemap,
    "academic_years": AcademicYearSitemap,
    "subjects": SubjectSitemap,
    "public_contents": PublicContentMaterialSitemap,
    "free_content_categories": FreeContentCategorySitemap,
    "free_content_subcategories": FreeContentSubCategorySitemap,
}

# --- Core App URLs ---
core_urlpatterns = [
    path('update-navbar-indicators/', core_views.update_navbar_indicators, name='update_navbar_indicators'),
    path('legal/aviso-legal/', core_views.LegalNoticeView.as_view(), name='legal_notice'),
    path('legal/privacidad/', core_views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('legal/cookies/', core_views.CookiesPolicyView.as_view(), name='cookies_policy'),
]

urlpatterns = [
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("service-worker.js", ServiceWorkerView.as_view(), name="service_worker"),
    path("admin/orchestrator/", include("orchestrator.admin_urls")),
    path("admin/assessment/", include("assessment.admin_urls", namespace="assessment_admin")),
    path("admin/contents/", include("contents.admin_urls", namespace="contents_admin")),
    path("admin/", admin.site.urls),
    path("", user_views.home_view, name="home"),
    path("robots.txt", user_views.robots_txt, name="robots_txt"),
    
    # --- START: Refactored Authentication URLs ---
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(template_name="users/logged_out.html"),
        name="logout",
    ),
    path(
        "accounts/password/change/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password_change_form.html",
            success_url=reverse_lazy("password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "accounts/password/change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "accounts/password/reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="users/password_reset_email.html",
            subject_template_name="users/password_reset_subject.txt",
            success_url=reverse_lazy("password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "accounts/password/reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        user_views.CustomPasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # --- END: Refactored Authentication URLs ---

    path("accounts/", include("users.urls", namespace="users")),
    path("announcements/", include("announcements.urls", namespace="announcements")),
    path("contents/", include("contents.urls", namespace="contents")),
    path("academic_structure/", include("academic_structure.urls", namespace="academic_structure")),
    path(
        "automation/",
        include("content_automation.urls", namespace="content_automation"),
    ),
    path("chat/", include("chat.urls", namespace="chat")),
    path("academic-chat/", include("academic_chat.urls", namespace="academic_chat")),
    path(
        "study-room/",
        include((study_room_urls_module.urlpatterns, "study_room"), namespace="study_room"),
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps_dict},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("portfolio/", include("portfolio.urls", namespace="portfolio")),
    path("messaging/", include("messaging.urls", namespace="messaging")),
    path("search/", include("search.urls", namespace="search")),
    path(
        "academic-directory/",
        include("academic_directory.urls", namespace="academic_directory"),
    ),
    path("feedback/", include("feedback.urls", namespace="feedback")),
    path("assessment/", include("assessment.urls", namespace="assessment")),
    path("push-tester/", include("push_tester.urls", namespace="push_tester")),
    path("universia/", include("universia.urls", namespace="universia")),
    path("schedule/", include("schedule.urls", namespace="schedule")),    
    path("traducciones/", include("translation_room.urls", namespace="translation_room")),    
    # --- Core App URL dispatcher ---
    path("core/", include((core_urlpatterns, "core"), namespace="core")),
    
    # --- Prototype Apps ---
    path("prototype/", include("favorites_prototype.urls", namespace="favorites_prototype")),
    
    path(
        "previews-seo/",
        serve,
        {
            "document_root": settings.PUBLIC_PREVIEWS_STATIC_DIR,
            "path": "index.html",
        },
        name="public_seo_previews_index",
    ),
    re_path(
        r"^previews-seo/(?P<path>.*)$",
        serve,
        {
            "document_root": settings.PUBLIC_PREVIEWS_STATIC_DIR,
            "show_indexes": False,
        },
        name="public_seo_previews_serve",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.media_url, document_root=settings.MEDIA_ROOT)
