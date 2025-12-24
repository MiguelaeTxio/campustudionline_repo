#!/bin/bash
# Servicio Primario: Celery Beat + Worker High Priority
PROJECT_DIR="/home/MiguelAeTxio/PROJECTS/CampuStudiOnline"
VENV_PYTHON="/home/MiguelAeTxio/.virtualenvs/campus_pa_env_py3.10/bin/python"

cd "$PROJECT_DIR" || { echo "CRITICAL: Directorio no encontrado"; exit 1; }

echo "--- Iniciando Servicio Primario (Beat + High Priority) ---"

# 1. Lanzar Worker High Priority en Background (&)
# Se encarga de: Chat, Emails urgentes, Notificaciones Push
"$VENV_PYTHON" -m dotenv run "$VENV_PYTHON" -m celery -A core worker \
    -Q high_priority \
    --hostname=worker_pri@%h \
    --loglevel=info \
    --concurrency=1 &

PID_WORKER=$!
echo ">> Worker High Priority iniciado (PID: $PID_WORKER)"

# 2. Lanzar Beat en Foreground
# Se encarga de: Cron jobs, Recordatorios de Agenda
echo ">> Iniciando Celery Beat..."
"$VENV_PYTHON" -m dotenv run "$VENV_PYTHON" -m celery -A core beat \
    --loglevel=info \
    --scheduler django_celery_beat.schedulers:DatabaseScheduler
