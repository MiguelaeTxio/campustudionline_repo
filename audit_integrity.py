import os

files_to_check = {
    "views.py": "/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/schedule/views.py",
    "event_form.html": "/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/schedule/templates/schedule/event_form.html",
    "event_confirm_delete.html": "/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/schedule/templates/schedule/event_confirm_delete.html",
    "schedule.js (Source)": "/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/schedule/static/schedule/js/schedule.js",
    "schedule.js (Prod)": "/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/staticfiles_production/schedule/js/schedule.js"
}

print("--- INFORME DE INTEGRIDAD DE ARCHIVOS ---")
for label, path in files_to_check.items():
    print(f"\nArchivo: {label}")
    if not os.path.exists(path):
        print(f"  Status: ❌ NO EXISTE")
        continue
    
    with open(path, 'r') as f:
        content = f.read()
        print(f"  Status: ✅ EXISTE")
        
        # Marcadores de parches
        if "HttpResponseRedirect" in content:
            count = content.count("HttpResponseRedirect")
            print(f"  - HttpResponseRedirect detectado (Count: {count})")
        
        if "X-Requested-With" in content or "x-requested-with" in content:
            print(f"  - Lógica AJAX detectada")
            
        if "alert('Sonda Error" in content:
            print(f"  - Sonda de alerta JS detectada: ✅")
        else:
            print(f"  - Sonda de alerta JS detectada: ❌")

        if "bubbles:true" in content:
            print(f"  - Burbujeo de eventos detectado: ✅")
        else:
            print(f"  - Burbujeo de eventos detectado: ❌")

        if "confirmar la eliminación" in content.lower():
            print(f"  - Fragmento de borrado estilizado detectado: ✅")

if __name__ == "__main__":
    pass
