import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from contents.services.navigation_builder import NavigationTreeBuilder

User = get_user_model()
USERNAME = "CampuStudiOnline"

def inspect_builder():
    try:
        user = User.objects.get(username=USERNAME)
        print(f"--- INSPECCIONANDO BUILDER PARA: {user.username} ---")
        
        # Instanciar el builder REAL
        builder = NavigationTreeBuilder(user)
        
        # Ejecutar la función interna que construye la sección de copias
        print("Ejecutando _build_copies_section()...")
        copies_data = builder._build_copies_section()
        
        # Buscar "Cálculo I" en los resultados
        found = False
        
        # Buscar en Academic
        if 'academic' in copies_data:
            for subject, copies in copies_data['academic'].items():
                for copy in copies:
                    if "Cálculo I" in copy['title']:
                        print(f"\n[ACADEMIC] Encontrado: {copy['title']}")
                        print(f"STATUS RAW EN JSON: '{copy.get('assessment_status')}'")
                        print(f"DATOS COMPLETOS: {copy}")
                        found = True

        # Buscar en Free (por si acaso)
        if 'free' in copies_data:
            for copy in copies_data['free']:
                if "Cálculo I" in copy['title']:
                    print(f"\n[FREE] Encontrado: {copy['title']}")
                    print(f"STATUS RAW EN JSON: '{copy.get('assessment_status')}'")
                    found = True

        if not found:
            print("\n❌ 'Cálculo I' NO aparece en la salida del builder.")
            
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO EJECUTANDO BUILDER: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    inspect_builder()
