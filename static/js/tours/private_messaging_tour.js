// /home/MiguelAeTxio/CampuStudiOnline/static/js/tours/private_messaging_tour.js
// Tour for the private messaging (P2P) conversation list.

document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'privateMessagingTour';
    if (window.activeTours && window.activeTours[tourId]) {
        return; // Avoid reinitialization
    }
    console.log(`[TourLoader] Loading tour definition: ${tourId}`);

    const allSteps = [
        {
            id: 'step-welcome',
            title: 'Tus Conversaciones Privadas',
            text: 'Este es tu centro de mensajería privada. Todas tus conversaciones seguras de usuario a usuario se gestionan desde aquí.',
            attachTo: { element: '#tour-pm-title', on: 'bottom' }
        },
        {
            id: 'step-search',
            title: 'Iniciar una Nueva Conversación',
            text: 'Usa este buscador para encontrar a cualquier usuario de la plataforma por su nombre o nick y empezar un nuevo chat cifrado.',
            attachTo: { element: '#tour-pm-search', on: 'bottom' }
        },
        {
            id: 'step-list',
            title: 'Lista de Chats',
            text: 'Aquí aparecerán tus conversaciones existentes. Las que tengan mensajes nuevos estarán resaltadas en azul y mostrarán un contador rojo.',
            attachTo: { element: '#tour-pm-list', on: 'top' }
        },
        {
            id: 'step-hide',
            title: 'Ocultar Conversaciones',
            text: 'Si una conversación ya no es relevante, puedes usar el botón de la papelera para ocultarla de esta lista. Esto no borrará los mensajes, solo limpiará tu vista.',
            attachTo: { element: '#tour-pm-list', on: 'top' }
        }
    ];

    // Dynamically filter steps based on elements present in the DOM
    const finalSteps = allSteps.filter(step => step && step.attachTo && document.querySelector(step.attachTo.element));

    if (finalSteps.length > 1) { // Only start if there are enough elements to guide
        const tour = initializeTour({
            tourId: tourId,
            steps: finalSteps
        });
        if (tour) {
            // APPLY HYBRID PATTERN
            startTour(tour, tourId, 'start-private-messaging-tour-btn');
        }
    } else {
        console.log(`[TourLoader] Tour "${tourId}" will not be started because there are not enough guide elements in the DOM.`);
    }
});
