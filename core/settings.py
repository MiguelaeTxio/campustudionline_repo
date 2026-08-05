# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/core/settings.py
from pathlib import Path
import os
import socket
import logging
from datetime import timedelta
from celery.schedules import crontab
from kombu import Queue

logger_settings = logging.getLogger(__name__ + ".settings_init")

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Secrets and Environment Configuration Loading ---
DJANGO_SECRET_KEY_FROM_ENV = os.environ.get("DJANGO_SECRET_KEY")
if not DJANGO_SECRET_KEY_FROM_ENV:
    raise ValueError(
        "CRITICAL: No se encontró la variable de entorno DJANGO_SECRET_KEY"
    )
SECRET_KEY = DJANGO_SECRET_KEY_FROM_ENV

DJANGO_DEBUG_STR = os.environ.get("DJANGO_DEBUG", "False")
DEBUG = DJANGO_DEBUG_STR.lower() in ("true", "1", "t")

HOSTNAME = ""
try:
    HOSTNAME = socket.gethostname()
except Exception:
    logger_settings.warning("Could not determine hostname via socket.gethostname().")
    pass

if HOSTNAME.endswith(".pythonanywhere.com"):
    logger_settings.info(
        f"PythonAnywhere environment detected (hostname: {HOSTNAME}). Forcing DEBUG=False for application logic."
    )
    DEBUG = False
elif "PYTHONANYWHERE_DOMAIN" in os.environ:
    logger_settings.info(
        "PythonAnywhere environment detected (PYTHONANYWHERE_DOMAIN env var). Forcing DEBUG=False for application logic."
    )
    DEBUG = False

DJANGO_ALLOWED_HOSTS_STR = os.environ.get("DJANGO_ALLOWED_HOSTS")
if DJANGO_ALLOWED_HOSTS_STR:
    ALLOWED_HOSTS = [host.strip() for host in DJANGO_ALLOWED_HOSTS_STR.split(",")]
else:
    ALLOWED_HOSTS = [
        "MiguelAeTxio.pythonanywhere.com",
        "www.MiguelAeTxio.pythonanywhere.com",
        "campustudionline.com",
        "www.campustudionline.com",
    ]
    logger_settings.warning(
        f"DJANGO_ALLOWED_HOSTS not set in environment. Using default list: {ALLOWED_HOSTS}"
    )

if DEBUG:
    ALLOWED_HOSTS.extend(["127.0.0.1", "localhost"])

SITE_URL = os.environ.get("SITE_URL", "https://www.campustudionline.com")

# --- Database Configuration ---
DB_NAME_FROM_ENV = os.environ.get("DB_NAME_PROD")
DB_USER_FROM_ENV = os.environ.get("DB_USER_PROD")
DB_PASSWORD_FROM_ENV = os.environ.get("DB_PASSWORD_PROD")
DB_HOST_FROM_ENV = os.environ.get("DB_HOST_PROD")
DB_PORT_FROM_ENV = os.environ.get("DB_PORT_PROD")

if not DEBUG:
    if not all(
        [DB_NAME_FROM_ENV, DB_USER_FROM_ENV, DB_PASSWORD_FROM_ENV, DB_HOST_FROM_ENV]
    ):
        raise ValueError(
            "CRITICAL: Una o más variables de entorno para la base de datos "
            "(DB_NAME_PROD, DB_USER_PROD, DB_PASSWORD_PROD, DB_HOST_PROD) no están definidas."
        )

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DB_NAME_FROM_ENV,
        "USER": DB_USER_FROM_ENV,
        "PASSWORD": DB_PASSWORD_FROM_ENV,
        "HOST": DB_HOST_FROM_ENV,
        "PORT": DB_PORT_FROM_ENV or "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES', SESSION time_zone = '+00:00'",
            "charset": "utf8mb4",
        },
    }
}

# --- START: EMAIL MIGRATION TO MAILERSEND ---
MAILERSEND_API_TOKEN_FROM_ENV = os.environ.get("MAILERSEND_API_TOKEN")
if not MAILERSEND_API_TOKEN_FROM_ENV and not DEBUG:
    logger_settings.warning(
        "MAILERSEND_API_TOKEN no configurada en producción. El envío de emails usará el backend de consola."
    )

ANYMAIL = {
    "MAILERSEND_API_TOKEN": (
        MAILERSEND_API_TOKEN_FROM_ENV
        if MAILERSEND_API_TOKEN_FROM_ENV
        else "dummy_key_for_dev"
    ),
}
EMAIL_BACKEND = (
    "anymail.backends.mailersend.EmailBackend"
    if MAILERSEND_API_TOKEN_FROM_ENV and not DEBUG
    else "django.core.mail.backends.console.EmailBackend"
)
DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "noreply@campustudionline.com"
)
# --- END: EMAIL MIGRATION TO MAILERSEND ---

