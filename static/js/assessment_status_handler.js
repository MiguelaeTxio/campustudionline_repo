document.addEventListener('DOMContentLoaded', function() {
    const panelContainer = document.getElementById('assessment-panel-container');
    if (!panelContainer) return;

    let pollingInterval = null;
    let countdownIntervals = []; // From a variable to an array for multiple timers

    function stopPolling() {
        if (pollingInterval) {
            clearInterval(pollingInterval);
            pollingInterval = null;
        }
    }

    // Modified to clear all stored intervals
    function stopCountdown() {
        countdownIntervals.forEach(intervalId => clearInterval(intervalId));
        countdownIntervals = [];
    }

    function updatePanel(html) {
        stopPolling();
        stopCountdown();
        panelContainer.innerHTML = html;
        initializePanel();
    }

    function initializePanel() {
        const panel = document.getElementById('assessment-panel');
        if (!panel) return;

        // --- START OF TIMER REFACTORING ---

        // We stop any previous timer to prevent memory leaks.
        stopCountdown();

        // We search for all timer elements by their class.
        const timerElements = document.querySelectorAll('.assessment-timer');

        // We iterate over each found timer element.
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
                        // If a timer reaches zero, we stop all and update the entire panel.
                        stopCountdown();
                        fetchPanelUpdate();
                    }
                };

                // We create an interval for this specific timer and save its ID.
                const intervalId = setInterval(updateCountdown, 1000);
                countdownIntervals.push(intervalId);
                updateCountdown(); // Initial call so there is no one-second delay.
            }
        });
        // --- END OF TIMER REFACTORING ---


        // Start polling if the state requires it (existing logic unchanged)
        const config = window.assessmentPollingConfig;
        if (config && config.statusUrl) {
            const checkStatus = () => {
                fetch(config.statusUrl)
                    .then(response => response.json())
                    .then(data => {
                        const finalStates = ['COMPLETED', 'FAILED', 'TIMEOUT_FAILURE', 'USER_CANCELLED', 'CORRECTION_COMPLETED', 'RESULTS_AVAILABLE'];
                        if (finalStates.includes(data.status)) {
                            stopPolling();
                            fetchPanelUpdate();
                        }
                    })
                    .catch(error => {
                        console.error('Error durante el polling de estado:', error);
                        stopPolling();
                    });
            };
            stopPolling();
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
    
    // Initialization on page load
    initializePanel();
});
