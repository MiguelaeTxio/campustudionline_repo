#!/bin/bash
# Wrapper Inmortal 2026 (Anti-Crash Loop)
# Mantiene el worker vivo aunque el código Python falle.

PROJECT_DIR="/home/MiguelAeTxio/PROJECTS/CampuStudiOnline"
VENV_ACTIVATE="/home/MiguelAeTxio/.virtualenvs/campus_pa_env_py3.10/bin/activate"

cd "$PROJECT_DIR"
source "$VENV_ACTIVATE"

while true; do
    echo "--- [$(date)] Iniciando Celery Worker ---"
    
    # Ejecutamos Celery con protección de Memoria (250MB)
    # Si falla, el script NO termina, el bucle 'while' lo captura.
    python -m dotenv run celery -A core worker -l info --concurrency=1 --max-memory-per-child=250000
    
    EXIT_CODE=$?
    echo "!!! Celery se detuvo (Código: $EXIT_CODE). Esperando 10s para evitar castigo de PA..."
    
    # Pausa obligatoria para evitar el Exponential Backoff
    sleep 10
done
