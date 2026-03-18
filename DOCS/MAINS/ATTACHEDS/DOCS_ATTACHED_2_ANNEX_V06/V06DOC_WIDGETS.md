<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_WIDGETS.md -->
# V06DOC_WIDGETS - CATÁLOGO DE COMPONENTES DE INTERFAZ (V1.1)

## 1. LIBRERÍA DE COMPONENTES TÉCNICOS

*   W-TECH-CALC (Consola de Cálculo Procedimental):
    *   Uso: Ingenierías y Ciencias.
    *   Funciones: Renderizado MathJax, entrada multietapa, bloqueo de traza lógica.
*   W-CLIN-SCAN (Visor de Evidencia Diagnóstica):
    *   Uso: Medicina, Odontología, Veterinaria.
    *   Funciones: Zoom HD de imágenes médicas, herramientas de medida y marcado de hallazgos.
*   W-OBJ-STRIKE (Selector de Respuesta con Riesgo):
    *   Uso: Lenguas y Materias Troncales.
    *   Funciones: Sistema de descarte visual (tachado) e indicador de riesgo de penalización. Soporte para Media Assets (Audio/Imagen context).

## 2. LIBRERÍA DE COMPONENTES DISCURSIVOS Y DE ACCIÓN

*   W-HUM-TEXT (Editor de Exégesis Crítica):
    *   Uso: Humanidades y Artes.
    *   Funciones: Pantalla dividida (Fuente vs Ensayo), gestor de citas por arrastre, contador de penalización formal.
    *   **Directriz de Multimodalidad (Miguel Ángel):** Al interactuar con el editor, el sistema DEBE ofrecer obligatoriamente el selector de entrada:
        1. **Teclado Nativo:** Layout del idioma objetivo (ej. Árabe, Ruso).
        2. **Occidentalización:** Transliteración/Pinyin/Romaji para alfabetos no latinos.
        3. **Pad Virtual/Trazos:** Escritura manual digital (Caligrafía).
        4. **OCR/Captura:** Digitalización de manuscrito físico del alumno.

*   W-PROC-ACTION (Panel de Acción Crítica):
    *   Uso: Salud y Seguridad Industrial.
    *   Funciones: Checklist dinámico de seguridad, cronómetro ECOE, validación de pasos obligatorios.
*   W-COMM-DIALOG (Interfaz de Mediación Dialéctica):
    *   Uso: Lenguas, Derecho, Educación.
    *   Funciones: Grabadora de audio, chat interactivo con IA UniversIA, análisis de registro formal/informal. Soporte para entrada multimodal en el chat.
*   W-LAW-NAV (Navegador de Marco Normativo):
    *   Uso: Derecho y Ciencias Sociales.
    *   Funciones: Acceso a repositorio legal/normativo emulado, buscador de jurisprudencia y cita rápida.

## 3. LIBRERÍA DE COMPONENTES LINGÜÍSTICOS Y ESTRUCTURALES (NUEVO V1.1)

*   W-TXT-CLOZE (Integrador de Huecos en Texto):
    *   Uso: Lenguas (Use of English) y Derecho (Completar escritos).
    *   Funciones: Renderizado de texto fluido con inputs incrustados. Soporta modo "Open" (Caja de texto) y "Select" (Dropdown en el hueco).
    *   **Directriz de Multimodalidad (Miguel Ángel):** Los inputs en modo "Open" deben heredar el selector de entrada multimodal (Teclado/Trazos/OCR) para garantizar la precisión caligráfica en lenguas Minor/Maior.
    *   **Mandato Minor (Bloqueo Caligráfico) [NUEVO V3.1]:** En el subarquetipo SUB-LIN-MINOR, cuando el `target_language_code` sea no-latino (Chino, Japonés, Árabe, Hebreo, Ruso), los inputs en modo "Open" quedan bloqueados EXCLUSIVAMENTE a **Pad de Trazos** u **OCR**. Se deshabilita el teclado occidental para forzar la evaluación de la grafía real.
*   W-MIX-MATCH (Matriz de Vinculación):
    *   Uso: Lenguas (Reading Headlines) y Ciencias (Concepto-Definición).
    *   Funciones: Arrastrar y soltar (Drag & Drop) o conectores visuales entre dos columnas.

## 4. ESTRATEGIA DE LAYOUT Y PANELES (NUEVO V1.2 - UX OPTIMIZATION)

*   **W-LAYOUT-SIDE (Panel Lateral Persistente):**
    *   **Función:** Muestra el "Estímulo de Sección" (Texto de lectura, Supuesto de hecho, Datos clínicos) de forma estática (Sticky) mientras el alumno hace scroll en las preguntas.
    *   **Justificación UX:** Evita el scroll vertical repetitivo ("Yo-Yo effect").
    *   **Contenido:** Estrictamente el material generado para el examen (Reading/Caso). NUNCA los apuntes del alumno.
