#!/bin/bash
# Servicio Pesado BLINDADO: IA + Generación
# Bucle infinito resistente a caídas y OOM.

PROJECT_DIR="/home/MiguelAeTxio/PROJECTS/CampuStudiOnline"
VENV_BIN="/home/MiguelAeTxio/.virtualenvs/campus_pa_env_py3.10/bin"

cd "$PROJECT_DIR" || { echo "CRITICAL: Directorio no encontrado"; exit 1; }

echo "[$(date)] Iniciando Servicio Heavy (Wrapper Inmortal)..." >> worker_heavy.log

while true; do
    echo "--- Lanzando Celery Worker (Heavy) ---"
    
    # Worker para colas pesadas con protección de memoria
    "$VENV_BIN/python" -m dotenv run "$VENV_BIN/celery" -A core worker \
        -Q default,content_automation \
        --loglevel=info \
        --concurrency=1 \
        --max-memory-per-child=250000 \
        --hostname=heavy_worker@%h
        
    EXIT_CODE=$?
    echo "!!! ALERTA: Heavy Worker se detuvo (Código: $EXIT_CODE)."
    echo "!!! Pausando 10 segundos para evitar penalización..."
    sleep 10
done
