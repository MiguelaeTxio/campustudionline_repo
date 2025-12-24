// /home/MiguelAeTxio/CampuStudiOnline/static/js/tours/study_room_directory_tour.js
// Tour for the user's study room directory.

document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'studyRoomDirectory';
    if (window.activeTours && window.activeTours[tourId]) {
        return; // Avoid reinitialization
    }
    console.log(`[TourLoader] Loading tour definition: ${tourId}`);

    const baseSteps = [
        {
            id: 'step-welcome',
            title: 'Tu Sala de Estudio',
            text: 'Este es el directorio de tu Sala de Estudio. Aquí se organizan todas las copias de materiales que has decidido estudiar, permitiéndote añadir tus propias anotaciones.',
            attachTo: { element: '#tour-sala-estudio-dir-title', on: 'bottom' }
        },
        {
            id: 'step-breadcrumbs',
            title: 'Navegación Jerárquica',
            text: 'Usa estas "migas de pan" para volver fácilmente a los niveles superiores de tu directorio de estudio.',
            attachTo: { element: '#tour-sala-estudio-dir-breadcrumbs', on: 'bottom' }
        }
    ];

    const finalStep = {
        id: 'step-explore',
        title: '¡Explora y Estudia!',
        text: 'Ahora ya sabes cómo moverte. ¡Haz clic en las carpetas para profundizar y en las copias para empezar a estudiar y tomar apuntes!',
        attachTo: { element: '#tour-sala-estudio-dir-list', on: 'top' }
    };
    
    let contextSteps = [];
    const listElement = document.getElementById('tour-sala-estudio-dir-list');

    if (listElement) {
        // Detect if we are in the copies list (last level)
        if (listElement.querySelector('.list-group-item.flex-column')) {
            contextSteps.push({
                id: 'step-copies',
                title: 'Tus Copias de Estudio',
                text: 'Estas son tus copias personales de los materiales. Haz clic para entrar a la sala de edición, donde podrás subrayar, tomar notas y generar autoevaluaciones.',
                attachTo: { element: '#tour-sala-estudio-dir-list', on: 'top' }
            });
        // Detect if we are at a folder level (areas or disciplines)
        } else if (listElement.querySelector('.list-group-item.list-group-item-action')) {
             contextSteps.push({
                id: 'step-folders',
                title: 'Navegación por Carpetas',
                text: 'Esto es una carpeta que organiza tus copias. Haz clic para entrar y ver las subcarpetas o las copias que contiene.',
                attachTo: { element: '#tour-sala-estudio-dir-list', on: 'top' }
            });
        }
    }
    
    let allSteps = [];
    // Only add breadcrumbs if they exist on the page
    if (document.getElementById('tour-sala-estudio-dir-breadcrumbs')) {
        allSteps.push(...baseSteps);
    } else {
        // If no breadcrumbs, just show the welcome step
        allSteps.push(baseSteps[0]);
    }
    
    allSteps.push(...contextSteps, finalStep);

    // Filter steps whose elements do not exist in the DOM
    const finalSteps = allSteps.filter(step => step && step.attachTo && document.querySelector(step.attachTo.element));

    if (finalSteps.length > 1) { // Only start tour if there are at least 2 valid steps
        const tour = initializeTour({
            tourId: tourId,
            steps: finalSteps
        });
        if (tour) {
            startTour(tour, tourId, 'start-study-room-directory-tour-btn');
        }
    } else {
        console.log(`[TourLoader] Tour "${tourId}" will not be started because there are not enough guide elements in the DOM.`);
    }
});
