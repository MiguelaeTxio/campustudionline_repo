import sys
import os

sys.path.append('/home/MiguelAeTxio/PROJECTS/CampuStudiOnline')
try:
    from universia.ai_config import UNIVERSIA_AGENDA_SKILL
    print("--- TESTING STRING FORMAT ---")
    try:
        # Intentamos lo mismo que hace services.py
        result = UNIVERSIA_AGENDA_SKILL.format(current_time="TEST_TIME")
        print("[SUCCESS] El string se formatea correctamente.")
    except Exception as e:
        print(f"[CRASH] FALLÓ EL FORMATEO: {type(e).__name__}: {e}")
        print("Causa probable: Las llaves del JSON no están escapadas como {{ y }}.")
except ImportError:
    print("[FAIL] No se pudo importar ai_config.")
except Exception as e:
    print(f"[FAIL] Error inesperado: {e}")
