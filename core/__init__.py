# Developer Note: The users app is named 'users', but for historical reasons,
# some legacy parts might still reference a 'usuarios' namespace. This should be refactored.

# This ensures the Celery app is loaded when Django starts.
from .celery import app as celery_app

__all__ = ("celery_app",)
