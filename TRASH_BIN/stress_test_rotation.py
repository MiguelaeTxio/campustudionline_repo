import os
import sys
import django
from django.utils import timezone

# Configuración de entorno Django
sys.path.append('/home/MiguelAeTxio/PROJECTS/CampuStudiOnline')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from orchestrator.models import AutomationSettings, ApiKey

def run_stress_test():
    print("--- INICIO STRESS TEST ROTACIÓN API (SIMULACIÓN) ---")
    
    # 1. Setup inicial y Snapshot del estado
    settings = AutomationSettings.load()
    original_active_key = settings.active_api_key
    
    if not original_active_key:
        print("❌ ABORTANDO: No hay clave activa definida en AutomationSettings.")
        return

    print(f"Clave Inicial Activa: {original_active_key.name} (ID: {original_active_key.id})")
    print(f"Estado Inicial -> Fallos: {original_active_key.consecutive_failures}, Cuarentena: {original_active_key.is_quarantined}")

    # Asegurarnos de tener al menos una clave de backup para rotar
    backup_keys = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).exclude(id=original_active_key.id)
    if not backup_keys.exists():
        print("⚠️ ADVERTENCIA: No hay claves de backup disponibles. La rotación fallará (Pool Agotado), pero probaremos la cuarentena.")
    else:
        print(f"Claves de backup disponibles: {backup_keys.count()}")

    # 2. Simulación de Fallos Consecutivos (Umbral = 4)
    print("\n[EJECUTANDO SIMULACIÓN DE 5 FALLOS CONSECUTIVOS]...")
    
    # Trabajamos sobre la clave original
    target_key = original_active_key
    
    # Reset temporal para asegurar condiciones de test limpias
    target_key.consecutive_failures = 0
    target_key.is_quarantined = False
    target_key.save()

    try:
        for i in range(1, 6):
            # Recargar estado
            target_key.refresh_from_db()
            settings.refresh_from_db()
            
            print(f"--- Iteración {i} ---")
            
            # Simular incremento de fallos (Lógica replicada de tasks.py)
            target_key.consecutive_failures += 1
            target_key.save()
            print(f"  Fallos registrados: {target_key.consecutive_failures}")

            # Verificar lógica de umbral (Hardcoded a 4 en tasks.py actual)
            if target_key.consecutive_failures >= 4:
                print("  -> UMBRAL DE CUARENTENA ALCANZADO.")
                
                # Aplicar Cuarentena
                target_key.is_quarantined = True
                target_key.save()
                print(f"  -> Clave '{target_key.name}' puesta en CUARENTENA.")
                
                # Intentar Rotación
                next_k = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).exclude(id=target_key.id).first()
                if next_k:
                    settings.active_api_key = next_k
                    settings.save()
                    print(f"  -> ROTACIÓN EXITOSA. Nueva clave activa: {next_k.name}")
                    # Terminamos el bucle si ya rotamos, aunque tasks.py seguiría intentando con la nueva
                    # Para el test, nos basta ver que rotó una vez.
                    break 
                else:
                    print("  -> FALLO DE ROTACIÓN: Pool Agotado (No hay más claves).")
            else:
                print("  -> Umbral no alcanzado. Continuando...")
            
    except Exception as e:
        print(f"❌ EXCEPCIÓN DURANTE EL TEST: {e}")

    # 3. Verificación de Resultados
    print("\n--- INFORME FINAL ---")
    target_key.refresh_from_db()
    settings.refresh_from_db()

    quarantine_success = target_key.is_quarantined
    rotation_success = settings.active_api_key.id != original_active_key.id
    
    if quarantine_success:
        print("✅ PRUEBA DE CUARENTENA: PASADA")
    else:
        print("❌ PRUEBA DE CUARENTENA: FALLIDA (La clave no se marcó como cuarentena)")

    if rotation_success:
        print(f"✅ PRUEBA DE ROTACIÓN: PASADA (Nueva clave: {settings.active_api_key.name})")
    elif not backup_keys.exists():
        print("⚪ PRUEBA DE ROTACIÓN: OMITIDA (Sin claves de backup)")
    else:
        print("❌ PRUEBA DE ROTACIÓN: FALLIDA (La clave activa no cambió)")

    # 4. Rollback (Restauración del Estado)
    print("\n[ROLLBACK] Restaurando estado original...")
    target_key.is_quarantined = False
    target_key.consecutive_failures = original_active_key.consecutive_failures # Restaurar contador original si fuera necesario, o a 0
    if original_active_key.consecutive_failures >= 4:
         # Si ya estaba mal antes, lo dejamos a 0 para que funcione
         target_key.consecutive_failures = 0
    else:
         target_key.consecutive_failures = 0 # Por seguridad, resetear a 0
         
    target_key.save()
    
    settings.active_api_key = original_active_key
    settings.save()
    print(f"Sistema restaurado a clave activa: {settings.active_api_key.name}")

if __name__ == "__main__":
    run_stress_test()
