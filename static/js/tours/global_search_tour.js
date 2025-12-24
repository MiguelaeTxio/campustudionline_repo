// /home/MiguelAeTxio/CampuStudiOnline/static/js/tours/global_search_tour.js
// Tour for the global search results page.

document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'globalSearch';
    if (window.activeTours && window.activeTours[tourId]) {
        return; // Avoid reinitialization
    }
    console.log(`[TourLoader] Loading tour definition: ${tourId}`);

    const steps = [
        {
            id: 'step-welcome',
            title: 'Resultados de Búsqueda',
            text: 'Aquí se muestran todos los resultados para tu consulta. ¡Veamos cómo funciona!',
            attachTo: { element: '#tour-results-title', on: 'bottom' }
        },
        {
            id: 'step-filters',
            title: 'Filtra tus Resultados',
            text: 'Puedes acotar tu búsqueda seleccionando los tipos de contenido que te interesan. Los resultados se actualizarán automáticamente.',
            attachTo: { element: '#tour-filters', on: 'right' }
        },
        {
            id: 'step-results-list',
            title: 'Lista de Resultados',
            text: 'Cada elemento en esta lista es un enlace directo al contenido, usuario o chat encontrado. Cada tipo de resultado tiene un icono distintivo.',
            attachTo: { element: '.list-group', on: 'top' }
        },
        {
            id: 'step-pagination',
            title: 'Navegación entre Páginas',
            text: 'Si hay muchos resultados, puedes usar estos controles para moverte entre las diferentes páginas.',
            attachTo: { element: 'nav[aria-label="Navegación de resultados"]', on: 'top' }
        }
    ];

    const resultsFound = document.querySelector('.list-group') !== null;
    if (!resultsFound) {
        console.log(`[TourLoader] Tour "${tourId}" will not be started because there are no results.`);
        return;
    }
    
    const paginationElement = document.querySelector('nav[aria-label="Navegación de resultados"]');
    const finalSteps = paginationElement ? steps : steps.filter(step => step.id !== 'step-pagination');

    const tour = initializeTour({
        tourId: tourId,
        steps: finalSteps
    });

    if (tour) {
        // APPLY HYBRID PATTERN
        startTour(tour, tourId, 'start-global-search-tour-btn');
    }
});
