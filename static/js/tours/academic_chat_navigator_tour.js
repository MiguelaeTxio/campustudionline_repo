// /home/MiguelAeTxio/CampuStudiOnline/static/js/tours/academic_chat_navigator_tour.js
// Tour for the Academic Chat Navigator page

document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'academicChatNavigator';
    if (window.activeTours && window.activeTours[tourId]) {
        return; // Avoid reinitialization
    }
    console.log(`[TourLoader] Loading tour definition: ${tourId}`);

    const allPossibleSteps = [
        {
            id: 'step-welcome',
            title: '¡Bienvenido al Navegador de Chats!',
            text: 'Esta sección te permite navegar de forma jerárquica hasta encontrar las salas de chat disponibles para las asignaturas en las que te has matriculado.',
            attachTo: { element: '#academic-chat-navigator-title', on: 'bottom' }
        },
        {
            id: 'step-navigation',
            title: 'Navegación por Niveles',
            text: 'La exploración comienza aquí. Selecciona una opción de la lista para profundizar en la estructura académica.',
            attachTo: { element: '#navigator-options-list', on: 'top' }
        },
        {
            id: 'step-cta',
            title: 'Inicia tu Navegación',
            text: 'Por ejemplo, al hacer clic aquí, avanzarás al siguiente nivel. ¡Continúa hasta encontrar tus salas de chat!',
            attachTo: { element: '#first-navigator-option', on: 'bottom' }
        },
        {
            id: 'step-final',
            title: 'Salas de Chat',
            text: 'Cuando llegues al último nivel, verás una lista de las salas de chat a las que tienes acceso. ¡Haz clic para entrar y participar!',
            attachTo: { element: '#academic-chat-list-container', on: 'top' }
        },
        {
            id: 'step-no-chats',
            title: 'Sin Salas de Chat',
            text: 'Si ves este mensaje, significa que no tienes acceso a ninguna sala de chat en esta sección. Asegúrate de estar matriculado en las asignaturas correctas.',
            attachTo: { element: '#no-academic-chats-message', on: 'top' }
        }
    ];

    // Filter steps to ensure their anchor elements exist in the DOM
    const finalSteps = allPossibleSteps.filter(step => {
        if (!step.attachTo || !step.attachTo.element) {
            return true;
        }
        return document.querySelector(step.attachTo.element);
    });

    if (finalSteps.length > 1) {
        const tour = initializeTour({
            tourId: tourId,
            steps: finalSteps
        });
        if (tour) {
            // APPLY HYBRID PATTERN WITH STANDARDIZED ID
            startTour(tour, tourId, 'start-academic-chat-tour-btn');
        }
    } else {
         console.log(`[TourLoader] Tour "${tourId}" will not be started because there are not enough elements in the DOM.`);
    }
});
