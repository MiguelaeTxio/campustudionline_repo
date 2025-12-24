// /home/MiguelAeTxio/CampuStudiOnline/assessment/static/assessment/view_results_tour.js
document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'viewResults';
    if (window.activeTours && window.activeTours[tourId]) {
        return; // Avoid reinitialization
    }
    console.log(`[TourLoader] Loading tour definition: ${tourId}`);

    // --- Specific logic to find and prepare DOM elements ---
    let firstAnsweredRow = null;
    const allAnswerRows = document.querySelectorAll('.row');
    allAnswerRows.forEach(row => {
        if (!firstAnsweredRow && row.querySelector('.col-md-6 .card-body p')) {
            firstAnsweredRow = row;
        }
    });

    let tourBlockElement = null;
    if (firstAnsweredRow) {
        const questionCard = firstAnsweredRow.previousElementSibling;
        if (questionCard && questionCard.matches('.card.mb-4')) {
            // Create a dynamic wrapper for the tour if it doesn't exist
            let wrapper = document.getElementById('tour-comparison-block');
            if (!wrapper) {
                wrapper = document.createElement('div');
                wrapper.id = 'tour-comparison-block';
                questionCard.parentNode.insertBefore(wrapper, questionCard);
                wrapper.appendChild(questionCard);
                wrapper.appendChild(firstAnsweredRow);
            }
            tourBlockElement = wrapper;
        }
    }
    
    const firstEvaluationCard = firstAnsweredRow ? firstAnsweredRow.nextElementSibling : null;
    if (firstEvaluationCard && !firstEvaluationCard.id) {
        firstEvaluationCard.id = 'first-evaluation-card';
    }
    // --- End of specific logic ---

    const steps = [
        {
            id: 'step-welcome',
            title: 'Resultados de tu Evaluación',
            text: 'Aquí puedes ver la corrección detallada de tu autoevaluación, comparando tus respuestas con las de la IA.',
            attachTo: { element: '.card-header', on: 'bottom' }
        },
        {
            id: 'step-comparison',
            title: 'Comparativa de Respuestas',
            text: 'Encontrarás las preguntas junto con tus respuestas y la respuesta modelo que da la IA, para que puedas compararlas.',
            attachTo: { element: tourBlockElement ? '#tour-comparison-block' : '.row', on: 'bottom' }
        },
        {
            id: 'step-feedback',
            title: 'Puntuación y Feedback',
            text: 'En esta sección, la IA te da una puntuación numérica y un feedback cualitativo sobre tu respuesta.',
            attachTo: { element: firstEvaluationCard ? '#first-evaluation-card' : '.card.mb-5.bg-light', on: 'top' }
        },
        {
            id: 'step-back',
            title: 'Volver a la Sala de Estudio',
            text: 'Cuando termines de revisar tu corrección, puedes volver a la sala de estudio desde aquí.',
            attachTo: { element: '.card-footer a.btn-primary', on: 'top' }
        }
    ];

    // If the DOM preparation logic failed, we do not show the steps that depend on it.
    if (!tourBlockElement) {
        steps.splice(1, 2); 
    }

    const tour = initializeTour({
        tourId: tourId,
        steps: steps
    });

    if (tour) {
        startTour(tour, tourId, 'start-view-results-tour-button');
    }
});
