// /home/MiguelAeTxio/CampuStudiOnline/static/js/shepherd_helpers.js
// ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'

/**
 * Genera una configuración de botones estándar para un paso de Shepherd.js.
 * @param {number} stepIndex - El índice del paso actual (base 0).
 * @param {number} totalSteps - El número total de pasos en el tour.
 * @param {Shepherd.Tour} tourInstance - La instancia del tour.
 * @returns {Array<object>} Un array de objetos de configuración de botones.
 */
function getShepherdButtonConfig(stepIndex, totalSteps, tourInstance) {
    const buttons = [];

    // El botón 'Atrás' solo aparece si no es el primer paso (índice 0)
    if (stepIndex > 0) {
        buttons.push({
            text: 'Atrás',
            action: tourInstance.back,
            secondary: true
        });
    }

    // El botón 'Siguiente' aparece en todos los pasos excepto en el último
    if (stepIndex < totalSteps - 1) {
        buttons.push({
            text: 'Siguiente',
            action: tourInstance.next
        });
    }

    // El botón 'Finalizar' solo aparece en el último paso
    if (stepIndex === totalSteps - 1) {
        buttons.push({
            text: 'Finalizar',
            action: tourInstance.complete
        });
    }

    return buttons;
}

/**
 * Centraliza la creación y configuración de un tour de Shepherd.js.
 * @param {object} config - Objeto de configuración del tour.
 * @param {string} config.tourId - Un identificador único para el tour (usado para localStorage).
 * @param {Array<object>} config.steps - Un array con los pasos del tour.
 * @returns {Shepherd.Tour | null} La instancia del tour creada o null si falta configuración.
 */
function initializeTour(config) {
    if (!config || !config.tourId || !config.steps) {
        console.error('[ShepherdHelper] La configuración del tour es inválida. Se requiere tourId y steps.');
        return null;
    }

    // Evitar inicializar el mismo tour dos veces
    if (window.activeTours && window.activeTours[config.tourId]) {
        return window.activeTours[config.tourId];
    }

    const tour = new Shepherd.Tour({
        useModalOverlay: true,
        defaultStepOptions: {
            cancelIcon: { enabled: true },
            classes: 'shepherd-theme-arrows shadow-lg',
            scrollTo: { behavior: 'smooth', block: 'center' }
        }
    });

    const totalSteps = config.steps.length;
    config.steps.forEach((step, index) => {
        if (!step.buttons) {
            step.buttons = getShepherdButtonConfig(index, totalSteps, tour);
        }
        tour.addStep(step);
    });

    const tourKey = `${config.tourId}Completed`;
    tour.on('complete', () => localStorage.setItem(tourKey, 'true'));
    tour.on('cancel', () => localStorage.setItem(tourKey, 'true'));

    if (!window.activeTours) {
        window.activeTours = {};
    }
    window.activeTours[config.tourId] = tour;
    
    console.log(`[ShepherdHelper] Tour "${config.tourId}" inicializado con ${totalSteps} pasos.`);

    return tour;
}

/**
 * Gestiona la lógica de inicio de un tour (manual o automático).
 * @param {Shepherd.Tour} tour - La instancia del tour a iniciar.
 * @param {string} tourId - El identificador único del tour.
 * @param {string} [buttonId] - El ID opcional del botón que inicia el tour manualmente.
 */
function startTour(tour, tourId, buttonId) {
    if (!tour || !tourId) {
        console.error('[ShepherdHelper] No se puede iniciar el tour. Faltan la instancia o el tourId.');
        return;
    }

    const tourKey = `${tourId}Completed`;

    if (buttonId) {
        const startTourBtn = document.getElementById(buttonId);
        if (startTourBtn) {
            startTourBtn.addEventListener('click', (e) => {
                e.preventDefault();
                console.log(`[ShepherdHelper] Iniciando tour "${tourId}" manualmente.`);
                if (!tour.isActive()) {
                    tour.start();
                }
            });
        }
    }
    
    // Si hay un parámetro en la URL para forzar el inicio, lo priorizamos
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('start_tour') && urlParams.get('start_tour') === tourId) {
        console.log(`[ShepherdHelper] Forzando inicio del tour "${tourId}" desde URL.`);
        setTimeout(() => {
            if (!tour.isActive()) { tour.start(); }
            // Opcional: limpiar la URL
            // window.history.replaceState({}, document.title, window.location.pathname);
        }, 500);
        return;
    }
    
    // Inicio automático si no se ha completado antes
    if (!localStorage.getItem(tourKey)) {
        console.log(`[ShepherdHelper] Iniciando tour "${tourId}" automáticamente.`);
        setTimeout(() => {
            if (!tour.isActive()) {
                tour.start();
            }
        }, 500);
    } else {
        console.log(`[ShepherdHelper] El tour "${tourId}" ya ha sido completado anteriormente.`);
    }
}