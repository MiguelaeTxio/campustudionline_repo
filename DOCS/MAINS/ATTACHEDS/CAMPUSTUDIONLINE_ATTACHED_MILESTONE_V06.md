### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
Al iniciar cualquier sesión de trabajo sobre el sistema de evaluaciones, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del Emulador UGR:
1.  /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md
2.  /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md

---

# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# Estado: EN PROGRESO (BLINDAJE LINGÜÍSTICO Y REFORMULACIÓN HSK)

## 1. RESUMEN TÉCNICO ACUMULADO

### Fase 1: Infraestructura Base
- Reconstrucción de `orchestrator/tasks.py` (indentación y funciones masivas).
- Implementación de Factory Atómico para delegación de prompts por arquetipo.
- Parser JSON robusto para soporte de objetos únicos (Caso Chino).

### Fase 2: Rigor Académico y Localización (Sesión Actual)
- **Blindaje Anti-Inglés:** Refactorizada `languages_strategy.py` con una instrucción de sistema agresiva que prohíbe el inglés y define al alumno como hispanohablante.
- **Rigor HSK/UGR:** Reestructurado el esqueleto `MINOR` para incluir Ordenación de Frases (`QT_ORDER`) y Caligrafía/Trazos (`REQ_DUAL`), eliminando los Cloze genéricos que no aplicaban.
- **Localización Castellano:** Traducidas todas las etiquetas de sección (`section_label`) para cumplir con la Regla de Oro del Idioma en la interfaz.
- **Trazabilidad Atómica:** Inyectados logs de progreso por cada pregunta en `tasks.py` con blindaje de conexión `db.close_old_connections()`.
- **Restauración de Badges:** Suavizada la lógica en `context_processors.py` para asegurar visibilidad de avisos en exámenes completados.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
1. **Validación de Inmersión Bilingüe:** Generar un examen MINOR (Chino/Japonés) y auditar que `question_text` es 100% [Castellano] + [Idioma Objetivo], sin intrusión de inglés.
2. **Stress Test de Claves API:** Ejecutar el script `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/TRASH_BIN/stress_test_rotation.py` para verificar que la cuarentena y rotación funcionan tras el 5º fallo.
3. **Auditoría de Widgets:** Verificar el renderizado de `REQ_ORDER` y `REQ_DUAL` en las nuevas tareas de ordenación y caligrafía.
4. **Validación de Cleanup:** Comprobar que `assessment_recovery/` se limpia tras una generación exitosa.
