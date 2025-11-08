{# /home/MiguelAeTxio/CampuStudiOnline/messaging/templates/service-worker.js #}
{% load static %}

importScripts("{% static 'js/crypto_manager.js' %}");

self.addEventListener('push', function(event) {
    console.log('[Service Worker] Push notification received.');
    const eventPromise = handlePushEvent(event);
    event.waitUntil(eventPromise);
});

async function handlePushEvent(event) {
    let data = {};
    try {
        if (event.data) {
            data = event.data.json();
        }
    } catch (e) {
        data = { body: event.data.text() };
    }

    const title = data.title || 'CampuStudiOnline';
    let body = data.body || 'You have received a new notification.';
    
    const encryptedPayload = data.data?.encrypted_message_payload;
    const recipientId = data.data?.recipient_id;

    if (encryptedPayload && recipientId && typeof encryptedPayload === 'object') {
        console.log('[Service Worker] E2E payload detected. Attempting to decrypt...');
        try {
            // This call will now read from IndexedDB.
            const decryptedMessage = await self.cryptoManager.decrypt(encryptedPayload, recipientId);
            
            if (decryptedMessage && !decryptedMessage.startsWith(">>")) {
                body = decryptedMessage;
                console.log('[Service Worker] Message decrypted successfully.');
            } else {
                 console.warn('[Service Worker] Decryption returned an error. Using generic body.', decryptedMessage);
            }
        } catch (error) {
            console.error('[Service Worker] Critical decryption error. Using generic body.', error);
        }
    } else {
        console.log('[Service Worker] Standard notification (non-E2E).');
        if (encryptedPayload && encryptedPayload.body) body = encryptedPayload.body;
        if (encryptedPayload && encryptedPayload.title) data.title = encryptedPayload.title;
    }

    const options = {
        body: body,
        icon: data.icon || "{% static 'images/web-app-manifest-192x192.png' %}",
        badge: data.badge || "{% static 'images/favicon-96x96.png' %}",
        data: {
            url: data.data?.url || '/'
        }
    };

    return self.registration.showNotification(title, options);
}

self.addEventListener('notificationclick', function(event) {
    console.log('[Service Worker] Notification click received.');
    event.notification.close();
    event.waitUntil(
        clients.openWindow(event.notification.data.url)
    );
});

self.addEventListener('install', event => {
    console.log('Service Worker: Installed.');
    self.skipWaiting();
});

self.addEventListener('activate', event => {
    console.log('Service Worker: Activated.');
    event.waitUntil(clients.claim()); 
});
