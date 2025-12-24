// /home/MiguelAeTxio/CampuStudiOnline/contents/static/contents/study_room_tour.js
// Tour for the user's study room (content copy view).

document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'studyRoom';
    if (window.activeTours && window.activeTours[tourId]) {
        return; // Avoid reinitialization
    }
    console.log(`[TourLoader] Loading tour definition: ${tourId}`);

    // --- Base tour steps ---
    const baseSteps = [
        {
            id: 'step-assessment-card',
            title: 'Autoevaluaciones con IA',
            text: 'Motor de Evaluaciones Activado. La IA está lista. Solicita un simulacro de examen sobre este contenido, recibe tu nota y aprende de tus errores.',
            attachTo: { element: '#tour-assessment-card', on: 'bottom' }
        },

        { id: 'step-content', title: 'Tu Espacio de Estudio', text: 'Este es el contenido de tu copia personal. Aunque no puedes escribir directamente aquí, puedes seleccionar texto para crear anotaciones y resúmenes.', attachTo: { element: '#material-content', on: 'top' }},
        {
            id: 'step-toolbar-info', title: 'Herramientas de Anotación', text: 'Cuando selecciones texto con el ratón o el dedo, aparecerá una barra flotante como esta. Te permite subrayar, marcar o añadir notas adhesivas a tu selección.', attachTo: { element: '#material-content', on: 'top' },
            beforeShowPromise: () => new Promise(resolve => {
                const tb = document.getElementById('floating-toolbar');
                if (tb) { tb.style.bottom = '50%'; tb.style.left = '50%'; tb.style.transform = 'translate(-50%, 50%)'; tb.classList.add('visible'); }
                resolve();
            }),
            when: { hide: () => { const tb = document.getElementById('floating-toolbar'); if (tb) { tb.classList.remove('visible'); tb.style.bottom = ''; tb.style.left = ''; tb.style.transform = ''; } }}
        },
        { id: 'step-annotations-list', title: 'Tus Anotaciones', text: 'Aquí verás una lista de todas las anotaciones que has creado. Puedes hacer clic en ellas para localizarlas en el texto o eliminarlas.', attachTo: { element: '#annotations-list-container', on: 'left' }},
        { id: 'step-public-toggle', title: 'Visibilidad de tu Copia', text: 'Usa esta opción para hacer tu copia (con todas sus anotaciones) pública. Otros usuarios podrán verla, pero no editarla.', attachTo: { element: '.form-check-label[for="visible_is_public_checkbox"]', on: 'bottom' }},
        { id: 'step-save', title: 'Guardar tu Progreso', text: '¡Muy importante! Haz clic aquí para guardar todas tus anotaciones y los cambios en la visibilidad de tu copia.', attachTo: { element: '#btn-save-copy', on: 'bottom' }},
    ];

    // --- Conditional steps for the assessment panel ---
    const assessmentPanelSteps = [];
    const panelContainer = '#assessment-panel-container';

    // REAL assessment panel state detection
    const canRequest = document.querySelector('#assessment-panel button[type="submit"]');
    const isProcessing = document.querySelector('#assessment-panel .spinner-border');
    const canTake = document.querySelector('#assessment-panel a.btn-success[href*="/assessment/"]');
    const hasResults = document.querySelector('#assessment-panel .available-corrections a');

    if (canRequest) {
        assessmentPanelSteps.push({
            id: 'step-assessment-request', title: 'Solicitar Evaluación', text: 'Desde aquí puedes solicitar a la IA que genere una nueva evaluación basada en este contenido. ¡Pruébalo cuando quieras!', attachTo: { element: canRequest, on: 'bottom' }
        });
    } else if (isProcessing) {
        assessmentPanelSteps.push({
            id: 'step-assessment-processing', title: 'Evaluación en Progreso', text: 'Actualmente, la IA está generando o corrigiendo una evaluación para ti. El panel se actualizará automáticamente cuando termine.', attachTo: { element: isProcessing, on: 'bottom' }
        });
    } else if (canTake) {
        assessmentPanelSteps.push({
            id: 'step-assessment-take', title: '¡Evaluación Lista!', text: '¡Genial! Tienes una evaluación lista para realizar. Al pulsar el botón "Realizar Evaluación", irás a la página del cuestionario.', attachTo: { element: canTake, on: 'bottom' }
        });
        assessmentPanelSteps.push({
            id: 'step-assessment-continue-tour', title: 'Continuar la Guía', text: 'La página del examen también tiene su propia visita guiada. ¿Quieres continuar la simulación allí?', attachTo: { element: canTake, on: 'bottom' },
            buttons: [
                { text: 'Finalizar aquí', action: function() { this.complete(); }, secondary: true },
                {
                    text: 'Continuar Guía (Demo)',
                    action: function() {
                        if (window.assessmentTourDemoURL) {
                            localStorage.setItem('startTakeAssessmentTour', 'true');
                            window.location.href = window.assessmentTourDemoURL;
                        } else {
                            alert('Error: Could not find the demo URL.');
                            this.complete();
                        }
                    },
                    classes: 'shepherd-button-primary'
                }
            ]
        });
    } else if (hasResults) {
        assessmentPanelSteps.push({
            id: 'step-assessment-results', title: 'Resultados Disponibles', text: '¡Tus resultados están listos! Haz clic en el enlace para ver tu puntuación y el feedback de la IA.', attachTo: { element: hasResults, on: 'bottom' }
        });
    }

    const allSteps = [...baseSteps, ...assessmentPanelSteps];
    
    const tour = initializeTour({
        tourId: tourId,
        steps: allSteps
    });

    if (tour) {
        startTour(tour, tourId, 'start-study-room-tour-button');
    }
});
