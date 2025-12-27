// /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/static/js/tours/schedule_tour.js
// Tour for the Schedule/Agenda application.

document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'schedule';
    
    // Check global tour state to avoid conflicts
    if (window.activeTours && window.activeTours[tourId]) {
        return; 
    }
    
    // Check if we are in the schedule page by looking for specific elements
    const calendarElement = document.getElementById('calendar');
    if (!calendarElement) {
        return;
    }

    console.log(`[TourLoader] Loading tour definition: ${tourId}`);

    const steps = [
        {
            id: 'step-schedule-welcome',
            title: 'Tu Agenda Personal',
            text: 'Bienvenido a tu nueva agenda académica. Aquí podrás organizar todo tu tiempo de estudio, entregas y exámenes.',
            attachTo: { element: '.schedule-container', on: 'top' },
            buttons: [
                {
                    text: 'Siguiente',
                    action: function() { return this.next(); }
                }
            ]
        },
        {
            id: 'step-calendar-nav',
            title: 'Navegación',
            text: 'Usa este calendario para cambiar entre meses, semanas o días. Haz clic en cualquier día para ver sus detalles o crear un evento.',
            attachTo: { element: '#calendar', on: 'left' }
        },
        {
            id: 'step-agenda-panel',
            title: 'Detalle Diario',
            text: 'En este panel verás la lista cronológica de tus eventos para el día seleccionado. Mantén el control de tus tareas pendientes aquí.',
            attachTo: { element: '.agenda-wrapper', on: 'right' }
        },
        {
            id: 'step-create-event',
            title: 'Añadir Evento Manual',
            text: '¿Tienes una nueva entrega o examen? Usa este botón flotante para añadirlo rápidamente a tu calendario de forma manual.',
            attachTo: { element: '#fab-add-event', on: 'left' }
        },
        {
            id: 'step-universia-shortcut',
            title: 'Atajo con UniversIA',
            text: `
                <p><strong>Consejo Pro:</strong> Úsala como secretaria. Escríbele por el chat: <em>"Añade un examen de Matemáticas el viernes a las 10"</em> y ella creará el evento por ti.</p>
                <p><small><i class="fas fa-arrows-alt"></i> ¡Por cierto! Si el icono te molesta, puedes arrastrarlo y moverlo a cualquier parte de la pantalla.</small></p>
            `,
            attachTo: { element: '#universia-widget-container', on: 'top' }
        }
    ];

    // Initialize tour only if elements exist
    const finalSteps = steps.filter(step => step && step.attachTo && document.querySelector(step.attachTo.element));

    if (finalSteps.length > 0) {
        const tour = initializeTour({
            tourId: tourId,
            steps: finalSteps
        });
    
        if (tour) {
            startTour(tour, tourId, 'start-schedule-tour-btn');
        }
    }
});
