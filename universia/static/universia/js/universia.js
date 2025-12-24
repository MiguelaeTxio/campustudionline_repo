document.addEventListener('DOMContentLoaded', function() {
        const container = document.getElementById('universia-widget-container');
    const currentContentTitle = container ? container.getAttribute('data-content-title') : null;
    
    // Inyectar HTML del widget si solo tenemos el contenedor
    if (container && !document.getElementById('universia-window')) {
        container.innerHTML = `
            <div id="universia-window">
                <div class="universia-header">
                    <div class="universia-title">
                        <i class="fas fa-robot"></i> UniversIA
                    </div>
                    <button class="universia-close" id="universia-close-btn">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="universia-messages" id="universia-messages">
                    <!-- Mensajes se cargarán aquí -->
                    <div class="uv-message model">
                        ¡Hola! Soy UniversIA. ¿En qué puedo ayudarte con tus estudios hoy?
                    </div>
                </div>
                <div class="universia-input-area">
                    <textarea id="universia-input" placeholder="Escribe tu duda..." rows="1"></textarea>
                    <button id="universia-send">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
            </div>
            <button id="universia-launcher">
                <i class="fas fa-comment-dots"></i>
            </button>
        `;
    }

    const launcher = document.getElementById('universia-launcher');
    if (!launcher) return; // Si no hay widget, salir.

    const windowEl = document.getElementById('universia-window');
    const closeBtn = document.getElementById('universia-close-btn');
    const messagesContainer = document.getElementById('universia-messages');
    const input = document.getElementById('universia-input');
    const sendBtn = document.getElementById('universia-send');

    let isHistoryLoaded = false;
    let isRequestPending = false;

    // --- Funciones de Interfaz ---

    function toggleChat() {
        windowEl.classList.toggle('active');
        if (windowEl.classList.contains('active')) {
            input.focus();
            if (!isHistoryLoaded) {
                loadHistory();
            }
            scrollToBottom();
        }
    }

    function scrollToBottom() {
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }

    function addMessage(text, role) {
        if (!messagesContainer) return;
        const msgDiv = document.createElement('div');
        msgDiv.className = `uv-message ${role}`;
        
        // msgDiv.textContent = text; 
                // Render HTML content (Markdown processed by server)
        msgDiv.innerHTML = text;
        
        messagesContainer.appendChild(msgDiv);
        scrollToBottom();
    }

    function showTyping() {
        if (!messagesContainer) return;
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = 'uv-typing';
        typingDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        messagesContainer.appendChild(typingDiv);
        scrollToBottom();
    }

    function removeTyping() {
        const typingIndicator = document.getElementById('uv-typing');
        if (typingIndicator) typingIndicator.remove();
    }

    // --- Funciones de API ---

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    async function loadHistory() {
        try {
            const response = await fetch('/universia/api/history/');
            const data = await response.json();
            
            if (data.messages && data.messages.length > 0 && messagesContainer) {
                messagesContainer.innerHTML = ''; 
                data.messages.forEach(msg => {
                    const role = msg.role === 'model' ? 'model' : 'user';
                    addMessage(msg.content, role);
                });
            }
            isHistoryLoaded = true;
        } catch (error) {
            console.error('Error cargando historial UniversIA:', error);
        }
    }

    async function sendMessage() {
        if (!input) return;
        const text = input.value.trim();
        if (!text || isRequestPending) return;

        // UI Updates
        addMessage(text, 'user');
        input.value = '';
        input.style.height = '40px'; 
        showTyping();
        isRequestPending = true;
        sendBtn.disabled = true;

        try {
            const contextUrl = window.location.href; 
            const response = await fetch('/universia/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    message: text,
                    context_url: contextUrl,
                    context_title: currentContentTitle
                })
            });

            const data = await response.json();
            removeTyping();

            if (data.status === 'success') {
                addMessage(data.response, 'model');
            } else {
                addMessage('Lo siento, ocurrió un error: ' + (data.error || 'Desconocido'), 'model');
            }

        } catch (error) {
            removeTyping();
            addMessage('Error de conexión. Por favor, inténtalo de nuevo.', 'model');
            console.error('Error enviando mensaje a UniversIA:', error);
        } finally {
            isRequestPending = false;
            sendBtn.disabled = false;
            input.focus();
        }
    }

    // --- Event Listeners ---

    if (launcher) launcher.addEventListener('click', toggleChat);
    if (closeBtn) closeBtn.addEventListener('click', toggleChat);
    if (sendBtn) sendBtn.addEventListener('click', sendMessage);

    if (input) {
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        input.addEventListener('input', function() {
            this.style.height = '40px';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }
});
