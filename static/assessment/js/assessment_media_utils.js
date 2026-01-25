/**
 * assessment_media_utils.js
 * Utilidades unificadas para TTS y Grabación de Audio.
 * UI Unificada: Botones circulares 45px, Ondas visuales, Estabilidad TTS mejorada.
 */

const AssessmentMedia = {
    config: {
        maxDuration: 120,
        detectedLang: 'es-ES'
    },

    init: function(contentTitle) {
        this.detectLanguage(contentTitle);
        // Limpiar cualquier audio pendiente al cargar
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();
        console.log("AssessmentMedia inicializado:", this.config.detectedLang);
    },

    detectLanguage: function(title) {
        if (!title) return;
        const map = {
            'Francés': 'fr-FR', 'Français': 'fr-FR', 'French': 'fr-FR',
            'Inglés': 'en-US', 'English': 'en-US',
            'Alemán': 'de-DE', 'German': 'de-DE',
            'Italiano': 'it-IT', 'Italian': 'it-IT',
            'Portugués': 'pt-PT', 'Portuguese': 'pt-PT',
            'Chino': 'zh-CN', 'Chinese': 'zh-CN',
            'Japonés': 'ja-JP', 'Japanese': 'ja-JP',
            'Ruso': 'ru-RU', 'Russian': 'ru-RU'
        };
        for (let key in map) {
            if (title.includes(key)) { this.config.detectedLang = map[key]; break; }
        }
    },

    ui: {
        updateUpload: function(input, qId) {
            const preview = document.getElementById(`file_preview_${qId}`);
            const fileName = document.getElementById(`file_name_${qId}`);
            if (input.files && input.files[0]) {
                fileName.innerText = input.files[0].name;
                preview.classList.remove('d-none');
            } else {
                preview.classList.add('d-none');
            }
        },
        toggleWave: function(id, type, state) {
            const wave = document.getElementById(`wave_${type}_${id}`);
            if (!wave) return;
            
            if (state === 'show') {
                wave.classList.remove('d-none');
                wave.classList.remove('paused');
            } else if (state === 'hide') {
                wave.classList.add('d-none');
                wave.classList.remove('paused');
            } else if (state === 'pause') {
                wave.classList.add('paused');
            }
        }
    },

    tts: {
        currentId: null,
        
        play: function(text, id) {
            if (!('speechSynthesis' in window)) return alert("Audio no soportado.");
            
            // Lógica de Pausa/Reanudar
            if (window.speechSynthesis.speaking && this.currentId === id) {
                if (window.speechSynthesis.paused) {
                    window.speechSynthesis.resume();
                    this.updateUI(id, 'playing');
                    AssessmentMedia.ui.toggleWave(id, 'tts', 'show');
                } else {
                    window.speechSynthesis.pause();
                    this.updateUI(id, 'paused');
                    AssessmentMedia.ui.toggleWave(id, 'tts', 'pause');
                }
                return;
            }

            // Hard Reset: Cancelar todo antes de empezar uno nuevo para estabilidad
            window.speechSynthesis.cancel();
            
            // Timeout de seguridad para evitar condiciones de carrera en la API
            setTimeout(() => {
                this.currentId = id;
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = AssessmentMedia.config.detectedLang;
                
                utterance.onend = () => { 
                    this.updateUI(id, 'idle'); 
                    AssessmentMedia.ui.toggleWave(id, 'tts', 'hide');
                    this.currentId = null; 
                };
                
                utterance.onerror = (e) => {
                    console.error("TTS Error", e);
                    this.updateUI(id, 'idle');
                    AssessmentMedia.ui.toggleWave(id, 'tts', 'hide');
                    this.currentId = null;
                };
                
                utterance.onstart = () => {
                    this.updateUI(id, 'playing');
                    AssessmentMedia.ui.toggleWave(id, 'tts', 'show');
                };
                
                window.speechSynthesis.speak(utterance);
            }, 50);
        },
        
        updateUI: function(id, state) {
            const btn = document.getElementById(`btn_tts_${id}`);
            if (!btn) return;
            const icon = btn.querySelector('i');
            
            // Asegurar dimensiones
            btn.style.width = '45px'; btn.style.height = '45px'; btn.style.borderRadius = '50%';
            
            if (state === 'playing') {
                icon.className = 'fas fa-pause';
                btn.className = 'btn btn-primary shadow-sm d-flex align-items-center justify-content-center';
            } else if (state === 'paused') {
                icon.className = 'fas fa-play';
                btn.className = 'btn btn-primary shadow-sm d-flex align-items-center justify-content-center';
            } else {
                icon.className = 'fas fa-play';
                btn.className = 'btn btn-outline-primary shadow-sm d-flex align-items-center justify-content-center';
            }
        }
    },

    recorder: {
        mediaRecorder: null,
        audioChunks: [],
        interval: null,
        
        start: async function(qId) {
            const timerEl = document.getElementById(`timer_${qId}`);
            const btnRec = document.getElementById(`btn_rec_${qId}`);
            const btnStop = document.getElementById(`btn_stop_${qId}`);
            const playBtn = document.getElementById(`btn_play_${qId}`);
            const statusEl = document.getElementById(`status_${qId}`);
            
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                this.mediaRecorder = new MediaRecorder(stream);
                this.audioChunks = [];
                
                this.mediaRecorder.ondataavailable = e => this.audioChunks.push(e.data);
                
                this.mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(this.audioChunks, { type: 'audio/mpeg' });
                    const file = new File([audioBlob], `oral_${qId}.mp3`, { type: 'audio/mpeg' });
                    const container = new DataTransfer();
                    container.items.add(file);
                    document.getElementById(`audio_input_${qId}`).files = container.files;
                    
                    const url = URL.createObjectURL(audioBlob);
                    
                    // UI Stop
                    playBtn.classList.remove("d-none");
                    playBtn.dataset.url = url;
                    
                    statusEl.innerHTML = "<span class='text-success small'><i class='fas fa-check-circle'></i> AUDIO LISTO</span>";
                    
                    // Reset Rec button state
                    btnRec.innerHTML = '<i class="fas fa-microphone"></i>';
                    btnRec.className = 'btn btn-outline-danger shadow-sm d-flex align-items-center justify-content-center';
                    btnRec.disabled = false;
                    
                    AssessmentMedia.ui.toggleWave(qId, 'rec', 'hide');
                    clearInterval(this.interval);
                    stream.getTracks().forEach(t => t.stop());
                };
                
                this.mediaRecorder.start();
                
                // UI Start
                statusEl.innerHTML = '<span class="text-danger small fw-bold">GRABANDO...</span>';
                AssessmentMedia.ui.toggleWave(qId, 'rec', 'show');
                
                // Ocultar play si se regraba
                playBtn.classList.add("d-none");
                
                btnRec.innerHTML = '<i class="fas fa-microphone"></i>';
                btnRec.className = 'btn btn-danger text-white shadow-sm d-flex align-items-center justify-content-center';
                btnRec.disabled = true;
                btnStop.disabled = false;
                
                let timeLeft = AssessmentMedia.config.maxDuration;
                this.interval = setInterval(() => {
                    timeLeft--;
                    const mins = Math.floor(timeLeft / 60).toString().padStart(2, '0');
                    const secs = (timeLeft % 60).toString().padStart(2, '0');
                    timerEl.innerText = `${mins}:${secs}`;
                    if (timeLeft <= 0) this.stop(qId);
                }, 1000);
                
            } catch (err) { alert("Error de micrófono: " + err.message); }
        },
        
        stop: function(qId) {
            if (this.mediaRecorder && this.mediaRecorder.state !== "inactive") {
                this.mediaRecorder.stop();
                document.getElementById(`btn_stop_${qId}`).disabled = true;
            }
        },
        
        preview: function(qId) {
            const url = document.getElementById(`btn_play_${qId}`).dataset.url;
            if (url) { new Audio(url).play(); }
        }
    }
};