# --- Celery Configuration ---
EFFECTIVE_REDIS_URL = os.environ.get("REDIS_URL")

if not EFFECTIVE_REDIS_URL:
    if not DEBUG:
        raise ValueError(
            "CRITICAL: La variable de entorno REDIS_URL no está configurada para Celery en producción."
        )
    else:
        logger_settings.warning(
            "WARNING: REDIS_URL not set for Celery. Defaulting to 'redis://localhost:6379/0' for LOCAL DEVELOPMENT."
        )
        EFFECTIVE_REDIS_URL = "redis://localhost:6379/0"

CELERY_BROKER_URL = EFFECTIVE_REDIS_URL
CELERY_RESULT_BACKEND = EFFECTIVE_REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Europe/Madrid"
CELERY_WORKER_CONCURRENCY = 1
# [OPTIMIZATION] Force a single shared connection pool for Redis to avoid exceeding plan limits.
CELERY_BROKER_POOL_LIMIT = 4
CELERY_REDIS_MAX_CONNECTIONS = 20
CELERY_RESULT_EXPIRES = 3600

# --- Celery Priority Queues Configuration (V2 - Arquitectura de Prioridades) ---
CELERY_TASK_QUEUES = (
    Queue('default', routing_key='task.default'),
    Queue('high_priority', routing_key='task.high_priority'),
    Queue('content_automation', routing_key='task.content_automation'),
)
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'task.default'

CELERY_TASK_ROUTES = {
    'orchestrator.tasks.generate_exam_task': {'queue': 'high_priority'},
    # [PASO 5 H06 - S029] Refinamiento asincrono de items PENDING_AI_ANALYSIS.
    # Misma cola que generate_exam_task: es IA casi en tiempo real para el
    # alumno, no debe esperar detras de la generacion masiva de contenido
    # del worker Pesado (cola 'default').
    'orchestrator.tasks.refine_pending_ai_items_task': {'queue': 'high_priority'},
    'orchestrator.tasks.generate_full_course_task': {'queue': 'content_automation'},
    'orchestrator.tasks.global_orchestrator_task': {'queue': 'default'},
}

# --- reCAPTCHA Configuration ---
RECAPTCHA_PUBLIC_KEY_FROM_ENV = os.environ.get("RECAPTCHA_PUBLIC_KEY_PROD")
RECAPTCHA_PRIVATE_KEY_FROM_ENV = os.environ.get("RECAPTCHA_PRIVATE_KEY_PROD")
RECAPTCHA_PUBLIC_KEY = RECAPTCHA_PUBLIC_KEY_FROM_ENV
RECAPTCHA_PRIVATE_KEY = RECAPTCHA_PRIVATE_KEY_FROM_ENV
NOCAPTCHA = False


# --- INSTALLED_APPS (CORRECTED ORDER) ---
# A logical and robust order is followed:
# 1. Native Django apps: To establish the framework's base.
# 2. Third-party apps: To integrate with the Django base.
# 3. Project apps: So they can safely override templates and configurations.
INSTALLED_APPS = [
    # 1. Native Django Applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    # 2. Third-Party Applications
    "django_recaptcha",
    "markdownify.apps.MarkdownifyConfig",
    "anymail",
    "webpush",
    "django_user_agents",
    "treebeard",
    "django_celery_beat",
    "crispy_forms",
    "crispy_bootstrap5",
    # 3. Project Applications
    "core",
    "orchestrator.apps.OrchestratorConfig",
    "users.apps.UsersConfig",
    "academic_structure.apps.AcademicStructureConfig",
    "content_automation.apps.ContentAutomationConfig",
    "announcements.apps.AnnouncementsConfig",
    "contents.apps.ContentsConfig",
    "global_settings.apps.GlobalSettingsConfig",
    "academic_chat",
    "chat.apps.ChatConfig",
    "portfolio.apps.PortfolioConfig",
    "messaging.apps.MessagingConfig",
    "search.apps.SearchConfig",
    "academic_directory.apps.AcademicDirectoryConfig",
    "push_tester.apps.PushTesterConfig",
    "favorites_prototype.apps.FavoritesPrototypeConfig",    "feedback.apps.FeedbackConfig",
    "universia.apps.UniversiaConfig",
    "schedule.apps.ScheduleConfig",
    "translation_room.apps.TranslationRoomConfig",
    "media_library.apps.MediaLibraryConfig",
    "assessment_v2.apps.AssessmentV2Config",
]

AUTH_USER_MODEL = "users.CustomUser"

