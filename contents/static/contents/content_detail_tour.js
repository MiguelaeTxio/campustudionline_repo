// /home/MiguelAeTxio/CampuStudiOnline/contents/static/contents/content_detail_tour.js
// Tour for the public content detail page.

document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'contentDetail';
    if (window.activeTours && window.activeTours[tourId]) {
        return; // Avoid reinitialization
    }
    console.log(`[TourLoader] Loading tour definition: ${tourId}`);

    const allPossibleSteps = [
        {
            id: 'step-1-copy-button',
            title: 'Tu Sala de Estudio Personal',
            text: 'PASO CLAVE: ¿Quieres que la IA te examine de este texto? Cópialo a tu Sala de Estudio para desbloquear el generador de exámenes y las herramientas de anotación.',
            attachTo: { element: '#tour-step-1-copy-button', on: 'bottom' }
        },
        {
            id: 'step-2-share-buttons',
            title: 'Comparte el Conocimiento',
            text: 'Usa estos botones para compartir este material en redes sociales o copiar el enlace directo.',
            attachTo: { element: '#tour-step-2-share-buttons', on: 'bottom' }
        },
        {
            id: 'step-report-button',
            title: 'Reportar Errores',
            text: '¿Has encontrado una errata o un problema en el contenido? Ayúdanos a mejorar usando este botón para reportarlo.',
            attachTo: { element: '[href*="feedback/report/content"]', on: 'bottom' }
        },
        {
            id: 'step-3-edit-buttons',
            title: 'Gestiona tu Contenido',
            text: 'Si eres el creador, desde aquí podrás editar o eliminar este material.',
            attachTo: { element: '#tour-step-3-edit-buttons', on: 'bottom' }
        },
        {
            id: 'step-4-content-body',
            title: 'El Contenido Principal',
            text: 'Aquí se encuentra el material de estudio. Puedes leerlo, analizarlo y usarlo como base para tus anotaciones y autoevaluaciones.',
            attachTo: { element: '#tour-step-4-content-body', on: 'top' }
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
            startTour(tour, tourId, 'start-content-detail-tour-btn');
        }
    } else {
         console.log(`[TourLoader] Tour "${tourId}" will not be started because there are not enough elements in the DOM.`);
    }
});
