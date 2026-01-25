/**
 * assessment_media_utils.js
 * v5.0 - UNIFIED PREMIUM INTERFACE (MP3 ONLY)
 * Motor nativo HTML5. Soporte para UI de 45px y ondas dinámicas.
 */

const AssessmentMedia = {
    config: { maxDuration: 120, detectedLang: 'es-ES' },

    init: function(title) {
        this.detectLanguage(title);
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();
        console.log("AssessmentMedia v5.0 Ready.");
    },

    detectLanguage: function(title) {
        if (!title) return;
        const lower = title.toLowerCase();
        const map = {
            'francés': 'fr-FR', 'français': 'fr-FR', 'inglés': 'en-US', 'english': 'en-US',
            'alemán': 'de-DE', 'german': 'de-DE', 'italiano': 'it-IT', 'portugués': 'pt-PT',
            'chino': 'zh-CN', 'japonés': 'ja-JP', 'ruso': 'ru-RU'
        };
        for (let key in map) { if (lower.includes(key)) { this.config.detectedLang = map[key]; return; } }
    },

    player: {
        audioObj: null, currentId: null,
        toggle: function(url, id) {
            if (!url) return;
            if (this.currentId === id && this.audioObj) {
                if (this.audioObj.paused) { this.audioObj.play(); this.updateUI(id, 'playing'); }
                else { this.audioObj.pause(); this.updateUI(id, 'paused'); }
                return;
            }
            this.stopAll();
            this.currentId = id;
            this.audioObj = new Audio(url);
            this.audioObj.onplay = () => { 
                this.updateUI(id, 'playing'); 
                AssessmentMedia.ui.toggleWave(id, 'tts', 'show'); 
            };
            this.audioObj.onpause = () => { 
                this.updateUI(id, 'paused'); 
                AssessmentMedia.ui.toggleWave(id, 'tts', 'pause'); 
            };
            this.audioObj.onended = () => { 
                this.updateUI(id, 'idle'); 
                AssessmentMedia.ui.toggleWave(id, 'tts', 'hide'); 
                this.currentId = null; 
            };
            this.audioObj.play();
        },
        stopAll: function() {
            if (this.audioObj) { this.audioObj.pause(); this.audioObj = null; }
            if (this.currentId) { this.updateUI(this.currentId, 'idle'); AssessmentMedia.ui.toggleWave(this.currentId, 'tts', 'hide'); }
        },
        updateUI: function(id, state) {
            const btn = document.getElementById(`btn_tts_${id}`);
            if (!btn) return;
            const icon = btn.querySelector('i');
            const baseClass = "btn rounded-circle shadow-sm d-flex align-items-center justify-content-center btn-media-45";
            if (state === 'playing') {
                icon.className = 'fas fa-pause';
                btn.className = `${baseClass} btn-primary`;
            } else if (state === 'paused') {
                icon.className = 'fas fa-play';
                btn.className = `${baseClass} btn-primary`;
            } else {
                icon.className = 'fas fa-play';
                btn.className = `${baseClass} btn-outline-primary`;
            }
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
            } else if (state === 'pause') {
                wave.classList.add('paused');
            }
        }
    },

    recorder: {
        mediaRecorder: null, audioChunks: [], interval: null,
        start: async function(qId) {
            const timerEl = document.getElementById(`timer_${qId}`);
            const btnRec = document.getElementById(`btn_rec_${qId}`);
            const btnStop = document.getElementById(`btn_stop_${qId}`);
            const statusEl = document.getElementById(`status_${qId}`);
            try {
                AssessmentMedia.player.stopAll();
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                this.mediaRecorder = new MediaRecorder(stream);
                this.audioChunks = [];
                this.mediaRecorder.ondataavailable = e => this.audioChunks.push(e.data);
                this.mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(this.audioChunks, { type: 'audio/mpeg' });
                    const file = new File([audioBlob], `oral_${qId}.mp3`, { type: 'audio/mpeg' });
                    const container = new DataTransfer(); container.items.add(file);
                    document.getElementById(`audio_input_${qId}`).files = container.files;
                    statusEl.innerHTML = "<span class='text-success small fw-bold'><i class='fas fa-check-circle'></i> AUDIO LISTO</span>";
                    btnRec.className = 'btn btn-outline-danger btn-media-45 shadow-sm';
                    btnRec.disabled = false; btnStop.disabled = true;
                    AssessmentMedia.ui.toggleWave(qId, 'rec', 'hide');
                    clearInterval(this.interval);
                    stream.getTracks().forEach(t => t.stop());
                };
                this.mediaRecorder.start();
                statusEl.innerHTML = '<span class="text-danger small fw-bold blink-text">● GRABANDO</span>';
                AssessmentMedia.ui.toggleWave(qId, 'rec', 'show');
                btnRec.className = 'btn btn-danger text-white btn-media-45 shadow-sm';
                btnRec.disabled = true; btnStop.disabled = false;
                let timeLeft = 120;
                this.interval = setInterval(() => {
                    timeLeft--;
                    timerEl.innerText = `${Math.floor(timeLeft/60).toString().padStart(2,'0')}:${(timeLeft%60).toString().padStart(2,'0')}`;
                    if (timeLeft <= 0) this.stop(qId);
                }, 1000);
            } catch (err) { alert("Error de micrófono."); }
        },
        stop: function(qId) { if (this.mediaRecorder) this.mediaRecorder.stop(); }
    }
};