# --- MIDDLEWARE ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django_user_agents.middleware.UserAgentMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "users.middleware.SecuritySetupMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.maintenance_middleware.MaintenanceModeMiddleware",
    "core.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.global_context",
                "assessment_v2.context_processors.assessment_badges",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# --- Internationalization ---
LANGUAGE_CODE = "es-es"
TIME_ZONE = "Europe/Madrid"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

# --- Static and Media Files ---
STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles_production")
PUBLIC_PREVIEWS_STATIC_DIR = BASE_DIR / "public_seo_previews"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

if DEBUG:
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
else:
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
        },
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

CSRF_TRUSTED_ORIGINS_STR = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS")
if CSRF_TRUSTED_ORIGINS_STR:
    CSRF_TRUSTED_ORIGINS = [
        origin.strip() for origin in CSRF_TRUSTED_ORIGINS_STR.split(",")
    ]
else:
    CSRF_TRUSTED_ORIGINS = [
        "https://www.campustudionline.com",
        "https://MiguelAeTxio.pythonanywhere.com",
    ]

if not DEBUG:
    SESSION_COOKIE_DOMAIN = ".campustudionline.com"
    CSRF_COOKIE_DOMAIN = ".campustudionline.com"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# --- Custom App Settings ---
MAINTENANCE_MODE_ALLOWED_IPS_STR = os.environ.get("MAINTENANCE_MODE_ALLOWED_IPS", "")
MAINTENANCE_MODE_ALLOWED_IPS = [
    ip.strip() for ip in MAINTENANCE_MODE_ALLOWED_IPS_STR.split(",") if ip.strip()
]
ADMIN_URL_SEGMENT = os.environ.get("DJANGO_ADMIN_URL_SEGMENT", "admin/")
ADMIN_URL = (
    f"{ADMIN_URL_SEGMENT}/"
    if not ADMIN_URL_SEGMENT.endswith("/")
    else ADMIN_URL_SEGMENT
)
if DEBUG:
    if "127.0.0.1" not in MAINTENANCE_MODE_ALLOWED_IPS:
        MAINTENANCE_MODE_ALLOWED_IPS.append("127.0.0.1")
    if "::1" not in MAINTENANCE_MODE_ALLOWED_IPS:
        MAINTENANCE_MODE_ALLOWED_IPS.append("::1")

DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024


def clean_pem_key(pem_key_string):
    if not pem_key_string:
        return None
    lines = pem_key_string.strip().split("\n")
    base64_lines = [line for line in lines if not line.strip().startswith("-----")]
    return "".join(base64_lines)


raw_public_key = os.getenv("VAPID_PUBLIC_KEY")
raw_private_key = os.getenv("VAPID_PRIVATE_KEY")
VAPID_PUBLIC_KEY = clean_pem_key(raw_public_key)
VAPID_PRIVATE_KEY = clean_pem_key(raw_private_key)
VAPID_ADMIN_EMAIL = os.getenv("VAPID_ADMIN_EMAIL")

if not all([VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_ADMIN_EMAIL]):
    logger_settings.warning(
        "Una o más claves VAPID no están configuradas correctamente en el entorno. Las notificaciones push no funcionarán."
    )

# --- AI Configuration ---
GEMINI_DAILY_REQUESTS_PER_USER = os.environ.get("GEMINI_DAILY_REQUESTS_PER_USER", "3")
if not os.environ.get("GEMINI_DAILY_REQUESTS_PER_USER"):
    logger_settings.warning(
        f"GEMINI_DAILY_REQUESTS_PER_USER no configurada. Usando valor por defecto: {GEMINI_DAILY_REQUESTS_PER_USER}"
    )

GEMINI_GLOBAL_PPM = os.environ.get("GEMINI_GLOBAL_PPM", "50")
if not os.environ.get("GEMINI_GLOBAL_PPM"):
    logger_settings.warning(
        f"GEMINI_GLOBAL_PPM no configurada. Usando valor por defecto: {GEMINI_GLOBAL_PPM}"
    )

# --- Meta (Facebook/Instagram) Ads Configuration ---
META_PIXEL_ID = os.environ.get("META_PIXEL_ID")
META_CONVERSIONS_API_TOKEN = os.environ.get("META_CONVERSIONS_API_TOKEN")

if not META_PIXEL_ID and not DEBUG:
    logger_settings.warning("META_PIXEL_ID no configurado en producción. El tracking de Meta Ads estará deshabilitado.")


SITE_ID = 1
SITE_NAME = "CampuStudiOnline"

# ==============================================================================
# ASSESSMENT CONFIGURATION (REMOVED HITO 6)
# ==============================================================================

