// Tour for the Translation Room (Streaming UI Version)
document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'translation_room_v2';
    
    if (window.activeTours && window.activeTours[tourId]) return;

    const steps = [
        {
            id: 'step-welcome',
            title: 'Traductor Neuronal',
            text: 'Bienvenido a la nueva interfaz de traducción simultánea. Diseñada para textos académicos largos.',
            attachTo: { element: '.h3', on: 'bottom' },
            buttons: [
                {
                    text: 'Siguiente',
                    action: function() { return this.next(); }
                }
            ]
        },
        {
            id: 'step-languages',
            title: 'Selección de Idioma',
            text: 'Configura el idioma de origen (o déjalo en Auto) y el de destino aquí.',
            attachTo: { element: '#id_source_lang', on: 'bottom' }
        },
        {
            id: 'step-source-editor',
            title: 'Editor de Entrada',
            text: 'Escribe o pega tu texto aquí. Tienes herramientas para limpiar o pegar rápidamente en la barra superior.',
            attachTo: { element: '#source-editor', on: 'right' }
        },
        {
            id: 'step-document',
            title: 'Documentos',
            text: 'O sube un PDF/Word. El contenido se extraerá y añadirá al editor automáticamente.',
            attachTo: { element: 'input[type="file"]', on: 'bottom' }
        },
        {
            id: 'step-translate',
            title: 'Traducción en Tiempo Real',
            text: 'Pulsa traducir y verás el resultado aparecer palabra por palabra en el panel derecho, sin esperas.',
            attachTo: { element: '#btn-translate', on: 'bottom' }
        }
    ];

    const tour = initializeTour({
        tourId: tourId,
        steps: steps
    });

    if (tour) {
        startTour(tour, tourId);
    }
});
