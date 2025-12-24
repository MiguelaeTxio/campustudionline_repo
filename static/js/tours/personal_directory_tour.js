// /home/MiguelAeTxio/CampuStudiOnline/static/js/tours/personal_directory_tour.js
// Tour for the user's personal content directory.

document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'personalDirectory';
    if (window.activeTours && window.activeTours[tourId]) {
        return; // Avoid reinitialization
    }
    console.log(`[TourLoader] Loading tour definition: ${tourId}`);

    const baseSteps = [
        {
            id: 'step-welcome',
            title: 'Tu Directorio Personal',
            text: 'Este es tu Explorador Personal. Aquí se archivan tus publicaciones y los materiales favoritos que has copiado.',
            attachTo: { element: '#tour-dir-title', on: 'bottom' }
        },

    ];

    const finalStep = {
        id: 'step-explore',
        title: '¡Explora!',
        text: 'Ahora ya sabes cómo moverte. ¡Haz clic en las carpetas para profundizar y en los materiales para empezar a estudiar!',
        attachTo: { element: '#tour-dir-list', on: 'top' }
    };
    
    let contextSteps = [];
    const listElement = document.getElementById('tour-dir-list');

    if (listElement) {
        // Detect if we are in the materials list (last level)
        if (listElement.querySelector('.list-group-item.flex-column')) {
            contextSteps.push({
                id: 'step-materials',
                title: 'Tus Materiales de Estudio',
                text: 'Estos son los materiales que has creado o copiado. Haz clic en uno para ver su detalle o ir a tu copia en la Sala de Estudio.',
                attachTo: { element: '#tour-dir-list', on: 'top' }
            });
        // Detect if we are at a folder level
        } else if (listElement.querySelector('.list-group-item.list-group-item-action')) {
             contextSteps.push({
                id: 'step-folders',
                title: 'Navegación por Carpetas',
                text: 'Esto es una carpeta que contiene más subcarpetas o materiales. Haz clic para entrar y explorar su contenido.',
                attachTo: { element: '#tour-dir-list', on: 'top' }
            });
        }
    }
    
    let allSteps = [];
    // Only add breadcrumbs if they exist on the page
    if (document.getElementById('tour-dir-breadcrumbs')) {
        allSteps.push(...baseSteps);
    } else {
        // If no breadcrumbs, just show the welcome step
        allSteps.push(baseSteps[0]);
    }
    
    allSteps.push(...contextSteps, finalStep);

    // Filter steps whose elements do not exist
    const finalSteps = allSteps.filter(step => step && step.attachTo && document.querySelector(step.attachTo.element));

    if (finalSteps.length > 1) { // Only start tour if there are at least 2 valid steps
        const tour = initializeTour({
            tourId: tourId,
            steps: finalSteps
        });
        if (tour) {
            // APPLY HYBRID PATTERN
            startTour(tour, tourId, 'start-personal-directory-tour-btn');
        }
    } else {
        console.log(`[TourLoader] Tour "${tourId}" will not be started because there are not enough guide elements in the DOM.`);
    }
});
