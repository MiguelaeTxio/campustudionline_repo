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

## 13. DEPURACIÓN DEL CORE Y RE-ARQUITECTURA DOCUMENTAL - [X] 100%
- [X] Refactor `core/services/gemini_service.py`: Soporte para `response_schema` implementado.
- [X] Re-arquitectura "Python-Dictator": Documentación maestra reescrita para forzar el uso de Estrategias como Plantillas (Skeleton-First Real).
- [X] Auditoría de Integridad: Eliminación de ambigüedades en los 22 subarquetipos.

## 14. IMPLEMENTACIÓN DEL MOTOR DE PLANTILLAS - [ ] 0%
- [ ] Refactor `orchestrator/tasks.py`: Adaptar el bucle para inyectar contenido en `ExamItems` pre-existentes.
- [ ] Refactor `strategies/languages.py`: Implementar el método `get_exam_skeleton()` con widgets fijos.
- [ ] Fix Frontend: Renderizado del `section_stimulus` en el panel lateral persistente.

--- 
**ESTADO:** LISTO PARA IMPLEMENTACIÓN TÉCNICA (DOCUMENTACIÓN BLINDADA).
