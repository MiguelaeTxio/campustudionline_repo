import os
import sys
import django

# Configuración del entorno Django Standalone
sys.path.append('/home/MiguelAeTxio/PROJECTS/CampuStudiOnline')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import re
from django.conf import settings
from assessment.models import Assessment
from orchestrator.models import AutomationSettings, ApiKey

def audit_main():
    print("=== REPORTE DE AUDITORÍA HITO 6 (V2) ===")
    
    # 1. AUDITORÍA EVALUACIÓN #297
    print("\n[1] ANÁLISIS DE EVALUACIÓN #297")
    try:
        if not Assessment.objects.filter(id=297).exists():
             print("❌ La evaluación #297 NO EXISTE en la base de datos.")
        else:
            a = Assessment.objects.get(id=297)
            print(f"   > Estado: {a.status}")
            print(f"   > Arquetipo: {a.archetype}")
            print(f"   > Itinerario: {a.language_itinerary}")
            
            # Análisis de Logs de Eventos
            print(f"   > Event Log ({len(a.event_log)} entradas):")
            if not a.event_log:
                print("     ⚠️ EL LOG ESTÁ VACÍO (Fallo de persistencia confirmado si se generó).")
            else:
                for log in a.event_log[:5]:
                    ts = log.get('timestamp', 'No TS')
                    msg = log.get('message', '')
                    print(f"     - [{ts}] {msg}")

            # Análisis de Bilingüismo en Preguntas
            print(f"   > Preguntas Generadas ({a.questions.count()}):")
            questions = a.questions.all().order_by('id')
            for q in questions[:3]: # Muestra solo las primeras 3
                text = q.question_text
                # Detección simple de caracteres chinos
                has_chinese = bool(re.search(r'[\u4e00-\u9fff]', text))
                # Detección simple de español
                has_spanish = bool(re.search(r'[áéíóúñÁÉÍÓÚÑ]', text)) or "lee" in text.lower()
                
                status = "✅ BILINGÜE" if (has_chinese and has_spanish) else ("⚠️ FALTA ESPAÑOL" if has_chinese else ("⚠️ FALTA CHINO" if has_spanish else "❓ INCIERTO"))
                print(f"     Q{q.id} [{q.section_label}]: {status}")
                print(f"       Snippet: {text[:80]}...")

    except Exception as e:
        print(f"❌ Error leyendo evaluación #297: {e}")

    # 2. ESTADO DE CLAVES API (Stress Test Prep)
    print("\n[2] ESTADO DE CLAVES API (Orchestrator)")
    try:
        s = AutomationSettings.load()
        active = s.active_api_key.name if s.active_api_key else "NINGUNA"
        print(f"   > Clave Activa: {active}")
        
        keys = ApiKey.objects.all().order_by('id')
        print(f"   > Inventario de Claves ({keys.count()}):")
        for k in keys:
            status = "🔴 CUARENTENA" if k.is_quarantined else ("🟢 OK" if k.is_enabled else "⚪ DESHABILITADA")
            print(f"     - ID {k.id} [{k.name}]: {status} | Fallos Consecutivos: {k.consecutive_failures}")
            
    except Exception as e:
        print(f"❌ Error leyendo configuración de claves: {e}")

    # 3. VERIFICACIÓN DE LIMPIEZA
    print("\n[3] ARCHIVOS DE RECUPERACIÓN (JSON)")
    try:
        rec_dir = os.path.join(settings.BASE_DIR, 'assessment_recovery')
        if os.path.exists(rec_dir):
            files = [f for f in os.listdir(rec_dir) if f.endswith('.json')]
            if not files:
                print(f"   ✅ Directorio limpio ({rec_dir}).")
            else:
                print(f"   ⚠️ {len(files)} JSONs residuales encontrados:")
                for f in files: print(f"     - {f}")
        else:
            print(f"   ✅ Directorio no existe (Limpio).")
    except Exception as e:
        print(f"❌ Error verificando archivos: {e}")

    print("\n=== FIN DE REPORTE ===")

if __name__ == '__main__':
    audit_main()
