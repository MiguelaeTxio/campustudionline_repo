# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/management/commands/clean_task_logs.py
import json
from django.core.management.base import BaseCommand
from orchestrator.models import PendingContentTask

class Command(BaseCommand):
    help = 'Limpia los logs de tareas eliminando los payloads pesados (prompts) para liberar espacio en la BBDD.'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando limpieza de logs...")
        tasks = PendingContentTask.objects.all()
        count = 0
        cleaned_entries_total = 0

        for task in tasks:
            modified = False
            if not task.task_log or not isinstance(task.task_log, list):
                continue
            
            for entry in task.task_log:
                if 'payload' in entry:
                    payload_content = entry['payload']
                    
                    # El payload se guarda como string JSON en log_task_event
                    if isinstance(payload_content, str):
                        try:
                            payload_dict = json.loads(payload_content)
                            if 'prompt' in payload_dict:
                                del payload_dict['prompt']
                                # Volvemos a serializar sin el prompt
                                entry['payload'] = json.dumps(payload_dict, indent=2, ensure_ascii=False, sort_keys=True)
                                modified = True
                                cleaned_entries_total += 1
                        except (json.JSONDecodeError, TypeError):
                            # Si no es JSON válido o es otro tipo, lo ignoramos
                            pass
            
            if modified:
                task.save(update_fields=['task_log'])
                count += 1
                if count % 10 == 0:
                    self.stdout.write(f"Procesadas {count} tareas...")

        self.stdout.write(self.style.SUCCESS(f'Limpieza completada. Se actualizaron {count} tareas y se limpiaron {cleaned_entries_total} entradas de log.'))
