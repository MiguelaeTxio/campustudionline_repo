// static/js/crypto_manager.js
// ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'

const scope = (typeof window !== 'undefined') ? window : self;

if (typeof scope.cryptoManager === 'undefined') {
    scope.cryptoManager = {};
}

(function(cryptoManager) {
    'use strict';
    console.log("Crypto Manager: Módulo v7.0 (IndexedDB Robusto) cargado.");

    let localPrivateKey = null;
    let localPublicKeyString = null;
    const hasLocalStorage = typeof scope.localStorage !== 'undefined';
    
    // --- GESTOR DE INDEXEDDB ---
    const DB_NAME = 'crypto_storage';
    const STORE_NAME = 'keys';
    const KEY_ID = 'privateKey';
    let dbPromise = null;

    function getDb() {
        if (!dbPromise) {
            dbPromise = new Promise((resolve, reject) => {
                const request = scope.indexedDB.open(DB_NAME, 1);
                request.onerror = (event) => reject(`Error al abrir IndexedDB: ${event.target.error}`);
                request.onsuccess = (event) => resolve(event.target.result);
                request.onupgradeneeded = (event) => {
                    const db = event.target.result;
                    if (!db.objectStoreNames.contains(STORE_NAME)) {
                        db.createObjectStore(STORE_NAME, { keyPath: 'id' });
                    }
                };
            });
        }
        return dbPromise;
    }

    async function saveKeyToDb(keyJwk) {
        if (typeof scope.indexedDB === 'undefined') return;
        console.log("Crypto Manager: Intentando guardar clave privada en IndexedDB.");
        try {
            const db = await getDb();
            const tx = db.transaction(STORE_NAME, 'readwrite');
            const store = tx.objectStore(STORE_NAME);
            store.put({ id: KEY_ID, key: keyJwk });
            await new Promise((resolve, reject) => {
                tx.oncomplete = () => resolve();
                tx.onerror = () => reject(tx.error);
            });
            console.log("Crypto Manager: Clave guardada en IndexedDB con éxito.");
        } catch (error) {
            console.error("Crypto Manager: Fallo al guardar la clave en IndexedDB.", error);
        }
    }

    // --- INICIO DE LA CORRECCIÓN CLAVE ---
    // Reescribimos la función para usar Promises correctamente y esperar el resultado.
    async function getKeyFromDb() {
        if (typeof scope.indexedDB === 'undefined') return null;
        console.log("Crypto Manager (SW): Buscando clave privada en IndexedDB.");
        try {
            const db = await getDb();
            return await new Promise((resolve, reject) => {
                const tx = db.transaction(STORE_NAME, 'readonly');
                const store = tx.objectStore(STORE_NAME);
                const request = store.get(KEY_ID);
                
                request.onsuccess = () => {
                    if (request.result) {
                        console.log("Crypto Manager (SW): ¡Clave encontrada en IndexedDB!");
                        resolve(request.result.key);
                    } else {
                        console.warn("Crypto Manager (SW): No se encontró registro de clave en IndexedDB.");
                        resolve(null);
                    }
                };
                request.onerror = (event) => {
                    console.error("Crypto Manager (SW): Error en la petición a IndexedDB.", event.target.error);
                    reject(event.target.error);
                };
            });
        } catch (error) {
            console.error("Crypto Manager (SW): Error crítico al leer desde IndexedDB.", error);
            return null;
        }
    }
    // --- FIN DE LA CORRECCIÓN CLAVE ---
    
    // --- FUNCIONES AUXILIARES ---
    function base64ToArrayBuffer(base64) {
        const binary_string = scope.atob(base64);
        const len = binary_string.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) { bytes[i] = binary_string.charCodeAt(i); }
        return bytes.buffer;
    }

    function arrayBufferToBase64(buffer) {
        let binary = '';
        const bytes = new Uint8Array(buffer);
        for (let i = 0; i < bytes.byteLength; i++) { binary += String.fromCharCode(bytes[i]); }
        return scope.btoa(binary);
    }
    
    // --- FUNCIONES CRIPTOGRÁFICAS ---
    async function deriveKeyFromPassword(password, salt) {
        const encoder = new TextEncoder();
        const keyMaterial = await scope.crypto.subtle.importKey("raw", encoder.encode(password), { name: "PBKDF2" }, false, ["deriveKey"]);
        return scope.crypto.subtle.deriveKey({ name: "PBKDF2", salt: salt, iterations: 100000, hash: "SHA-256" }, keyMaterial, { name: "AES-GCM", length: 256 }, true, ["encrypt", "decrypt"]);
    }

    async function decryptPrivateKeyWithPassword(encryptedString, password) {
        const parts = encryptedString.split(':');
        if (parts.length !== 3) throw new Error("Formato de clave cifrada inválido.");
        const [saltB64, ivB64, ciphertextB64] = parts;
        const salt = base64ToArrayBuffer(saltB64);
        const iv = base64ToArrayBuffer(ivB64);
        const data = base64ToArrayBuffer(ciphertextB64);
        const derivedKey = await deriveKeyFromPassword(password, salt);
        const decryptedBuffer = await scope.crypto.subtle.decrypt({ name: "AES-GCM", iv: iv }, derivedKey, data);
        return new TextDecoder().decode(decryptedBuffer);
    }

    async function importPublicKey(keyString) {
        const jwk = JSON.parse(keyString);
        return await scope.crypto.subtle.importKey('jwk', jwk, { name: "RSA-OAEP", hash: "SHA-256" }, true, ["encrypt"]);
    }

    // --- GESTOR DE UI (Solo para navegador) ---
    function requestPassword(mode, error = null) {
        if (!hasLocalStorage) return Promise.reject(new Error("requestPassword no está disponible."));
        return new Promise((resolve, reject) => {
            const overlay = document.getElementById('password-modal-overlay'); const titleEl = document.getElementById('password-modal-title'); const textEl = document.getElementById('password-modal-text'); const form = document.getElementById('password-modal-form'); const input = document.getElementById('password-modal-input'); const errorEl = document.getElementById('password-modal-error'); const cancelBtn = document.getElementById('password-modal-cancel-btn'); if (!overlay) return reject(new Error("HTML del modal no encontrado.")); if (mode === 'unlock') { titleEl.textContent = "Desbloquear Claves de Chat"; textEl.textContent = "Introduce tu contraseña para desbloquear tus claves de chat."; } if (error) { errorEl.textContent = error; errorEl.style.display = 'block'; } else { errorEl.style.display = 'none'; } input.value = ''; const cleanup = () => { overlay.style.display = 'none'; form.onsubmit = null; cancelBtn.onclick = null; }; const onSubmit = (e) => { e.preventDefault(); const password = input.value; if (password) { cleanup(); resolve(password); } }; const onCancel = () => { cleanup(); reject(new Error("Usuario canceló.")); }; form.onsubmit = onSubmit; cancelBtn.onclick = onCancel; overlay.style.display = 'flex'; input.focus();
        });
    }

    // --- FUNCIONES PÚBLICAS ---

    cryptoManager.initializeCrypto = async function() {
        // Lógica para el Service Worker
        if (!hasLocalStorage) {
            console.log("Crypto Manager (SW): Inicializando...");
            const privateKeyJwk = await getKeyFromDb();
            if (privateKeyJwk) {
                localPrivateKey = await scope.crypto.subtle.importKey('jwk', privateKeyJwk, { name: "RSA-OAEP", hash: "SHA-256" }, true, ["decrypt"]);
                console.log("Crypto Manager (SW): Clave privada cargada desde IndexedDB con éxito.");
                return { success: true };
            }
            console.error("Crypto Manager (SW): FALLO al cargar la clave privada desde IndexedDB.");
            return { success: false };
        }
        
        // Lógica para el navegador
        try {
            const localPrivateKeyJwkString = localStorage.getItem('privateKey');
            const localPublicKeyJwkString = localStorage.getItem('publicKey');
            const serverKeysResponse = await fetch('/messaging/get_keys/');
            const serverKeysData = await serverKeysResponse.json();

            if (localPublicKeyJwkString) {
                if (serverKeysData.status === 'success' && serverKeysData.public_key === localPublicKeyJwkString) {
                    console.log("Crypto Manager: Sincronizado. Cargando claves locales.");
                    const privateKeyJwk = JSON.parse(localPrivateKeyJwkString);
                    localPrivateKey = await scope.crypto.subtle.importKey('jwk', privateKeyJwk, { name: "RSA-OAEP", hash: "SHA-256" }, true, ["decrypt"]);
                    localPublicKeyString = localPublicKeyJwkString;
                    await saveKeyToDb(privateKeyJwk);
                    return { success: true };
                } else {
                    console.warn("Crypto Manager: DESINCRONIZACIÓN. Forzando recuperación.");
                    localStorage.removeItem('publicKey'); localStorage.removeItem('privateKey');
                    return await this.initializeCrypto();
                }
            }
            
            if (serverKeysData.status === 'success') {
                let privateKeyString;
                let errorMessage = null;
                while (true) {
                    try {
                        const password = await requestPassword('unlock', errorMessage);
                        privateKeyString = await decryptPrivateKeyWithPassword(serverKeysData.encrypted_private_key, password);
                        break;
                    } catch (e) {
                        if (e.message.includes("canceló")) { throw e; }
                        errorMessage = "Contraseña incorrecta. Inténtalo de nuevo.";
                    }
                }
                const privateKeyJwk = JSON.parse(privateKeyString);
                localStorage.setItem('publicKey', serverKeysData.public_key);
                localStorage.setItem('privateKey', privateKeyString);
                await saveKeyToDb(privateKeyJwk);
                return await this.initializeCrypto();
            }
            throw new Error(`Error al obtener claves del servidor: ${serverKeysData.message || 'Error'}`);
        } catch (error) {
            console.error("FALLO CRÍTICO en initializeCrypto (navegador).", error);
            localStorage.removeItem('publicKey'); localStorage.removeItem('privateKey');
            return { success: false };
        }
    };
    
    cryptoManager.decrypt = async function(contentPayload, currentUserId) {
        if (!localPrivateKey) {
            console.log("Descifrado: Clave no en memoria, inicializando...");
            const status = await cryptoManager.initializeCrypto();
            if (!status.success || !localPrivateKey) {
                 console.error("Fallo de inicialización al intentar descifrar. La clave privada no está disponible.");
                 return ">> Error: Clave de descifrado no disponible <<";
            }
        }
        const ciphertextBase64 = contentPayload[String(currentUserId)];
        if (!ciphertextBase64) return ">> Mensaje no disponible para ti <<";
        try {
            const ciphertextBuffer = base64ToArrayBuffer(ciphertextBase64);
            const decryptedBuffer = await scope.crypto.subtle.decrypt({ name: "RSA-OAEP" }, localPrivateKey, ciphertextBuffer);
            return new TextDecoder().decode(decryptedBuffer);
        } catch (error) {
            console.error("Error al descifrar el mensaje (posiblemente corrupto):", error);
            return ">> Mensaje ilegible (corrupto) <<";
        }
    };

    cryptoManager.createEncryptedPayload = async function(plaintext, otherUserPublicKeyString, currentUserId, otherUserId) {
        if (!localPrivateKey || !localPublicKeyString) {
             const status = await cryptoManager.initializeCrypto();
             if (!status.success) {
                alert("Error de configuración criptográfica. No se puede enviar el mensaje.");
                return null;
             }
        }
        try {
            const otherUserPublicKey = await importPublicKey(otherUserPublicKeyString);
            const ownPublicKey = await importPublicKey(localPublicKeyString);
            const ciphertextForOther = await scope.crypto.subtle.encrypt({ name: "RSA-OAEP" }, otherUserPublicKey, new TextEncoder().encode(plaintext));
            const ciphertextForSelf = await scope.crypto.subtle.encrypt({ name: "RSA-OAEP" }, ownPublicKey, new TextEncoder().encode(plaintext));
            return {
                [String(otherUserId)]: arrayBufferToBase64(ciphertextForOther),
                [String(currentUserId)]: arrayBufferToBase64(ciphertextForSelf)
            };
        } catch (error) {
            console.error("Error durante el doble cifrado:", error);
            alert("Error: No se pudo cifrar el mensaje.");
            return null;
        }
    };

})(scope.cryptoManager);