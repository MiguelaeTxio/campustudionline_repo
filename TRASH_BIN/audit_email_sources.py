import os

# Configuración
PROJECT_ROOT = '/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/'
OUTPUT_FILE = '/home/MiguelAeTxio/SWAP/EMAIL_AUDIT_REPORT.txt'

# Términos a buscar (Funciones de envío y textos del correo "fugitivo")
KEYWORDS = [
    'send_mail',
    'EmailMultiAlternatives',
    'EmailMessage',
    'send_mass_mail',
    'mail_admins',
    'mail_managers',
    'Clave(s) API',
    'BUZÓN PROCESADO',
    'Automation'
]

# Directorios a ignorar
IGNORE_DIRS = {'.git', '__pycache__', 'venv', 'env', '.idea', '.vscode', 'staticfiles_production', 'media', 'site-packages'}

def audit_project():
    print(f"Iniciando auditoría en: {PROJECT_ROOT}")
    results = []

    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Filtrar directorios ignorados
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if file.endswith('.py') or file.endswith('.html') or file.endswith('.txt'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            for keyword in KEYWORDS:
                                if keyword in line:
                                    # Guardamos ruta relativa para facilitar lectura
                                    rel_path = os.path.relpath(file_path, PROJECT_ROOT)
                                    result = f"[{keyword}] Found in {rel_path}:{i+1} -> {line.strip()}"
                                    results.append(result)
                except Exception as e:
                    print(f"Error leyendo {file}: {e}")

    # Escribir reporte
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"REPORTE DE AUDITORÍA DE EMAILS - {len(results)} hallazgos\n")
        f.write("===================================================\n\n")
        for item in results:
            f.write(item + "\n")
    
    print(f"\nAuditoría completada. Reporte generado en: {OUTPUT_FILE}")

if __name__ == "__main__":
    audit_project()
