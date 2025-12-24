// static/js/security_setup.js
// ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'

document.addEventListener('DOMContentLoaded', () => {
    // --- MODO DE DEPURACIÓN ---
    console.log("[Security Setup] Script iniciado y listo.");

    // --- OBTENCIÓN DE ELEMENTOS DEL DOM Y DATOS DE DJANGO ---
    const setupScript = document.getElementById('security-setup-script');
    const passwordForm = document.getElementById('password-form');
    const passwordInput = document.getElementById('user-password');
    const generateBtn = document.getElementById('generate-keys-btn');
    const formContainer = document.getElementById('password-form-container');
    const statusContainer = document.getElementById('security-status');

    if (!setupScript || !passwordForm || !statusContainer) {
        console.error("[Security Setup] Faltan elementos críticos del DOM. Abortando.");
        return;
    }

    const saveKeysUrl = setupScript.dataset.saveKeyUrl;
    const csrfToken = setupScript.dataset.csrfToken;
    const redirectUrl = setupScript.dataset.redirectUrl;

    // --- FUNCIONES AUXILIARES ---

    /**
     * Convierte un ArrayBuffer a una cadena Base64.
     * @param {ArrayBuffer} buffer El buffer a convertir.
     * @returns {string} La cadena en formato Base64.
     */
    function arrayBufferToBase64(buffer) {
        let binary = '';
        const bytes = new Uint8Array(buffer);
        const len = bytes.byteLength;
        for (let i = 0; i < len; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return window.btoa(binary);
    }

    // --- FUNCIONES CRIPTOGRÁFICAS ---

    /**
     * Genera un par de claves RSA-OAEP de 2048 bits.
     * @returns {Promise<CryptoKeyPair>} El par de claves pública y privada.
     */
    async function generateRsaKeyPair() {
        console.log("[Security Setup] Generando nuevo par de claves RSA-OAEP...");
        const keyPair = await window.crypto.subtle.generateKey(
            { name: "RSA-OAEP", modulusLength: 2048, publicExponent: new Uint8Array([1, 0, 1]), hash: "SHA-256" },
            true, ["encrypt", "decrypt"]
        );
        console.log("[Security Setup] Par de claves RSA generado con éxito.");
        return keyPair;
    }

    /**
     * Exporta una CryptoKey a formato de cadena JWK (JSON Web Key).
     * @param {CryptoKey} key La clave a exportar.
     * @returns {Promise<string>} La clave en formato de cadena JSON.
     */
    async function exportKeyAsString(key) {
        const exportedKey = await window.crypto.subtle.exportKey("jwk", key);
        return JSON.stringify(exportedKey);
    }

    /**
     * Cifra la clave privada usando una SAL proporcionada.
     * @param {string} privateKeyJwkString - La clave privada para cifrar.
     * @param {string} password - La contraseña del usuario.
     * @param {ArrayBuffer} salt - La sal criptográfica a utilizar (DEBE ser la misma para cifrar y descifrar).
     * @returns {Promise<string>} Una cadena que contiene iv y ciphertext, codificados en Base64 y separados por dos puntos. La sal ya no se incluye aquí.
     */
    async function encryptPrivateKey(privateKeyJwkString, password, salt) { // <--- MODIFICADO: Acepta la sal
        console.log("[Security Setup] Iniciando cifrado de la clave privada con la sal proporcionada...");
        const iv = window.crypto.getRandomValues(new Uint8Array(12));

        const passwordKey = await window.crypto.subtle.importKey('raw', new TextEncoder().encode(password), { name: 'PBKDF2' }, false, ['deriveKey']);
        const aesKey = await window.crypto.subtle.deriveKey(
            // USA LA SAL PROPORCIONADA
            { name: 'PBKDF2', salt: salt, iterations: 100000, hash: 'SHA-256' },
            passwordKey,
            { name: 'AES-GCM', length: 256 },
            true,
            ['encrypt']
        );
        console.log("[Security Setup] Clave AES derivada de la contraseña y la sal.");

        const encodedPrivateKey = new TextEncoder().encode(privateKeyJwkString);
        const encryptedPrivateKeyBuffer = await window.crypto.subtle.encrypt({ name: 'AES-GCM', iv: iv }, aesKey, encodedPrivateKey);
        console.log("[Security Setup] Clave privada cifrada con AES-GCM.");

        const B64_SALT = arrayBufferToBase64(salt);
        const B64_IV = arrayBufferToBase64(iv);
        const B64_CIPHERTEXT = arrayBufferToBase64(encryptedPrivateKeyBuffer);
        
        // Devolvemos el payload completo para mantener la consistencia en el archivado
        return `${B64_SALT}:${B64_IV}:${B64_CIPHERTEXT}`;
    }

    /**
     * Envía la clave pública, la clave privada cifrada Y LA SAL al servidor.
     * @param {string} publicKeyString - La clave pública en formato JWK string.
     * @param {string} encryptedPrivateKeyString - El paquete cifrado (salt:iv:ciphertext).
     * @param {string} saltB64 - La sal en formato Base64 para guardarla por separado.
     */
    async function sendKeysToServer(publicKeyString, encryptedPrivateKeyString, saltB64) { // <--- MODIFICADO: Acepta la sal
        console.log("[Security Setup] Enviando claves y sal al servidor...");
        const response = await fetch(saveKeysUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
            body: JSON.stringify({
                public_key: publicKeyString,
                encrypted_private_key: encryptedPrivateKeyString,
                encryption_salt: saltB64 // <--- NUEVO: Enviamos la sal para que el servidor la guarde
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Error del servidor: ${errorData.message || response.statusText}`);
        }
        
        console.log("[Security Setup] El servidor ha guardado las claves y la sal con éxito.");
        return response.json();
    }


    // --- FUNCIÓN PRINCIPAL Y MANEJADOR DE EVENTOS ---

    /**
     * Orquesta todo el proceso de generación y guardado de claves.
     */
    async function handleSecuritySetup(event) {
        event.preventDefault();
        console.log("[Security Setup] Formulario de contraseña enviado. Iniciando proceso.");

        const password = passwordInput.value;
        if (!password) {
            alert("Por favor, introduce tu contraseña.");
            return;
        }

        generateBtn.disabled = true;
        generateBtn.textContent = 'Procesando...';
        formContainer.style.display = 'none';
        statusContainer.style.display = 'block';

        try {
            // 1. Generar la sal UNA SOLA VEZ y convertirla a Base64 para enviarla al servidor.
            console.log("[Security Setup] Generando sal criptográfica...");
            const salt = window.crypto.getRandomValues(new Uint8Array(16));
            const saltB64 = arrayBufferToBase64(salt);
            console.log("[Security Setup] Sal generada.");

            // 2. Generar el par de claves RSA
            const keyPair = await generateRsaKeyPair();

            // 3. Exportar ambas claves a formato string (JWK)
            const publicKeyString = await exportKeyAsString(keyPair.publicKey);
            const privateKeyString = await exportKeyAsString(keyPair.privateKey);

            // 4. Guardar las claves SIN CIFRAR en localStorage para uso inmediato
            console.log("[Security Setup] Guardando claves en localStorage para uso del cliente.");
            localStorage.setItem('publicKey', publicKeyString);
            localStorage.setItem('privateKey', privateKeyString);

            // 5. Cifrar la clave privada usando la contraseña y la sal que acabamos de generar
            const encryptedPrivateKeyPayload = await encryptPrivateKey(privateKeyString, password, salt); // <--- MODIFICADO

            // 6. Enviar la clave pública, la privada CIFRADA y la SAL al servidor
            await sendKeysToServer(publicKeyString, encryptedPrivateKeyPayload, saltB64); // <--- MODIFICADO

            // 7. Redirigir en caso de éxito
            console.log(`[Security Setup] Configuración completada. Redirigiendo a: ${redirectUrl}`);
            window.location.href = redirectUrl;

        } catch (error) {
            console.error("[Security Setup] FALLO CRÍTICO en la configuración de seguridad:", error);
            statusContainer.innerHTML = `<h3 class="text-danger">¡Error en la Configuración!</h3><p>No pudimos configurar la seguridad de tu cuenta. Por favor, recarga la página para intentarlo de nuevo.</p><p class="text-muted small">Detalle del error: ${error.message}</p>`;
            formContainer.style.display = 'block';
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generar y Guardar Claves';
        }
    }

    // Adjuntar el manejador de eventos al formulario
    passwordForm.addEventListener('submit', handleSecuritySetup);
});