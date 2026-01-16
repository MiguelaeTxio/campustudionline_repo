#!/bin/bash
PROJECT_DIR="/home/MiguelAeTxio/PROJECTS/CampuStudiOnline"
VENV_BIN="/home/MiguelAeTxio/.virtualenvs/campus_pa_env_py3.10/bin"

cd "$PROJECT_DIR" || { echo "CRITICAL: Directorio no encontrado"; exit 1; }

# Logging básico de intentos de arranque
echo "[$(date)] Iniciando Servicio Heavy (Versión Reparada)..." >> worker_heavy_debug.log

# Lanzar Worker usando rutas absolutas y SIN hostname fijo para evitar bloqueos por crash previo
exec "$VENV_BIN/python" -m dotenv run "$VENV_BIN/celery" -A core worker \
    -Q default,content_automation \
    --loglevel=info \
    --concurrency=1
