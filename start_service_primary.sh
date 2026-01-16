#!/bin/bash
# Servicio Primario BLINDADO: Beat + Worker HP
# Incluye gestión de zombies para evitar duplicidad de workers al reiniciar.

PROJECT_DIR="/home/MiguelAeTxio/PROJECTS/CampuStudiOnline"
VENV_BIN="/home/MiguelAeTxio/.virtualenvs/campus_pa_env_py3.10/bin"

cd "$PROJECT_DIR" || { echo "ERROR: Directorio no encontrado"; exit 1; }

# Función para matar procesos hijos al reiniciar el bucle
cleanup_workers() {
    # Si existe un PID guardado del worker HP anterior, lo matamos
    if [ ! -z "$HP_PID" ]; then
        echo ">> [Limpieza] Deteniendo Worker HP anterior (PID: $HP_PID)..."
        kill -9 $HP_PID 2>/dev/null
    fi
    rm -f celerybeat.pid beat.pid
}

# Trap para asegurar limpieza si se mata el script manualmente
trap "cleanup_workers; exit" INT TERM EXIT

while true; do
    cleanup_workers
    echo "--- [$(date)] Iniciando Ciclo de Servicio Primario ---"

    # 1. Lanzar Worker High Priority en background (Con límite de memoria)
    "$VENV_BIN/python" -m dotenv run "$VENV_BIN/celery" -A core worker \
        -Q high_priority \
        --loglevel=info \
        --concurrency=1 \
        --max-memory-per-child=250000 \
        --hostname=hp_worker@%h 2>&1 &
    
    HP_PID=$!
    echo ">> Worker High Priority iniciado en background (PID: $HP_PID)"

    sleep 5

    # 2. Lanzar Celery Beat en primer plano (Proceso Bloqueante Principal)
    echo ">> Iniciando Celery Beat (Scheduler)..."
    "$VENV_BIN/python" -m dotenv run "$VENV_BIN/celery" -A core beat \
        --loglevel=info \
        --scheduler django_celery_beat.schedulers:DatabaseScheduler
    
    EXIT_CODE=$?
    echo "!!! CRITICAL: Celery Beat se ha detenido (Código: $EXIT_CODE)."
    echo "!!! Reiniciando ciclo completo en 10 segundos..."
    
    sleep 10
done
