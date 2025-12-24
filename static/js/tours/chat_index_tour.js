
// /home/MiguelAeTxio/CampuStudiOnline/static/js/tours/chat_index_tour.js
// Tour for the main chat rooms index page (UPDATED).

document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'chatIndex';
    if (window.activeTours && window.activeTours[tourId]) {
        return; 
    }
    console.log(`[TourLoader] Loading tour definition: ${tourId}`);

    const allSteps = [
        {
            id: 'step-welcome',
            title: 'Salas de Chat',
            text: 'Bienvenido a tus comunidades de aprendizaje. Aquí encontrarás todas las salas de chat a las que tienes acceso.',
            attachTo: { element: '#tour-chat-index-title', on: 'bottom' }
        },
        {
            id: 'step-global',
            title: 'Comunidad Global',
            text: 'Estas son las salas abiertas a toda la plataforma. Únete para charlar con estudiantes de todas las disciplinas.',
            attachTo: { element: '#tour-chat-global', on: 'top' }
        },
        {
            id: 'step-academic',
            title: 'Tus Asignaturas',
            text: 'Aquí aparecen automáticamente las salas de chat de las asignaturas que estás estudiando (de las que has creado una copia).',
            attachTo: { element: '#tour-chat-academic', on: 'top' }
        },
        {
            id: 'step-interests',
            title: 'Tus Intereses',
            text: 'Estas salas corresponden a los temas de contenido libre que estás explorando. Se activan cuando copias material libre.',
            attachTo: { element: '#tour-chat-interests', on: 'top' }
        }
    ];

    const finalSteps = allSteps.filter(step => step && step.attachTo && document.querySelector(step.attachTo.element));

    if (finalSteps.length > 1) {
        const tour = initializeTour({
            tourId: tourId,
            steps: finalSteps
        });
        if (tour) {
            startTour(tour, tourId, 'start-chat-index-tour-btn');
        }
    }
});
