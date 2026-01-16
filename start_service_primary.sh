#!/bin/bash
# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/start_service_primary.sh

PROJECT_DIR="/home/MiguelAeTxio/PROJECTS/CampuStudiOnline"
PYTHON_EXE="/home/MiguelAeTxio/.virtualenvs/campus_pa_env_py3.10/bin/python"
CELERY_EXE="/home/MiguelAeTxio/.virtualenvs/campus_pa_env_py3.10/bin/celery"

cd "$PROJECT_DIR" || { echo "ERROR: Directorio no encontrado"; exit 1; }

# Limpieza preventiva de archivos de bloqueo de Celery Beat
rm -f celerybeat.pid
rm -f beat.pid

echo "[$(date)] Iniciando Servicio Primario (Worker HP + Beat)..."

# 1. Lanzar Worker High Priority en background
"$PYTHON_EXE" -m dotenv run "$CELERY_EXE" -A core worker \
    -Q high_priority \
    --loglevel=info \
    --concurrency=1 2>&1 &

sleep 3

# 2. Lanzar Celery Beat reemplazando el proceso del shell (exec)
exec "$PYTHON_EXE" -m dotenv run "$CELERY_EXE" -A core beat \
    --loglevel=info \
    --scheduler django_celery_beat.schedulers:DatabaseScheduler 2>&1
