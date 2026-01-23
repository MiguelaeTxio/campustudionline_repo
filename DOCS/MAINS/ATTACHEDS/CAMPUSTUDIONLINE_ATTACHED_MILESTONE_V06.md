# ANEXO HITO 6: SISTEMA DE EVALUACIONES (ESTABILIZACIÓN ARQUITECTÓNICA)

**DIRECTRIZ OBLIGATORIA:** Al iniciar sesión con este hito, es **MANDATORIO** cargar el archivo:
`DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_MASTER_PLAN.md`

## ESTADO DE LA HOJA DE RUTA (POST-RESTRUCTURACIÓN)
1. [X] **Restauración de Sistema.** (Sintaxis corregida y servidor WSGI operativo).
2. [X] **Implementación de Atomic Flow (Fase A).** (Esqueletos deterministas delegados a estrategias).
3. [X] **Sincronización PAIR de Rotación.** (Blindaje ante errores 429 y rotación proactiva).
4. [X] **Purga de Código Muerto.** (Eliminada lógica obsoleta de clasificación por keywords).
5. [ ] **Validación de Arquetipo Minor (Chino).** (Pendiente testeo real tras restauración de prompts).
6. [ ] **Test de Estrategia LOGIC_AND_TECH.** (Verificación de LaTeX).

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN
1. **Validación Empírica de Clasificación:** Iniciar evaluación de Chino para verificar que el Rector (v4804ad0a) asigne CEFR_LANGUAGES y active el esqueleto de 4 bloques.
2. **Validación de UX Minor:** Comprobar integración de texto de lectura en el cuerpo del examen y ocultación de sidebar de referencia.
3. **Auditoría LaTeX:** Verificar renderizado en arquetipo de Ciencias (LOGIC_AND_TECH).
4. **Prueba de Corrección:** Validar que la IA procese correctamente los nuevos widgets de subida de archivos en la fase de evaluación.

## LOG DE CAMBIOS (NRA)
- Consolidada la sección 5 del Documento Maestro (Especificación Técnica de Evaluaciones).
- Implementada persistencia de 'section_label' y 'widget_type' en base de datos.
- Restaurado Clasificador Rector UGR original (commit 4804ad0a) tras detectar degradación de prompts.
- Sincronizado flujo de excepciones para forzar rotación proactiva de claves API.
- Desacoplado Orquestador de la lógica lingüística mediante delegación en estrategias.
