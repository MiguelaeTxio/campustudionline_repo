// /home/MiguelAeTxio/CampuStudiOnline/static/js/tours/user_account_tour.js
// Tour for the user's account management page.

document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'userAccount';
    if (window.activeTours && window.activeTours[tourId]) {
        return; // Avoid reinitialization
    }
    console.log(`[TourLoader] Loading tour definition: ${tourId}`);

    const steps = [
        {
            id: 'step-welcome',
            title: 'Tu Panel de Control',
            text: 'Desde esta página puedes gestionar todos los aspectos de tu cuenta. Te mostraremos las secciones principales.',
            attachTo: { element: '#tour-account-title', on: 'bottom' }
        },
        {
            id: 'step-settings',
            title: 'Configuración de la Cuenta',
            text: 'Aquí puedes cambiar tu nombre de usuario o tu correo electrónico. Son tus credenciales principales.',
            attachTo: { element: '#tour-account-settings', on: 'bottom' }
        },
        {
            id: 'step-profile',
            title: 'Perfil y Privacidad',
            text: 'Desde aquí puedes editar la información que otros usuarios ven de ti, como tu biografía o tus enlaces, y controlar la privacidad de tu portafolio.',
            attachTo: { element: '#tour-account-profile', on: 'top' }
        },
        {
            id: 'step-security',
            title: 'Seguridad',
            text: 'Usa esta sección para cambiar tu contraseña de forma segura siempre que lo necesites.',
            attachTo: { element: '#tour-account-security', on: 'bottom' }
        },
        {
            id: 'step-danger-zone',
            title: 'Zona de Peligro',
            text: '¡Con cuidado! Esta opción es para eliminar tu cuenta permanentemente. Es una acción que no se puede deshacer.',
            attachTo: { element: '#tour-account-danger', on: 'top' }
        }
    ];

    const allElementsPresent = steps.every(step => document.querySelector(step.attachTo.element));

    if (allElementsPresent) {
        const tour = initializeTour({
            tourId: tourId,
            steps: steps
        });

        if (tour) {
            // APPLY HYBRID PATTERN
            startTour(tour, tourId, 'start-user-account-tour-btn');
        }
    } else {
        console.log(`[TourLoader] Tour "${tourId}" will not be started because elements are missing from the DOM.`);
    }
});
