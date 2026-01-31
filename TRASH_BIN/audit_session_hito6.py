import os
import re
import json
from django.conf import settings
from assessment.models import Assessment

def audit_assessment_297():
    print("\n=== 1. AUDITORÍA EVALUACIÓN #297 ===")
    try:
        if not Assessment.objects.filter(id=297).exists():
            print("❌ La evaluación #297 NO EXISTE.")
            return

        a = Assessment.objects.get(id=297)
        print(f"Status: {a.status}")
        print(f"Arquetipo: {a.archetype}")
        print(f"Itinerario: {a.language_itinerary}")
        print(f"Total Preguntas: {a.questions.count()}")

        print("\n--- ANÁLISIS DE LOGS DE EVENTOS ---")
        if not a.event_log:
            print("⚠️ EL EVENT LOG ESTÁ VACÍO.")
        else:
            print(f"Total entradas: {len(a.event_log)}")
            for i, log in enumerate(a.event_log[:5]):
                ts = log.get('timestamp', 'No TS')
                lvl = log.get('level', 'INFO')
                msg = log.get('message', '')
                print(f"[{i}] {ts} | {lvl} | {msg}")

        print("\n--- ANÁLISIS LINGÜÍSTICO (Bilingüismo) ---")
        # Rango Unicode CJK: \u4e00-\u9fff
        has_chinese = lambda s: bool(re.search(r'[\u4e00-\u9fff]', s))
        # Detección laxa de español (tildes o palabras clave de instrucción)
        has_spanish = lambda s: bool(re.search(r'[áéíóúñÁÉÍÓÚÑ]', s)) or "lee" in s.lower() or "traduce" in s.lower() or "escucha" in s.lower()

        questions = a.questions.all().order_by('id')
        if not questions.exists():
             print("⚠️ No hay preguntas generadas.")
        
        for q in questions:
            txt = q.question_text
            es = has_spanish(txt)
            zh = has_chinese(txt)
            status = "✅ OK (Bilingüe)" if (es and zh) else ("⚠️ FALTA CHINO" if es else ("⚠️ FALTA ESPAÑOL" if zh else "❓ DESCONOCIDO"))
            print(f"Q{q.id} [{q.section_label}]: {status}")
            print(f"   Snippet: {txt[:60]}...")

    except Exception as e:
        print(f"❌ Error crítico auditando #297: {e}")

def audit_recovery_files():
    print("\n=== 2. VERIFICACIÓN DE ARCHIVOS DE RESPALDO (CLEANUP) ===")
    recovery_dir = os.path.join(settings.BASE_DIR, "assessment_recovery")
    if not os.path.exists(recovery_dir):
        print(f"✅ El directorio {recovery_dir} no existe (Limpio).")
        return

    files = os.listdir(recovery_dir)
    json_files = [f for f in files if f.endswith('.json')]
    
    if not json_files:
        print(f"✅ El directorio existe pero no contiene JSONs ({len(files)} archivos totales).")
    else:
        print(f"⚠️ SE ENCONTRARON {len(json_files)} ARCHIVOS JSON RESIDUALES:")
        for f in json_files:
            print(f"   - {f}")

if __name__ == "__main__":
    audit_assessment_297()
    audit_recovery_files()
