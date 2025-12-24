// /home/MiguelAeTxio/CampuStudiOnline/assessment/static/assessment/take_assessment_tour.js
document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'takeAssessment';
    if (window.activeTours && window.activeTours[tourId]) {
        return; // Avoid reinitialization
    }
    console.log(`[TourLoader] Loading tour definition: ${tourId}`);

    const steps = [
        {
            id: 'step-welcome',
            title: 'Tu Autoevaluación',
            text: '¡Bienvenido a tu cuestionario personalizado! La IA ha preparado estas preguntas basándose en el material de estudio.',
            attachTo: { element: '.card-header', on: 'bottom' }
        },
        {
            id: 'step-questions',
            title: 'Responde a las Preguntas',
            text: 'Lee cada pregunta con atención y escribe tu respuesta en el cuadro de texto correspondiente. ¡Tómate tu tiempo para responder de la forma más completa posible!',
            attachTo: { element: 'form ol', on: 'top' }
        },
        {
            id: 'step-submit',
            title: 'Enviar para Corrección',
            text: 'Una vez que hayas respondido a todas las preguntas, pulsa este botón. Tus respuestas serán enviadas a la IA para su corrección y recibirás una puntuación y feedback detallado.',
            attachTo: { element: '#assessment-form button[type="submit"]', on: 'top' }
        }
    ];

    const tour = initializeTour({
        tourId: tourId,
        steps: steps
    });

    if (tour) {
        // Special start logic: force if coming from another tour.
        const startTourFlag = 'startTakeAssessmentTour';
        if (localStorage.getItem(startTourFlag)) {
            console.log(`[TourLoader] Forcing start of tour "${tourId}" due to redirection.`);
            localStorage.removeItem(startTourFlag);
            setTimeout(() => {
                if (!tour.isActive()) {
                    tour.start();
                }
            }, 500);
        } else {
            // Standard start logic
            startTour(tour, tourId, 'start-assessment-tour-button');
        }
    }
});
