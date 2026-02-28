<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_INCIDENTS_ROADMAP.md -->
# HOJA DE RUTA DE REPARACIÓN: 55 INCIDENCIAS HITO 06

1. [X] Sobrescritura de metadata en Orquestador (Destrucción de TaskInstruction).
2. [X] Schema IA: Inclusión prohibida de widget_id en la salida de la IA.
3. [X] Schema IA: Inclusión prohibida de block_type en la salida de la IA.
4. [X] Schema IA: Omisión del campo obligatorio feedback_justification.
5. [X] Schema IA: Falta de validación minItems: 4 para opciones de respuesta.
6. [X] Schema IA: Etiquetas de competencia/cognitivas abiertas (Faltan Enums).
7. [X] Schema IA: Omisión de parámetros técnicos (Density, Quality, Bias).
8. [X] Orquestador: Audio de Listening generado desde Stem (Pregunta) en lugar de Estímulo.
9. [X] Cuotas: Mecanismo de penalización EXPIRED_UNTAKEN inoperante (Sin cambio de estado).
10. [X] Motor PRM-STRIKE: Penalización hardcodeada a -0.33 en Ciencias.
11. [X] Motor PRM-STRIKE: Penalización hardcodeada a -0.25 en Sociales.
12. [X] Motor CLOZE: Bug de evaluación por comparación de Array vs String.
13. [X] Motor RBT-CANON: Falta de rigor estricto contra paráfrasis en niveles superiores.
14. [X] Motor RPP-TRAZA: Ausencia de lógica de Arrastre de Error (Inferencia).
15. [X] Motor DRA-HOLO: Valor de penalización incorrecto (-2.0 vs -2.5 documental).
16. [X] Motor DRA-HOLO: Lógica de calificación inexistente (Simulada).
17. [X] Bloque BMT-SHIFT: Ausencia total de motor de calificación (Bloque Fantasma).
18. [X] Itinerario ITIN_DOC: Ausencia total de lógica de detección y rigor.
19. [X] Itinerario ITIN_INV: Rigor insuficiente (No es FATAL como exige el doc).
20. [X] Estructura Ciencias: Omisión de fase obligatoria SD_MODEL.
21. [X] Estructura Ciencias: Omisión de fase obligatoria SD_VERIF.
22. [X] Estructura Salud: Omisión de fase obligatoria SD_NORM.
23. [X] Estructura Sociales: Omisión de fase obligatoria SD_ETHI.
24. [X] Estructura Artes: Omisión de fase obligatoria SD_ARTE.
25. [X] Mapeo: Violación de la Barrera de Fuego (localized_sections en arquetipos no-LANG).
26. [X] Mapeo: Clasificación por defecto a ARCH_SOC (Violación de prohibición).
27. [X] Notificación: Falta de aviso por Email en fallo fatal de generación de examen.
28. [X] Taxonomía: Desfase documental entre ARCH_SCI y LOGIC_MAPPING.
29. [X] Rigor: Factor multiplicador x1.3 para MAIOR+LVL_B inexistente en código.
30. [X] Rigor: La matriz de rigor ignora el Itinerario (Solo usa el Nivel).
31. [X] Arquitectura: Crash sistémico (AttributeError) - 83% de estrategias sin get_immersion_mode.
32. [X] Modelo: Falta campo level_requisite en ExamItem.
33. [X] Modelo: Falta campo weight en ExamItem.
34. [X] Modelo: Falta campo estimated_time en ExamItem.
35. [X] Reporte: Ruta de acceso al feedback errónea en HTML (Busca en metadata).
36. [X] Acreditación: Violación de Gating (CERTACCLES exige 50% por destreza, no media).
37. [X] Acreditación: Mutilación de estaciones ECOE (De 5 obligatorias a 3).
38. [X] Acreditación: Ausencia total de Escala Likert para Salud.
39. [X] Acreditación: Falta motor para bloques especializados (Planos/Demostración).
40. [X] Acreditación: Falta motor para simulación judicial en Derecho.
41. [ ] Frontend: W-TECH-CALC carece de bloqueo de traza lógica.
42. [ ] Frontend: W-CLIN-SCAN carece de Zoom HD.
43. [ ] Frontend: W-CLIN-SCAN carece de herramientas de medida.
44. [ ] Frontend: W-OBJ-STRIKE carece de indicador visual de riesgo de penalización.
45. [ ] Frontend: W-HUM-TEXT carece de gestor de citas por arrastre.
46. [ ] Frontend: W-HUM-TEXT carece de métricas de calidad formal en tiempo real.
47. [ ] Frontend: W-PROC-ACTION carece de cronómetro específico ECOE.
48. [ ] Frontend: W-COMM-DIALOG carece de interfaz de chat/UniversIA.
49. [ ] Frontend: W-LAW-NAV inexistente (0% código implementado).
50. [ ] Frontend: W-TXT-CLOZE incompleto (Falta modo Dropdown/Select).
51. [ ] Validación: Falsos positivos en script de test por uso de fallbacks.
52. [ ] Validación: Rama de Ciencias Puras totalmente excluida de las pruebas masivas.
53. [ ] Validación: IDs de sub-arquetipos desincronizados entre script y estrategias.
54. [ ] Celery: Bucle de reintentos locales falsea el conteo de MaxRetries.
55. [ ] UI: Imposibilidad de comparar dos fuentes simultáneamente en bloque hermenéutico.
