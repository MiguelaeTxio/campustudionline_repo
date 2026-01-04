import os

file_path = '/home/MiguelAeTxio/PROJECTS/Mecalygest/DOCS/MAINS/MECALYGEST_MASTER_DOCUMENT.md'

new_content = """# Documento Maestro del Proyecto: MECALYGEST

**Filosofía:** Este documento es la única fuente de verdad para la arquitectura, estándares y hoja de ruta específicos del proyecto MECALYGEST.

---

## 1. Arquitectura y Lógica de Negocio

**Nombre del Proyecto:** MECALYGEST (Mecanizado de Albaranes y Gestión).

**Tecnología Principal:** Django Framework + Google Gemini (IA).

**Objetivo Principal:** Sistema integral para la digitalización, mecanizado inteligente y gestión de costes. El sistema centraliza la recepción de documentos (albaranes de proveedores y partes de trabajo), automatiza su procesamiento mediante IA y permite un control analítico de costes imputados a vehículos, obras o departamentos.

### 1.1. Diseño de Modelos de Datos

La arquitectura se centra en la **Gestión de Entradas**:

*   **Entidades:** `Proveedor` (Source), `Empleado` (Source).
*   **Destinos de Coste (Taxonomía):** `CentroCoste` (Abstracto) -> `Vehículo`, `Obra`, `Departamento`.
*   **Documentos:**
    *   `AlbaranEntrada`: Documento externo de proveedor con líneas de detalle.
    *   `ParteTrabajo`: Documento interno de imputación de horas/materiales.
*   **Gestión Documental:** Vinculación de archivos digitales (PDF/JPG) a cada registro transaccional.

---

## 2. Estándares y Convenciones del Proyecto

*(Cualquier estándar de código, nomenclatura o convención que se desvíe o complemente al Documento Maestro General.)*

---

## 3. Hoja de Ruta (Milestones)

### Hito 1: Definición del Proyecto y Hoja de Ruta [EN PROGRESO]
- **Objetivo:** Establecer el alcance funcional definitivo y la arquitectura técnica.
- **Entregables:** Documento Maestro actualizado, diagramas de flujo de ingesta.
- **Estado:** EN EJECUCIÓN.

### Hito 2: Arquitectura de Datos y Núcleo Transaccional [PENDIENTE]
- **Objetivo:** Construir el "cerebro" de la base de datos y el panel de administración.
- **Tareas:**
    - Implementación de modelos: `Proveedor`, `CentroCoste`, `AlbaranEntrada`, `ParteTrabajo`.
    - Configuración del Django Admin para gestión manual completa.
    - Definición de la Taxonomía de Gastos (Categorías).

### Hito 3: Interfaz de Operaciones y Bandeja de Entrada Digital [PENDIENTE]
- **Objetivo:** Crear el Frontend operativo y los canales de recepción asíncronos (Opción C y Web).
- **Tareas:**
    - Desarrollo de la Web App para gestión diaria.
    - **Sistema de Ingesta:** Implementación de "Bandeja de Entrada" donde caen los documentos antes de procesarse.
    - **Canal Email:** Configurar recepción automática (Scan-to-Email) desde impresoras de red.
    - **Canal Web:** Subida manual (Drag & Drop) y captura simple (Cámara móvil).

### Hito 4: Módulo de Captura Hardware (Agente Local) [PENDIENTE]
- **Objetivo:** Integración profunda con hardware local (Opción B).
- **Tareas:**
    - Desarrollo del "Agente Local MECALYGEST" (Script Python client-side).
    - Puente TWAIN/SANE para control directo de escáneres USB desde la web.
    - Impresión directa sin diálogos de sistema (opcional).

### Hito 5: Mecanizado Inteligente (IA) [PENDIENTE]
- **Objetivo:** Automatizar la introducción de datos.
- **Tareas:**
    - Integración con Google Gemini API.
    - **OCR Semántico:** Extracción automática de proveedor, fecha, totales y líneas.
    - **Auto-Clasificación:** La IA sugiere el `CentroCoste` basado en el contenido del albarán.

### Hito 6: Control de Gestión y Analítica [PENDIENTE]
- **Objetivo:** Explotación de datos.
- **Tareas:**
    - Dashboards de costes (Gastos por Vehículo, Rentabilidad de Obra).
    - Exportación de datos contables.

### Hito 7: Estabilización y Depuración (Beta Testing) [PENDIENTE]
- **Objetivo:** Garantizar la fiabilidad y usabilidad del sistema en un entorno de producción controlado.
- **Tareas:**
    - Despliegue piloto con usuarios reales.
    - Monitorización intensiva de logs y excepciones.
    - Resolución de incidencias (Bug fixing) y mejoras de UX.
    - Ajuste fino de prompts de IA según resultados reales.
"""

prop_path = file_path + '.prop'
with open(prop_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
