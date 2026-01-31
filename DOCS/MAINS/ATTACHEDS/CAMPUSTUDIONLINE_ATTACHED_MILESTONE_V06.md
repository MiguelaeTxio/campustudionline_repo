### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
Al iniciar cualquier sesión de trabajo sobre el sistema de evaluaciones, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del Emulador UGR:
1.  /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md
2.  /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md

---

# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# Estado: EN PROGRESO (ABSTRACCIÓN UNIVERSAL Y RIGOR UGR)

## 1. RESUMEN TÉCNICO ACUMULADO

### Fase 1: Infraestructura Base
- Reconstrucción de `orchestrator/tasks.py` para soporte de persistencia atómica y parser robusto.
- Implementación de Factory Atómico para despacho dinámico de estrategias.

### Fase 2: Arquitectura Universal de Idiomas (Sesión Actual)
- **Motor Agnóstico al Idioma:** Refactorizada `languages_strategy.py` eliminando diccionarios finitos. Ahora el sistema extrae la raíz lingüística del nombre de la asignatura y delega la localización en la IA.
- **Alineación Normativa UGR:** Corregido el itinerario **MINOR** eliminando el 'Reading Stimulus' de 400 palabras y pasando a un modelo de preguntas atómicas de gramática y vocabulario (Nivel HSK 1-3 / A1-A2).
- **Blindaje de Parser:** Parcheado `tasks.py` para interceptar y limpiar fugas de objetos `AttributedDict` en los estímulos de lectura de itinerarios **MAIOR**.
- **Validación de Resiliencia:** Ejecutado Stress Test exitoso de rotación de claves API ante límites de cuota y limpieza de archivos huérfanos en `assessment_recovery/`.
- **Dinamización de Frontend:** Cabeceras de sección ahora se muestran en el idioma objetivo según la traducción de la IA.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
1. **Validación Cruzada de Idiomas:** Generar evaluaciones para lenguas minoritarias (ej. Catalán, Gallego) y no latinas (ej. Griego o Coreano) para validar la extracción de raíz y la localización dinámica de etiquetas.
2. **Auditoría de Inmersión MAIOR:** Confirmar en exámenes de especialidad que el estímulo de lectura es texto plano limpio y que los 36 ítems mantienen el nivel académico exigido.
3. **Arquetipo LOGIC_AND_TECH:** Iniciar el desarrollo del esqueleto para Ingeniería/Ciencias, implementando el soporte mandatorio para fórmulas LaTeX en enunciados y respuestas.
