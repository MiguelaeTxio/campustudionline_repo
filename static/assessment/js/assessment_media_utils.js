/**
 * AssessmentMediaUtils v2.0 (HITO 6)
 * Gestión de widgets multimedia estilo "Cassette" y previsualización de archivos.
 */

const AssessmentMedia = {
    player: {
        currentAudio: null,
        currentBtnId: null,
        
        toggle: function(url, questionId) {
            const btn = document.getElementById(`btn_tts_${questionId}`);
            const wave = document.getElementById(`wave_tts_${questionId}`);
            
            // Si ya hay un audio sonando y es el mismo
            if (this.currentAudio && this.currentBtnId === questionId) {
                if (this.currentAudio.paused) {
                    this.currentAudio.play();
                    this._setPlayingState(btn, wave, true);
                } else {
                    this.currentAudio.pause();
                    this._setPlayingState(btn, wave, false);
                }
                return;
            }

            // Si hay otro audio sonando, pararlo
            if (this.currentAudio) {
                this.currentAudio.pause();
                this.currentAudio.currentTime = 0;
                // Reset UI del anterior
                if (this.currentBtnId) {
                    const prevBtn = document.getElementById(`btn_tts_${this.currentBtnId}`);
                    const prevWave = document.getElementById(`wave_tts_${this.currentBtnId}`);
                    this._setPlayingState(prevBtn, prevWave, false, true);
                }
            }

            // Nuevo audio
            this.currentAudio = new Audio(url);
            this.currentBtnId = questionId;

            this.currentAudio.addEventListener('ended', () => {
                this._setPlayingState(btn, wave, false, true);
                this.currentAudio = null;
                this.currentBtnId = null;
            });

            this.currentAudio.play().catch(e => console.error("Error playing audio:", e));
            this._setPlayingState(btn, wave, true);
        },

        _setPlayingState: function(btn, wave, isPlaying, isReset=false) {
            if (!btn) return;
            if (isReset) {
                btn.innerHTML = '<i class="fas fa-play"></i>';
                btn.classList.remove('btn-primary');
                btn.classList.add('btn-outline-primary');
                if (wave) wave.classList.add('d-none');
            } else if (isPlaying) {
                btn.innerHTML = '<i class="fas fa-pause"></i>';
                btn.classList.remove('btn-outline-primary');
                btn.classList.add('btn-primary');
                if (wave) wave.classList.remove('d-none');
            } else {
                // Paused state
                btn.innerHTML = '<i class="fas fa-play"></i>';
                if (wave) wave.classList.add('d-none');
            }
        }
    },

    recorder: {
        mediaRecorder: null,
        chunks: [],
        currentQuestionId: null,
        timerInterval: null,

        start: async function(questionId) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                this.mediaRecorder = new MediaRecorder(stream);
                this.chunks = [];
                this.currentQuestionId = questionId;

                const btnRec = document.getElementById(`btn_rec_${questionId}`);
                const btnStop = document.getElementById(`btn_stop_${questionId}`);
                const wave = document.getElementById(`wave_rec_${questionId}`);
                const status = document.getElementById(`status_${questionId}`);

                this.mediaRecorder.ondataavailable = (e) => {
                    if (e.data.size > 0) this.chunks.push(e.data);
                };

                this.mediaRecorder.onstop = () => {
                    const blob = new Blob(this.chunks, { type: 'audio/mp3' }); // Nota: WebM en realidad, pero renombramos
                    const fileInput = document.getElementById(`audio_input_${questionId}`);
                    
                    // Crear archivo para el input
                    const file = new File([blob], `recording_q${questionId}.mp3`, { type: 'audio/mpeg' });
                    const container = new DataTransfer();
                    container.items.add(file);
                    fileInput.files = container.files;

                    // Stop stream tracks
                    stream.getTracks().forEach(track => track.stop());
                    
                    // UI Update
                    status.innerHTML = '<span class="text-success"><i class="fas fa-check"></i> Grabación guardada</span>';
                    btnRec.disabled = false;
                    btnStop.disabled = true;
                    if (wave) wave.classList.add('d-none');
                    this._stopTimer(questionId);
                };

                this.mediaRecorder.start();

                // UI Update
                btnRec.disabled = true;
                btnStop.disabled = false;
                if (wave) wave.classList.remove('d-none');
                status.innerHTML = '<span class="text-danger blink-text">● GRABANDO...</span>';
                this._startTimer(questionId);

            } catch (err) {
                console.error("Error accessing microphone:", err);
                alert("No se pudo acceder al micrófono. Por favor, verifica los permisos.");
            }
        },

        stop: function(questionId) {
            if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
                this.mediaRecorder.stop();
            }
        },

        _startTimer: function(questionId) {
            let seconds = 0;
            const timerBadge = document.getElementById(`timer_${questionId}`);
            this.timerInterval = setInterval(() => {
                seconds++;
                const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
                const secs = (seconds % 60).toString().padStart(2, '0');
                timerBadge.innerText = `${mins}:${secs}`;
                // Límite duro de 5 minutos
                if (seconds >= 300) this.stop(questionId);
            }, 1000);
        },

        _stopTimer: function(questionId) {
            clearInterval(this.timerInterval);
        }
    },

    ui: {
        updateUpload: function(input, questionId) {
            const preview = document.getElementById(`file_preview_${questionId}`);
            const fileName = document.getElementById(`file_name_${questionId}`);
            if (input.files && input.files[0]) {
                fileName.innerText = input.files[0].name;
                preview.classList.remove('d-none');
            } else {
                preview.classList.add('d-none');
            }
        }
    },

    init: function(contextName) {
        console.log(`AssessmentMedia initialized for: ${contextName}`);
    }
};
