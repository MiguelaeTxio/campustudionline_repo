// /home/MiguelAeTxio/CampuStudiOnline/static/js/tours/intellectual_directory_tour.js
// Tour for the intellectual directory root page.

document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'intellectualDirectory';

    if (window.activeTours && window.activeTours[tourId]) {
        return; 
    }
    console.log(`[TourLoader] Loading tour definition: ${tourId}`);
    
    const allPossibleSteps = [
        {
            id: 'step-welcome',
            title: 'El Directorio de Contenidos Libres',
            text: 'Este es el explorador principal del campus. Desde aquí puedes navegar por toda la estructura de conocimiento de la plataforma, desde las áreas más generales hasta los materiales más específicos.',
            attachTo: { element: '#directorio-title', on: 'bottom' }
        },
        {
            id: 'step-categories',
            title: 'Navegación por Categorías',
            text: 'Cada uno de estos elementos es una "Área de Conocimiento", el nivel más alto. Haz clic en una para explorar las "Disciplinas" que contiene.',
            attachTo: { element: '#first-category-item', on: 'bottom' }
        },
        {
            id: 'step-manual-start',
            title: 'Reiniciar la Visita',
            text: 'Si alguna vez quieres volver a ver esta guía, simplemente haz clic en este botón.',
            attachTo: { element: '#start-intellectual-directory-tour-btn', on: 'bottom' }
        },
        {
            id: 'step-final',
            title: '¡A Explorar!',
            text: 'Ya estás listo para navegar por el conocimiento del campus. ¡Adelante!'
        }
    ];

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
            startTour(tour, tourId, 'start-intellectual-directory-tour-btn');
        }
    } else {
         console.log(`[TourLoader] Tour "${tourId}" will not be started because there are not enough elements in the DOM.`);
    }
});
