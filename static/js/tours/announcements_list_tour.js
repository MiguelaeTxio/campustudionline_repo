// /home/MiguelAeTxio/CampuStudiOnline/static/js/tours/announcements_list_tour.js
document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'announcementsList';
    if (window.activeTours && window.activeTours[tourId]) {
        return; // Avoid reinitialization
    }
    console.log(`[TourLoader] Loading tour definition: ${tourId}`);

    const allSteps = [
        {
            id: 'step-welcome',
            title: 'Tablón de Anuncios',
            text: '¡Bienvenido/a al Tablón de Anuncios! Este es el espacio central para comunicados, noticias y eventos de la comunidad.',
            attachTo: { element: '#tour-announcements-title', on: 'bottom' }
        },
        {
            id: 'step-list',
            title: 'Lista de Anuncios',
            text: 'Aquí verás todos los anuncios publicados, desde el más reciente al más antiguo. ¡Échales un vistazo para no perderte nada!',
            attachTo: { element: '#tour-announcements-list', on: 'top' }
        },
        {
            id: 'step-create',
            title: '¡Participa!',
            text: 'Si quieres compartir algo con la comunidad, puedes publicar tu propio anuncio haciendo clic aquí.',
            attachTo: { element: '#tour-announcements-btn-create', on: 'bottom' }
        }
    ];

    // Filter steps whose elements do not exist in the DOM.
    // This makes the 'step-create' optional (only for authenticated users).
    const finalSteps = allSteps.filter(step => step && step.attachTo && document.querySelector(step.attachTo.element));

    if (finalSteps.length > 1) { // Only start the tour if there are at least 2 valid steps
        const tour = initializeTour({
            tourId: tourId,
            steps: finalSteps
        });
        if (tour) {
            startTour(tour, tourId, 'start-announcements-list-tour-btn');
        }
    } else {
        console.log(`[TourLoader] Tour "${tourId}" will not be started because there are not enough guide elements in the DOM.`);
    }
});
