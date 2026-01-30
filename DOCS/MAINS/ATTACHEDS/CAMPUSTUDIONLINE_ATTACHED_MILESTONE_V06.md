### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
Al iniciar cualquier sesión de trabajo sobre el sistema de evaluaciones, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del Emulador UGR:
1.  /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md
2.  /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md

---

# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# Estado: EN PROGRESO (NÚCLEO RECONSTRUIDO)

## 1. RESUMEN TÉCNICO DE LA SESIÓN
Se ha realizado una reconstrucción integral de la infraestructura de generación para subsanar un colapso de sintaxis y lógica.

### Intervenciones Realizadas:
- **Reconstrucción de `orchestrator/tasks.py`:** Restaurada la integridad del archivo con indentación de 4 espacios. Recuperadas las funciones de automatización masiva perdidas.
- **Implementación de Factory Atómico:** El orquestador delega ahora la creación de prompts a las estrategias segregadas en tiempo de ejecución (Fase B).
- **Corrección de Parser (Caso Chino #294):** El parser JSON ahora soporta objetos únicos (diccionarios) envolviéndolos automáticamente en listas, evitando el fallo de "Generación/Parseo".
- **Mapeo de Claves Robusto:** Unificado el acceso a `model_answer` y `answer` en la caché y en los modelos de base de datos.
- **Refuerzo de Estrategia de Idiomas:** Refactorizado el prompt en `languages_strategy.py` para obligar a la IA a incluir el enunciado y el contenido lingüístico, eliminando la "Generación Fantasma".

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
La próxima sesión debe regirse estrictamente por los siguientes puntos sin margen de suposición:

1. **Auditoría de la Evaluación #297:** Verificar manualmente que el `question_text` contiene tanto la instrucción en castellano como el cuerpo del ejercicio en chino.
2. **Diagnosis de Logs de Eventos:** Investigar la causa por la cual las subtareas de generación atómica no están persistiendo correctamente sus mensajes de progreso en el `event_log` visible en el panel de administración.
3. **Simulación de Cuarentena (Stress Test):** Ejecutar un script para agotar la cuota de la clave activa y validar que el sistema realiza la rotación a la siguiente clave disponible sin abortar el examen en curso.
4. **Verificación de Limpieza de Respaldo:** Comprobar que tras un `SUCCESS` en la generación, el archivo JSON correspondiente en `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment_recovery/` es eliminado automáticamente.
