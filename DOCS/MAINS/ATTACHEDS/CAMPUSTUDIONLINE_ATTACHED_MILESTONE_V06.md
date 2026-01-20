# ANEXO HITO 6: SISTEMA DE AUTOEVALUACIONES CON IA (UGR EMULATOR)

**DIRECTRIZ OBLIGATORIA:** Al iniciar sesión con este hito, es **MANDATORIO** cargar el archivo:
`DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_MASTER_PLAN.md`

---

## ESTADO DE LA HOJA DE RUTA TÉCNICA (Ref. Plan Maestro)
1. [X] **Refactor de Orchestrator.** (Reparado: Eliminado fallback a Humanidades, saneamiento de imports y gestión de errores determinista).
2. [X] **Estrategia CEFR_LANGUAGES.** (Refinado: Implementada lógica adaptativa de instrucciones según nivel A1-C2. Estímulo siempre en idioma objetivo).
3. [X] **Estrategia LOGIC_AND_TECH.** (Completado).
4. [X] **Estrategia SOCIO_LEGAL.** (Completado).
5. [X] **Estrategia HEALTH_SCIENCES.** (Completado: Modelo ECOE/Estaciones Clínicas UGR).
6. [ ] **Estrategia HUMANITIES_ARTS.** (Pendiente: Refinar dialéctica y comentarios).

---

## LOG DE AVANCES DE ESTA SESIÓN
*   **Restauración Crítica:** Reconstrucción total de `models.py`, `views.py`, `utils.py` y `prompt_generators.py` tras incidente de corrupción.
*   **Sincronización BBDD:** Aplicadas migraciones 0025 y 0026 (campos `daily_limit`, `weekly_limit` y ajustes de arquetipo).
*   **Blindaje de Clasificación:** El Rector ya no deriva errores a "Humanidades". Si la clasificación falla, la tarea lanza un error trazable.
*   **Salud (UGR ECOE):** Implementado arquetipo 4 con enfoque en juicio clínico y seguridad.

---

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN
**Objetivo Primario:** Persistencia de Nivel CEFR y Finalización de Arquetipos.

1.  **Persistencia CEFR:** Modificar `orchestrator/tasks.py` para capturar el campo `cefr_level` del JSON de estímulos y pasarlo a la generación final del examen (evitar el hardcode de B1).
2.  **Estrategia Humanidades:** Refinar `humanities_strategy.py` para asegurar el rigor en el Arquetipo 5.
3.  **Pruebas Cruzadas:** Validar la rotación de formatos mediante el botón "Formato Incorrecto" con la nueva lógica adaptativa.
