// /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/static/js/assessment_status_handler.js
/**
 * Assessment Status Handler v2.1 (HITO 6)
 * Gestión de paneles pasivos (Dashboards, Listas de espera).
 * NO interfiere con la lógica activa de 'exam_take.html'.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Guard Clause: Solo se ejecuta si existe el contenedor del panel (Dashboard)
    const panelContainer = document.getElementById('assessment-panel-container');
    if (!panelContainer) return;

    let pollingInterval = null;
    let countdownIntervals = [];

    function stopPolling() {
        if (pollingInterval) {
            clearInterval(pollingInterval);
            pollingInterval = null;
        }
    }

    function stopCountdowns() {
        countdownIntervals.forEach(intervalId => clearInterval(intervalId));
        countdownIntervals = [];
    }

    function updatePanel(html) {
        stopPolling();
        stopCountdowns();
        panelContainer.innerHTML = html;
        initializePanel();
    }

    function initializePanel() {
        const panel = document.getElementById('assessment-panel');
        if (!panel) return;

        // Limpiar temporizadores previos para evitar fugas de memoria
        stopCountdowns();

        // Buscar temporizadores pasivos (ej: tiempo restante para desbloqueo de cuota)
        const timerElements = document.querySelectorAll('.assessment-timer');

        timerElements.forEach(timerElement => {
            if (timerElement.dataset.endTime) {
                const endTime = new Date(timerElement.dataset.endTime);

                const updateCountdown = () => {
                    const now = new Date();
                    const remainingSeconds = Math.round((endTime - now) / 1000);

                    if (remainingSeconds > 0) {
                        const hours = Math.floor(remainingSeconds / 3600).toString().padStart(2, '0');
                        const minutes = Math.floor((remainingSeconds % 3600) / 60).toString().padStart(2, '0');
                        const seconds = (remainingSeconds % 60).toString().padStart(2, '0');
                        timerElement.textContent = `${hours}:${minutes}:${seconds}`;
                    } else {
                        // Si un contador llega a cero, refrescamos el panel para actualizar estados
                        stopCountdowns();
                        fetchPanelUpdate();
                    }
                };

                const intervalId = setInterval(updateCountdown, 1000);
                countdownIntervals.push(intervalId);
                updateCountdown(); 
            }
        });

        // Configuración de Polling para actualizaciones de estado asíncronas
        const config = window.assessmentPollingConfig;
        if (config && config.statusUrl) {
            const checkStatus = () => {
                fetch(config.statusUrl)
                    .then(response => response.json())
                    .then(data => {
                        const finalStates = ['COMPLETED', 'FAILED', 'TIMEOUT_FAILURE', 'USER_CANCELLED', 'CORRECTION_COMPLETED', 'RESULTS_AVAILABLE', 'READY'];
                        
                        // Si el estado cambia a uno final o listo, actualizamos la UI
                        if (finalStates.includes(data.status)) {
                            stopPolling();
                            fetchPanelUpdate();
                        }
                    })
                    .catch(error => {
                        console.error('Error durante el polling de estado:', error);
                        // En caso de error persistente, detenemos para no saturar
                        stopPolling();
                    });
            };
            
            stopPolling();
            // Intervalo de 5 segundos para no sobrecargar el servidor
            pollingInterval = setInterval(checkStatus, 5000);
            checkStatus();
        }
    }

    function fetchPanelUpdate() {
        const config = window.assessmentPollingConfig;
        if (config && config.panelUpdateUrl) {
            fetch(config.panelUpdateUrl)
                .then(response => response.json())
                .then(data => {
                    if (data.html) {
                        updatePanel(data.html);
                    }
                })
                .catch(error => console.error('Error al actualizar el panel:', error));
        }
    }
    
    // Inicialización
    initializePanel();
});
