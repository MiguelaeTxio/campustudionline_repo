# /home/MiguelAeTxio/CampuStudiOnline/core/celery.py
import os
from celery import Celery
from dotenv import load_dotenv

# --- START OF ENVIRONMENT LOADING ---
# Build the absolute path to the .env file located in the project root.
# os.path.dirname(__file__) -> /home/MiguelAeTxio/CampuStudiOnline/core
# os.path.dirname(...) -> /home/MiguelAeTxio/CampuStudiOnline
# os.path.join(..., '.env') -> /home/MiguelAeTxio/CampuStudiOnline/.env
dotenv_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"
)

# If the .env file exists at that path, load it.
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
# --- END OF ENVIRONMENT LOADING ---

# Set the default Django settings module for the 'celery' program.
# 'core.settings' points to our project's /core/settings.py file.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Create the main Celery application instance.
# The first argument 'core' is the name of our main project.
app = Celery("core")

# Load configuration from Django's settings.
# The 'CELERY' namespace means that Celery will look for all its
# configuration variables in settings.py that start with "CELERY_", e.g., CELERY_BROKER_URL.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover task modules (tasks.py) from all apps listed in INSTALLED_APPS.
app.autodiscover_tasks()
