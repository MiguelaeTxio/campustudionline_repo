<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_ROADMAP.md -->
# V06DOC_ROADMAP - MANIFIESTO DE CUMPLIMIENTO TÉCNICO (V2.1)

## 11. DEPURACIÓN DE ERRORES DE PRODUCCIÓN - [X] 100%
- [X] Resolución de TypeError en orquestador.
- [X] Validación de limpieza de CSS/HTML (Bleach Fix).

---

## 12. AUDITORÍA INTEGRAL DE DESALINEACIÓN (DOC-IMPL) - [X] 100%
- [X] Diagnóstico de Causa Raíz: Identificar por qué la implementación ignora sistemáticamente las directrices `V06DOC_*`.
- [X] Auditoría de Flujo Atómico: Investigar la nulidad de ítems generados (¿Fallo de prompt o de persistencia?).
- [X] Evaluación de Lógica Pedagógica: Analizar la incapacidad del motor para discriminar Itinerarios y Niveles.
- [X] Verificación de Fugas de Contexto: Determinar qué impide que la documentación satélite actúe como fuente de verdad en la ejecución.

--- 

---

## 13. DEPURACIÓN DEL CORE Y VALIDACIÓN - [ ] 0%
- [ ] Refactor `core/services/gemini_service.py`: Añadir soporte para `response_schema`.
- [ ] Test de Integración: Generación exitosa de ítems con `section_stimulus`.
- [ ] Validación UI: Verificación del panel lateral dinámico en el frontend.

--- 
**ESTADO:** EN PROGRESO (PENDIENTE REFACTOR DE FIRMA EN CORE).