# Task scheduler for Celery Beat
CELERY_BEAT_SCHEDULE = {
    "check-scheduled-reminders-hourly": {
        "task": "schedule.tasks.check_scheduled_reminders",
        "schedule": crontab(minute=0), # Cada hora en punto
    },
    'run-global-orchestrator-every-5-minutes': {
        'task': 'orchestrator.tasks.global_orchestrator_task',
        'schedule': crontab(minute='*/5'),
        'options': {'queue': 'default'},
    },
}
# ==============================================================================

# --- Forensic Logging Configuration (ROBUST V2) ---
# SilentStreamHandler: subclass of StreamHandler that suppresses OSError
# exceptions caused by writing to a closed stderr/stdout descriptor.
# This occurs on PythonAnywhere when the WSGI worker process is recycled
# and the console stream becomes invalid. Without this guard, the logging
# system catches the OSError and re-logs it via the root logger, producing
# the repetitive 'OSError: write error' entries observed in django.log.
# SilentStreamHandler: subclase de StreamHandler que suprime las excepciones
# OSError causadas por escribir en un descriptor stderr/stdout cerrado.
# Ocurre en PythonAnywhere cuando el proceso worker WSGI se recicla y el
# stream de consola queda inválido. Sin esta guardia, el sistema de logging
# captura el OSError y lo vuelve a loguear vía el logger raíz, produciendo
# las entradas repetitivas 'OSError: write error' observadas en django.log.
import logging as _logging_module
import sys as _sys_module

class _SilentStreamHandler(_logging_module.StreamHandler):
    def emit(self, record):
        try:
            super().emit(record)
        except OSError:
            pass

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - %(levelname)s - [%(name)s:%(lineno)d] - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "core.settings._SilentStreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "django.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "error.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 2,
            "formatter": "verbose",
        },
    },
    "loggers": {
        # El logger raíz captura los logs de NUESTRAS aplicaciones.
        "": {
            "handlers": ["console", "file", "error_file"],
            "level": "DEBUG",
        },
        # El logger 'django' captura los logs del framework.
        "django": {
            "handlers": ["console", "file", "error_file"],
            "level": "INFO",
            "propagate": False,
        },
        # Logger específico para errores del servidor (5xx). Crucial para producción.
        "django.request": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": True,
        },
        # Silenciamos el logger de base de datos por defecto para evitar ruido.
        # Cambiar a 'DEBUG' para depurar consultas SQL específicas.
        "django.db.backends": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "push_debugger": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


WSGI_APPLICATION = "core.wsgi.application"

logger_settings.info(f"Settings cargados para {SITE_NAME}. DEBUG={DEBUG}.")

PASSWORD_RESET_TIMEOUT = 600

# --- Compatibility Aliases ---
# BASE_URL is required by orchestrator tasks for notifications
BASE_URL = SITE_URL

# --- Crispy Forms Configuration ---
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# --- Markdownify Configuration / Configuracion de Markdownify ---
# Named configuration used ONLY by the assessment report, to render the
# AI-written feedback (justification, qualitative_summary), which arrives
# as Markdown: fenced code blocks, inline code and numbered lists.
#
# There is deliberately NO "default" key. The announcements board calls
# the filter with no argument, which looks up MARKDOWNIFY["default"];
# that raises KeyError, the filter catches it and falls back to an empty
# settings dict -- byte-identical to today's behaviour, when the setting
# does not exist at all. Adding a "default" key here would silently
# change how announcements render.
#
# bleach sanitises the output, which matters because this text is
# written by a language model. The default bleach whitelist lacks p, br
# and pre, which is why they are listed explicitly.
# ---
# Configuracion con nombre, usada UNICAMENTE por el informe de
# evaluacion, para renderizar el feedback redactado por la IA
# (justification, qualitative_summary), que llega en Markdown: vallas de
# codigo, codigo en linea y listas numeradas.
#
# NO hay clave "default" a proposito. El tablon de anuncios invoca el
# filtro sin argumento, que busca MARKDOWNIFY["default"]; eso lanza
# KeyError, el filtro lo captura y cae en un dict de ajustes vacio --
# identico al comportamiento de hoy, cuando el ajuste no existe. Anadir
# una clave "default" aqui cambiaria en silencio como se ven los
# anuncios.
#
# bleach sanea la salida, lo que importa porque ese texto lo redacta un
# modelo de lenguaje. La lista blanca por defecto de bleach carece de p,
# br y pre, de ahi que se declaren de forma explicita.
MARKDOWNIFY = {
    "assessment": {
        "WHITELIST_TAGS": [
            "p",
            "br",
            "pre",
            "code",
            "ul",
            "ol",
            "li",
            "strong",
            "em",
            "blockquote",
        ],
        "MARKDOWN_EXTENSIONS": [
            "fenced_code",
            "nl2br",
        ],
    },
}
