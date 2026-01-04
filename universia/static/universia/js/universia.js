document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('universia-widget-container');
    const currentContentTitle = container ? container.getAttribute('data-content-title') : null;
    
    // Inyectar HTML del widget si solo tenemos el contenedor
    if (container && !document.getElementById('universia-window')) {
        // HITO V29: Icono actualizado a fa-brain
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
                <i class="fas fa-brain"></i>
            </button>
        `;
    }

    const launcher = document.getElementById('universia-launcher');
    if (!launcher) return; 

    const windowEl = document.getElementById('universia-window');
    const closeBtn = document.getElementById('universia-close-btn');
    const messagesContainer = document.getElementById('universia-messages');
    const input = document.getElementById('universia-input');
    const sendBtn = document.getElementById('universia-send');

    let isHistoryLoaded = false;
    let isRequestPending = false;

    // --- HITO V29: Lógica de Drag & Drop ---
    // Restaurar posición guardada
    try {
        const savedPos = JSON.parse(localStorage.getItem('univ_pos'));
        if(savedPos && container) { 
            container.style.bottom='auto'; 
            container.style.right='auto'; 
            container.style.left=savedPos.x; 
            container.style.top=savedPos.y; 
        }
    } catch(e){}

    let isDrag=false, sX, sY, iL, iT;
    
    const startDrag = (e) => {
        if(e.type==='mousedown' && e.button!==0) return; // Solo click izq
        const t = e.type.includes('touch')?e.touches[0]:e;
        sX = t.clientX; 
        sY = t.clientY;
        
        // Bloquear posición absoluta actual para iniciar movimiento relativo
        const rect = container.getBoundingClientRect();
        iL = rect.left; 
        iT = rect.top;
        container.style.bottom='auto'; container.style.right='auto'; 
        container.style.left=iL+'px'; container.style.top=iT+'px';
        
        document.addEventListener(e.type==='mousedown'?'mousemove':'touchmove', onDrag, {passive:false});
        document.addEventListener(e.type==='mousedown'?'mouseup':'touchend', stopDrag);
    };

    const onDrag = (e) => {
        const t = e.type.includes('touch')?e.touches[0]:e;
        if(!isDrag && (Math.abs(t.clientX - sX) > 5 || Math.abs(t.clientY - sY) > 5)) { 
            isDrag = true; 
            launcher.classList.add('is-dragging'); 
            if(windowEl) windowEl.classList.remove('active'); // Colapsar ventana al arrastrar
        }
        if(isDrag){
            if(e.cancelable) e.preventDefault();
            const dx = t.clientX - sX;
            const dy = t.clientY - sY;
            container.style.left = (iL + dx) + 'px';
            container.style.top = (iT + dy) + 'px';
        }
    };

    const stopDrag = () => {
        document.removeEventListener('mousemove', onDrag); document.removeEventListener('touchmove', onDrag);
        document.removeEventListener('mouseup', stopDrag); document.removeEventListener('touchend', stopDrag);
        if(isDrag){
            setTimeout(()=>{ isDrag = false; launcher.classList.remove('is-dragging'); }, 50);
            localStorage.setItem('univ_pos', JSON.stringify({x:container.style.left, y:container.style.top}));
        }
    };
    
    launcher.addEventListener('mousedown', startDrag);
    launcher.addEventListener('touchstart', startDrag, {passive:false});
    
    // Interceptar clicks si se arrastró
    launcher.addEventListener('click', (e) => {
        if(isDrag){ e.stopImmediatePropagation(); e.preventDefault(); }
    }, true);


    // --- Funciones de Interfaz ---

    function toggleChat() {
        if (isDrag) return; // Seguridad extra
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
        msgDiv.innerHTML = text; // Markdown renderizado por backend
        messagesContainer.appendChild(msgDiv);
        scrollToBottom();
    }

    function showTyping() {
        if (!messagesContainer) return;
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = 'uv-typing';
        typingDiv.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
        messagesContainer.appendChild(typingDiv);
        scrollToBottom();
    }

    function removeTyping() {
        const typingIndicator = document.getElementById('uv-typing');
        if (typingIndicator) typingIndicator.remove();
    }

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
                let responseHtml = data.response;
                
                // Si hay una acción de redirección, inyectamos el botón en el HTML
                if (data.client_action && data.client_action.type === 'redirect') {
                    const actionUrl = data.client_action.url;
                    responseHtml += `
                        <div class="mt-2 text-center">
                            <a href="${actionUrl}" class="btn btn-sm btn-outline-primary" style="font-size: 0.8rem; border-radius: 20px; padding: 5px 15px;">
                                <i class="fas fa-calendar-alt"></i> Ver en la Agenda
                            </a>
                        </div>
                    `;
                }
                
                // Mostramos el mensaje (con o sin botón)
                addMessage(responseHtml, 'model');
            } else {
                addMessage('Lo siento, ocurrió un error: ' + (data.error || 'Desconocido'), 'model');
            }

        } catch (error) {
            removeTyping();
            addMessage('Error de conexión. Por favor, inténtalo de nuevo.', 'model');
            console.error('Error UniversIA:', error);
        } finally {
            isRequestPending = false;
            sendBtn.disabled = false;
            input.focus();
        }
    }

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
            
            // HITO V29: Validación de longitud máxima
            const MAX_CHARS = 500;
            if (this.value.length > MAX_CHARS) {
                this.value = this.value.substring(0, MAX_CHARS);
                // Feedback visual opcional o truncado silencioso
            }
        });

        // --- HITO V29: Hardening (Bloqueo de Pegado Masivo) ---
        input.addEventListener('paste', function(e) {
            e.preventDefault();
            alert('Por seguridad y para fomentar la síntesis, el pegado de texto está deshabilitado. Por favor, escribe tu consulta.');
        });
        
        input.addEventListener('copy', (e) => e.preventDefault());
        input.addEventListener('cut', (e) => e.preventDefault());
        input.addEventListener('dragover', (e) => e.preventDefault());
        input.addEventListener('drop', (e) => e.preventDefault());
        // Bloqueo de menú contextual para evitar bypass
        input.addEventListener('contextmenu', (e) => e.preventDefault());

    }
});
