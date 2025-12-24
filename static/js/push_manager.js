// /static/js/push_manager.js
// ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'
/**
 * Gestor de Notificaciones Push v3.1 ("Fort Knox - Instrumentado")
 * Refactorización completa para soportar la nueva arquitectura multi-dispositivo.
 * - Genera/recupera un UUID persistente para el navegador (browser_uuid).
 * - Envía el browser_uuid y el User-Agent al servidor junto con la suscripción.
 * - Añadida sonda de depuración para inspeccionar el payload de suscripción.
 */

(function() {
    'use strict';

    if (!('serviceWorker' in navigator) || !('PushManager' in window) || !window.django_data || !window.django_data.isUserAuthenticated) {
        console.warn('Push Manager: Navegador no compatible, usuario no autenticado o faltan datos (django_data).');
        return;
    }

    const { vapidPublicKey, saveSubscriptionUrl } = window.django_data;
    const banner = document.getElementById('push-notification-banner');
    const acceptButton = document.getElementById('accept-push');
    const denyButton = document.getElementById('deny-push');
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // [FORT KNOX] Función para obtener/crear el UUID del navegador.
    function getBrowserUUID() {
        let browserUUID = localStorage.getItem('browser_uuid');
        if (!browserUUID) {
            console.log("Push Manager [Fort Knox]: No se encontró UUID de navegador. Creando uno nuevo.");
            browserUUID = crypto.randomUUID();
            localStorage.setItem('browser_uuid', browserUUID);
        } else {
            console.log("Push Manager [Fort Knox]: UUID de navegador recuperado de localStorage.");
        }
        return browserUUID;
    }

    function initializePushManager() {
        const permission = Notification.permission;
        if (permission === 'granted') {
            registerServiceWorkerAndSubscribe();
        } else if (permission === 'denied') {
            // El usuario ha denegado los permisos. No se hace nada.
        } else {
            if (!sessionStorage.getItem('pushNotificationDenied')) {
                showBanner();
            }
        }
    }

    function showBanner() { if (banner) banner.style.display = 'block'; }
    function hideBanner() { if (banner) banner.style.display = 'none'; }

    if (acceptButton) {
        acceptButton.addEventListener('click', () => {
            hideBanner();
            requestPermissionAndSubscribe();
        });
    }

    if (denyButton) {
        denyButton.addEventListener('click', () => {
            hideBanner();
            sessionStorage.setItem('pushNotificationDenied', 'true');
        });
    }

    async function requestPermissionAndSubscribe() {
        try {
            const permission = await Notification.requestPermission();
            if (permission === 'granted') {
                await registerServiceWorkerAndSubscribe();
            }
        } catch (error) {
            console.error('Push Manager: Error al solicitar permiso.', error);
        }
    }

    async function registerServiceWorkerAndSubscribe() {
        try {
            console.log('Push Manager: Registrando Service Worker...');
            await navigator.serviceWorker.register('/service-worker.js');
            console.log('Push Manager: Service Worker registrado.');

            const registration = await navigator.serviceWorker.ready;
            console.log('Push Manager: Service Worker listo.');

            let subscription = await registration.pushManager.getSubscription();
            if (subscription === null) {
                console.log('Push Manager: Creando nueva suscripción...');
                const applicationServerKey = urlBase64ToUint8Array(vapidPublicKey);
                subscription = await registration.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey });
                await sendSubscriptionToServer(subscription, 'creada');
            } else {
                console.log('Push Manager: Sincronizando suscripción existente.');
                await sendSubscriptionToServer(subscription, 'existente');
            }
        } catch (error) {
            console.error('Push Manager: Error durante el registro o la suscripción.', error);
        }
    }

    async function sendSubscriptionToServer(subscription, action) {
        // [FORT KNOX] Obtenemos los nuevos datos requeridos por el backend.
        const browserUUID = getBrowserUUID();
        const userAgent = navigator.userAgent;

        // [FORT KNOX] Construimos el nuevo payload.
        const payload = {
            subscription_data: subscription.toJSON(), // subscription.toJSON() es estándar
            browser_uuid: browserUUID,
            user_agent: userAgent
        };

        // --- INICIO DE LA SONDA DE DEPURACIÓN ---
        console.log('%c[SONDA DE DIAGNÓSTICO OPERA]', 'color: #ff1b8d; font-weight: bold; font-size: 1.2em;');
        console.log('Payload completo a enviar al servidor:');
        console.dir(payload);
        // --- FIN DE LA SONDA DE DEPURACIÓN ---

        try {
            const response = await fetch(saveSubscriptionUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                body: JSON.stringify(payload) // Enviamos el nuevo payload
            });

            if (response.ok) {
                const logMessage = action === 'creada' ?
                    'Nueva suscripción guardada en el servidor.' :
                    'Suscripción existente sincronizada con el servidor.';
                console.log(`Push Manager [Fort Knox]: ¡ÉXITO! ${logMessage}`);
            } else {
                const errorData = await response.json();
                 // Si la vista está en modo mantenimiento, lo indicamos claramente.
                if (response.status === 501) {
                    console.warn(`Push Manager [Fort Knox]: El servidor indica que el endpoint está en mantenimiento. ${errorData.message}`);
                } else {
                    console.error('Push Manager [Fort Knox]: Error del servidor al guardar la suscripción.', {
                        status: response.status,
                        statusText: response.statusText,
                        error: errorData
                    });
                }
            }
        } catch (error) {
            console.error('Push Manager [Fort Knox]: Error de red al enviar la suscripción.', error);
        }
    }

    function urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);
        for (let i = 0; i < rawData.length; ++i) { outputArray[i] = rawData.charCodeAt(i); }
        return outputArray;
    }

    window.addEventListener('load', initializePushManager);

})();