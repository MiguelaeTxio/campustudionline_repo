// /home/MiguelAeTxio/CampuStudiOnline/static/js/tours/academic_directory_tour.js
// Tour for the public Academic Directory pages.

document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'academicDirectory';
    if (window.activeTours && window.activeTours[tourId]) {
        return; // Avoid reinitialization
    }
    console.log(`[TourLoader] Loading tour definition: ${tourId}`);

    const baseSteps = [
        {
            id: 'step-welcome',
            title: 'El Directorio Académico',
            text: 'Bienvenido al Directorio Académico. Este es un mapa público de todo el conocimiento disponible en la plataforma, organizado por universidad, titulación y asignatura.',
            attachTo: { element: '#tour-dir-title', on: 'bottom' }
        },
        {
            id: 'step-breadcrumbs',
            title: 'Navegación Jerárquica',
            text: 'Usa estas "migas de pan" para orientarte y volver fácilmente a los niveles superiores (por ejemplo, a la lista de titulaciones o universidades).',
            attachTo: { element: '#tour-dir-breadcrumbs', on: 'bottom' }
        }
    ];

    const finalStep = {
        id: 'step-explore',
        title: '¡Explora el Conocimiento!',
        text: 'Ahora ya sabes cómo moverte. ¡Haz clic en las carpetas para profundizar y descubrir todo el contenido público disponible!',
        attachTo: { element: '#tour-dir-list', on: 'top' }
    };
    
    let contextSteps = [];
    const listElement = document.getElementById('tour-dir-list');

    if (listElement) {
        // If there is a list of folders (Universities, Branches, Degrees, etc.)
        if (listElement.querySelector('.list-group-item.list-group-item-action.d-flex')) {
             contextSteps.push({
                id: 'step-folders',
                title: 'Navegación por Carpetas',
                text: 'Cada uno de estos elementos es como una carpeta. Haz clic para entrar y explorar el siguiente nivel de la jerarquía académica.',
                attachTo: { element: '#tour-dir-list', on: 'top' }
            });
        // If there is a list of contents (study materials)
        } else if (listElement.querySelector('.list-group-item.list-group-item-action')) {
            contextSteps.push({
                id: 'step-materials',
                title: 'Contenidos Públicos',
                text: '¡Materiales localizados! Abre cualquiera de estos apuntes. Si es útil para tu estudio, podrás copiarlo y usar la IA para examinarte de él.',
                attachTo: { element: '#tour-dir-list', on: 'top' }
            });
        }
    }
    
    let allSteps = [];
    // Only add breadcrumbs if they exist on the page
    if (document.getElementById('tour-dir-breadcrumbs')) {
        allSteps.push(...baseSteps);
    } else {
        // If there are no breadcrumbs (we are at the top level), only show the welcome step
        allSteps.push(baseSteps[0]);
    }
    
    allSteps.push(...contextSteps, finalStep);

    // Filter steps whose elements do not exist on the current page
    const finalSteps = allSteps.filter(step => step && step.attachTo && document.querySelector(step.attachTo.element));

    if (finalSteps.length > 1) { // Only start the tour if there are at least 2 valid steps
        const tour = initializeTour({
            tourId: tourId,
            steps: finalSteps
        });
        if (tour) {
            // APPLY HYBRID PATTERN: button for manual start and automatic on first visit
            startTour(tour, tourId, 'start-academic-directory-tour-btn');
        }
    } else {
        console.log(`[TourLoader] Tour "${tourId}" will not be started because there are not enough guide elements in the DOM.`);
    }
});
