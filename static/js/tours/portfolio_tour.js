// /home/MiguelAeTxio/CampuStudiOnline/static/js/tours/portfolio_tour.js
// Tour for the user's public portfolio page.

document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'portfolioTour';
    if (window.activeTours && window.activeTours[tourId]) {
        return; // Avoid reinitialization
    }
    console.log(`[TourLoader] Loading tour definition: ${tourId}`);

    const allSteps = [
        {
            id: 'step-welcome',
            title: 'Tu Portafolio Público',
            text: '¡Esta es tu tarjeta de presentación! Aquí es donde otros usuarios pueden ver la información que decides compartir. Te mostraremos las secciones clave.',
            attachTo: { element: '#tour-portfolio-header', on: 'bottom' }
        },
        {
            id: 'step-about-me',
            title: 'Sección "Sobre mí"',
            text: 'Aquí se muestra tu descripción personal. Puedes editarla y cambiar su visibilidad desde el panel de "Editar Perfil y Privacidad".',
            attachTo: { element: '#tour-portfolio-about', on: 'bottom' }
        },
        {
            id: 'step-info',
            title: 'Información de Contacto',
            text: 'Esta área muestra los datos de contacto y académicos que has decidido hacer públicos. También se gestiona desde tu perfil.',
            attachTo: { element: '#tour-portfolio-info', on: 'bottom' }
        },
        {
            id: 'step-materials',
            title: 'Materiales de Estudio',
            text: 'Este enlace lleva a tu directorio personal, donde se listan todos tus materiales. Desde allí puedes gestionar cuáles son públicos y cuáles privados.',
            attachTo: { element: '#tour-portfolio-materials', on: 'bottom' }
        },
        {
            id: 'step-links',
            title: 'Enlaces de Interés',
            text: 'Aquí aparecen los enlaces que compartes. Puedes añadir o eliminar enlaces desde las "Acciones Rápidas" al final de la página.',
            attachTo: { element: '#tour-portfolio-links', on: 'bottom' }
        },
        {
            id: 'step-chat-rooms',
            title: 'Salas de Chat',
            text: 'Esta sección muestra las salas de chat a las que perteneces. Puedes controlar si esta sección es visible para otros usando el botón de configuración.',
            attachTo: { element: '#tour-portfolio-chat-rooms', on: 'bottom' }
        },
        {
            id: 'step-messages',
            title: 'Mensajes Cortos',
            text: 'Utiliza esta sección para compartir actualizaciones rápidas o pensamientos. También puedes gestionarlos desde las "Acciones Rápidas".',
            attachTo: { element: '#tour-portfolio-messages', on: 'bottom' }
        },
        {
            id: 'step-p2p',
            title: 'Mensajería Privada',
            text: 'Este es el punto de entrada a tus conversaciones privadas de usuario a usuario. Un enlace similar aparecerá en los portafolios de otros para que puedas contactarlos.',
            attachTo: { element: '#tour-portfolio-p2p', on: 'top' }
        },
        {
            id: 'step-actions',
            title: 'Acciones Rápidas',
            text: 'Finalmente, este panel te da acceso directo para añadir contenido a tu portafolio sin tener que navegar a otras páginas. ¡Es tu centro de mando!',
            attachTo: { element: '#tour-portfolio-actions', on: 'top' }
        }
    ];

    // Dynamically filter steps based on elements present in the DOM
    const finalSteps = allSteps.filter(step => step && step.attachTo && document.querySelector(step.attachTo.element));

    if (finalSteps.length > 1) { // Only start if there are enough elements to guide
        const tour = initializeTour({
            tourId: tourId,
            steps: finalSteps
        });
        if (tour) {
            // APPLY HYBRID PATTERN
            startTour(tour, tourId, 'start-portfolio-tour-btn');
        }
    } else {
        console.log(`[TourLoader] Tour "${tourId}" will not be started because there are not enough guide elements in the DOM.`);
    }
});
