{# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md #}
### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
La próxima sesión debe cargarse OBLIGATORIAMENTE con la siguiente constelación documental:
*   V06DOC_ARCHETYPES.md
*   V06DOC_SUBARCHETYPES.md
*   V06DOC_SUBDIVISIONS.md
*   V06DOC_BLOCKS.md
*   V06DOC_WIDGETS.md
*   V06DOC_METADATA.md
*   V06DOC_LEVELS.md
*   V06DOC_TEMPLATES.md
*   V06DOC_STRUCTURE.md
*   V06DOC_LOGIC_MAPPING.md
*   V06DOC_ROADMAP.md

**PROTOCOLO DEL MANIFIESTO (FUENTE DE LA VERDAD):**
El archivo V06DOC_ROADMAP.md es la ÚNICA fuente de verdad para el progreso. 
1. Es OBLIGATORIO auditar este archivo al inicio de cada sesión.
2. Es MANDATORIO actualizar su estado atómico (Checklist) al cierre de cada sesión.

---

# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: INTERFAZ Y CALIFICACIÓN CERTIFICADAS - ANTI-ABUSA DOCUMENTADO

### PARTE MUTABLE (RESUMEN Y HOJA DE RUTA)

## 1. RESUMEN TÉCNICO DE LA SESIÓN (CSO)
*   **Certificación de Arquetipos y Lógica:** Auditado el motor de calificación (`GradingOrchestrator`) y las estrategias (`health.py`, `tech.py`). El sistema respeta los roles académicos y las penalizaciones de la UGR.
*   **Alineación Front-Back (JSON Contracts):** Se ha reescrito integralmente `exam_take.html` como un "neonato" funcional. Ahora el JS genera payloads exactos para `RPP-TRAZA` (lista de objetos `{id, value}`) y `CDS-KILL` (toggle de seguridad), garantizando que el emulador sea un espejo de la documentación.
*   **Test End-to-End Exitoso:** Validado mediante script de diagnóstico (`verify_hito6_e2e.py`) el ciclo completo de creación, respuesta y calificación con un "TEST PASS" rotundo.
*   **Detección de Regresión y Solución Documental:** Identificado fallo en la navegación por ausencia de `expiration_date`. Se ha procedido a documentar formalmente la **Regla de las 24 horas (Anti-Abuso)** en `V06DOC_TEMPLATES.md` y `V06DOC_ROADMAP.md` antes de su implementación.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
**PROHIBIDO AVANZAR SIN CUMPLIR ESTOS PUNTOS:**

1.  **IMPLEMENTACIÓN DEL MODELO ANTI-ABUSO:** Añadir el campo `expiration_date` al modelo `Exam` en `assessment_v2/models/main.py` y ejecutar migraciones.
2.  **LÓGICA DE CADUCIDAD:** Programar el cálculo automático de +24h en el momento en que el examen pasa a estado 'READY' (tras la tarea de Celery).
3.  **CORRECCIÓN DE NAVEGACIÓN:** Reparar `contents/services/navigation_builder.py` para que utilice el nuevo campo `expiration_date` y filtre correctamente los exámenes disponibles para el usuario.
4.  **TEST DE PENALIZACIÓN:** Verificar que el sistema descuenta cuota o bloquea intentos ante exámenes caducados no realizados.

---
