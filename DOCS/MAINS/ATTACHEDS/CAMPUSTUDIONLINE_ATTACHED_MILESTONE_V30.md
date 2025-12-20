# Hito 30: Sistema de Atribución Comercial por Código de Recomendación

## 1. Visión Estratégica
Implementación de un motor de crecimiento basado en Relaciones Públicas (PR). Un usuario del grupo 'Comerciales' distribuye códigos únicos de 4 dígitos. El sistema debe rastrear la conversión desde el registro hasta el uso activo de la plataforma para liquidar comisiones por hitos alcanzados.

## 2. Definiciones Técnicas Inmutables
*   **Actor Principal:** Usuario perteneciente al Grupo de Django `Comerciales`.
*   **Identificador de Conversión:** Código alfanumérico de 4 caracteres (Ej: `4A7K`).
*   **Hitos de Pago (Conversión):**
    1.  **Registro:** Usuario nuevo crea cuenta usando un código válido.
    2.  **Primera Copia:** Usuario referido crea su primera `ContentCopy` en la Sala de Estudio.
    3.  **Primera Evaluación:** Usuario referido solicita su primera `Assessment`.

## 3. Arquitectura de Datos (Modelos en App 'users')
*   **Modelo `RecommendationCode`:**
    *   `code`: CharField(4), unique=True, db_index=True. (Alfanumérico: A-Z, 0-9).
    *   `vendor`: ForeignKey(User, limit_choices_to={'groups__name': 'Comerciales'}).
    *   `is_used`: BooleanField(default=False).
    *   `redeemed_by`: OneToOneField(User, null=True, blank=True) -> El usuario que se registró.
    *   `date_redeemed`: DateTimeField(null=True).
*   **Campos de Control en `UserProfile`:**
    *   `referred_by`: ForeignKey(User, related_name='referrals') -> Apunta al Comercial.
    *   `has_claimed_copy_incentive`: BooleanField(default=False).
    *   `has_claimed_assessment_incentive`: BooleanField(default=False).

## 4. Lógica de Negocio y Flujos
*   **Generador de Códigos:** Script para crear paquetes de N códigos asignados a un Comercial, garantizando no duplicidad.
*   **Refactorización del Registro:**
    *   Formulario: Añadir campo opcional `referral_code`.
    *   Validación: Comprobar existencia y que `is_used` sea False.
    *   Procesamiento: Al crear el usuario, marcar el código como usado, vincular al `redeemed_by` y establecer el `referred_by` en el perfil del nuevo usuario.
*   **Sistema de Atribución (Signals):**
    *   `post_save` en `contents.ContentCopy`: Si el autor tiene `referred_by` y `has_claimed_copy_incentive` es False -> Marcar True y registrar conversión para el Comercial.
    *   `post_save` en `assessment.Assessment`: Si el autor tiene `referred_by` y `has_claimed_assessment_incentive` es False -> Marcar True y registrar conversión para el Comercial.

## 5. Dashboard del Comercial (Frontend)
*   **Acceso:** Restringido a miembros del grupo 'Comerciales'.
*   **Métricas en tiempo real:**
    *   Lista de códigos disponibles (paquetes actuales).
    *   Lista de códigos gastados con fecha y usuario referido.
    *   Contador de "Conversiones de Registro".
    *   Contador de "Conversiones de Contenido" (Primeras copias).
    *   Contador de "Conversiones de Evaluación" (Primeras evaluaciones).
*   **Interacción:** Botón para solicitar nuevo paquete de códigos (dispara notificación al Admin).

## 6. Hoja de Ruta Táctica para la Próxima Sesión
1.  [ ] **FASE 1: Datos.** Crear el modelo `RecommendationCode` y actualizar `UserProfile` con los flags de control.
2.  [ ] **FASE 2: Backend.** Implementar el generador de códigos y la lógica de validación en el formulario de registro.
3.  [ ] **FASE 3: Automatización.** Programar las signals en `contents` y `assessment` para la atribución de hitos.
4.  [ ] **FASE 4: UI/UX.** Construir el Dashboard del Comercial y el sistema de solicitud de lotes.
