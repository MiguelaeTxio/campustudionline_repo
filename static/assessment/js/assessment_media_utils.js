/**
 * assessment_media_utils.js
 * Utilidades unificadas para TTS y Grabación de Audio en Evaluaciones.
 * Soporta: SpeechSynthesis API y MediaRecorder API.
 */

const AssessmentMedia = {
    // --- CONFIGURACIÓN ---
    config: {
        maxDuration: 120, // Segundos
        detectedLang: 'es-ES' // Por defecto
    },

    // --- INICIALIZACIÓN ---
    init: function(contentTitle) {
        this.detectLanguage(contentTitle);
        console.log("AssessmentMedia inicializado. Idioma TTS:", this.config.detectedLang);
    },

    detectLanguage: function(title) {
        if (!title) return;
        if (title.match(/Francés|Français|French/i)) this.config.detectedLang = 'fr-FR';
        else if (title.match(/Inglés|English/i)) this.config.detectedLang = 'en-US';
        else if (title.match(/Alemán|German/i)) this.config.detectedLang = 'de-DE';
        else if (title.match(/Italiano|Italian/i)) this.config.detectedLang = 'it-IT';
        else if (title.match(/Portugués|Portuguese/i)) this.config.detectedLang = 'pt-PT';
        else if (title.match(/Chino|Chinese/i)) this.config.detectedLang = 'zh-CN';
        else if (title.match(/Japonés|Japanese/i)) this.config.detectedLang = 'ja-JP';
        else if (title.match(/Ruso|Russian/i)) this.config.detectedLang = 'ru-RU';
    },

    // --- TTS CONTROLLER ---
    tts: {
        currentId: null,
        
        play: function(text, id) {
            if (!('speechSynthesis' in window)) return alert("Tu navegador no soporta audio.");
            
            // Resume si es el mismo
            if (window.speechSynthesis.paused && this.currentId === id) {
                window.speechSynthesis.resume();
                this.updateUI(id, 'Reproduciendo...', 'primary');
                return;
            }

            window.speechSynthesis.cancel();
            this.currentId = id;
            
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = AssessmentMedia.config.detectedLang;
            utterance.rate = 0.9;
            
            utterance.onend = () => {
                this.updateUI(id, 'Escuchar Audio', 'info');
                this.currentId = null;
            };
            
            utterance.onstart = () => this.updateUI(id, 'Reproduciendo...', 'warning');
            utterance.onerror = (e) => {
                console.error("TTS Error:", e);
                this.updateUI(id, 'Error', 'danger');
            };

            window.speechSynthesis.speak(utterance);
        },

        stop: function() {
            window.speechSynthesis.cancel();
            if (this.currentId) this.updateUI(this.currentId, 'Escuchar Audio', 'info');
            this.currentId = null;
        },

        updateUI: function(id, text, btnClass) {
            const btn = document.getElementById(`btn_tts_${id}`);
            if (btn) {
                btn.innerHTML = `<i class="fas fa-volume-up me-1"></i> ${text}`;
                // Reset clases
                btn.className = `btn btn-${btnClass} text-white btn-sm rounded-pill px-3 shadow-sm`;
            }
        }
    },

    // --- RECORDER CONTROLLER ---
    recorder: {
        mediaRecorder: null,
        audioChunks: [],
        interval: null,

        start: async function(qId) {
            const statusEl = document.getElementById(`status_${qId}`);
            const timerEl = document.getElementById(`timer_${qId}`);
            const btnRec = document.getElementById(`btn_rec_${qId}`);
            const btnStop = document.getElementById(`btn_stop_${qId}`);

            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                this.mediaRecorder = new MediaRecorder(stream);
                this.audioChunks = [];

                this.mediaRecorder.ondataavailable = event => this.audioChunks.push(event.data);
                
                this.mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(this.audioChunks, { type: 'audio/mpeg' });
                    const file = new File([audioBlob], `oral_response_${qId}.mp3`, { type: 'audio/mpeg' });
                    
                    // Asignar al input
                    const container = new DataTransfer();
                    container.items.add(file);
                    document.getElementById(`audio_input_${qId}`).files = container.files;
                    
                    // UI Final
                    statusEl.innerHTML = '<span class="text-success"><i class="fas fa-check-circle"></i> Grabación guardada.</span>';
                    clearInterval(this.interval);
                    
                    // Liberar stream
                    stream.getTracks().forEach(track => track.stop());
                };

                this.mediaRecorder.start();
                
                // UI Updates
                statusEl.innerText = "GRABANDO...";
                statusEl.className = "mt-3 text-center text-danger fw-bold blink";
                btnRec.disabled = true;
                btnStop.disabled = false;

                // Timer
                let timeLeft = AssessmentMedia.config.maxDuration;
                this.updateTimer(timerEl, timeLeft);
                
                this.interval = setInterval(() => {
                    timeLeft--;
                    this.updateTimer(timerEl, timeLeft);
                    if (timeLeft <= 0) this.stop(qId);
                }, 1000);

            } catch (err) {
                console.error(err);
                alert("No se pudo acceder al micrófono. Verifica permisos.");
            }
        },

        stop: function(qId) {
            if (this.mediaRecorder && this.mediaRecorder.state !== "inactive") {
                this.mediaRecorder.stop();
                document.getElementById(`btn_stop_${qId}`).disabled = true;
            }
        },

        updateTimer: function(el, seconds) {
            const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
            const secs = (seconds % 60).toString().padStart(2, '0');
            el.innerText = `${mins}:${secs}`;
        }
    }
};
