#!/bin/bash
# Servicio Pesado: Worker Default + Automation
PROJECT_DIR="/home/MiguelAeTxio/PROJECTS/CampuStudiOnline"
VENV_PYTHON="/home/MiguelAeTxio/.virtualenvs/campus_pa_env_py3.10/bin/python"

cd "$PROJECT_DIR" || { echo "CRITICAL: Directorio no encontrado"; exit 1; }

echo "--- Iniciando Servicio de Carga Pesada ---"

# Lanzar Worker General en Foreground
# Se encarga de: Generación IA, Evaluaciones, Tareas default
"$VENV_PYTHON" -m dotenv run "$VENV_PYTHON" -m celery -A core worker \
    -Q default,content_automation \
    --hostname=worker_hvy@%h \
    --loglevel=info \
    --concurrency=1
