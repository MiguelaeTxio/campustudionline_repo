import os
import sys
import json
import re

# Setup Django Environment
sys.path.append('/home/MiguelAeTxio/PROJECTS/CampuStudiOnline')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django
django.setup()

from django.conf import settings
from django.utils import timezone
from orchestrator.models import ApiKey

print(">>> PASO 0: Inicio Entorno OK")

try:
    print(">>> PASO 1: Importando Configuraciones AI...")
    from universia.ai_config import UNIVERSIA_ACADEMIC_PROMPT, UNIVERSIA_NAVIGATION_PROMPT, UNIVERSIA_AGENDA_SKILL
    print("   [OK] Configuración importada.")
    print(f"   [DEBUG] Skill preview: {UNIVERSIA_AGENDA_SKILL[:50]}...")
except Exception as e:
    print(f"   [FAIL] Import ai_config: {e}")
    sys.exit(1)

try:
    print(">>> PASO 2: Obteniendo API Key...")
    # Lógica simplificada de servicio
    api_key = ApiKey.objects.filter(is_enabled=True, is_quarantined=False).first().key
    print("   [OK] Key obtenida.")
except Exception as e:
    print(f"   [FAIL] No hay API Key válida: {e}")
    sys.exit(1)

try:
    print(">>> PASO 3: Configurando Gemini Library...")
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    print("   [OK] Configurado.")
except Exception as e:
    print(f"   [FAIL] Import/Config Gemini: {e}")
    sys.exit(1)

try:
    print(">>> PASO 4: Formateando Prompts...")
    now = timezone.now()
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S (%A)")
    
    # Aquí es donde fallaba antes, probamos de nuevo
    skill_fmt = UNIVERSIA_AGENDA_SKILL.format(current_time=current_time_str)
    print("   [OK] Skill format success.")
    
    base_prompt = UNIVERSIA_NAVIGATION_PROMPT.format(agenda_skill=skill_fmt)
    print("   [OK] Base Prompt format success.")
except Exception as e:
    print(f"   [FAIL] Error formateo strings: {e}")
    sys.exit(1)

try:
    print(">>> PASO 5: Generando Respuesta IA (API CALL)...")
    model = genai.GenerativeModel('gemini-2.5-flash-lite', system_instruction=base_prompt)
    chat = model.start_chat(history=[])
    
    # Hacemos una llamada REAL
    response = chat.send_message("Hola UniversIA")
    print(f"   [OK] Respuesta IA recibida: {response.text[:30]}...")
except Exception as e:
    print(f"   [FAIL] Fallo en llamada a Gemini API: {e}")
    sys.exit(1)

print("\n>>> DIAGNÓSTICO FINAL: Todo funciona correctamente a nivel unitario.")
print(">>> Si esto pasa pero la web falla, el problema está en views.py o en la gestión de la sesión del usuario.")
