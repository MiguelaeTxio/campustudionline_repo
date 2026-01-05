// /home/MiguelAeTxio/CampuStudiOnline/static/js/tours/home_tour.js
// Tour for the home page (Responsive Version).

document.addEventListener('DOMContentLoaded', function () {
    const tourId = 'home_v36';
    if (window.activeTours && window.activeTours[tourId]) {
        return; 
    }
    console.log(`[TourLoader] Loading tour definition: ${tourId}`);

    // Detectar si estamos en vista móvil (hamburguesa visible)
    const navbarToggler = document.querySelector('.navbar-toggler');
    const isMobile = navbarToggler && window.getComputedStyle(navbarToggler).display !== 'none';

    let steps = [];

    // Paso 1: Bienvenida (Común)
    steps.push({
        id: 'step-welcome',
        title: '¡Bienvenido a CampuStudiOnline!',
        text: 'Esta es tu página de inicio. Te daremos un breve recorrido por la plataforma.',
        attachTo: { element: '.display-5.fw-bold', on: 'bottom' },
        buttons: [
            {
                text: 'Siguiente',
                action: function() {
                    return this.next();
                }
            }
        ]
    });

    // Paso 2: Apertura de Menú (Solo Móvil)
    if (isMobile) {
        steps.push({
            id: 'step-mobile-menu',
            title: 'Menú de Navegación',
            text: 'Toca "Siguiente" para desplegar el menú y descubrir las herramientas académicas.',
            attachTo: { element: '.navbar-toggler', on: 'bottom' },
            buttons: [
                {
                    text: 'Siguiente',
                    action: function() {
                        const toggler = document.querySelector('.navbar-toggler');
                        const collapse = document.getElementById('navigationBar');
                        // Si el menú está cerrado, lo abrimos
                        if (collapse && !collapse.classList.contains('show')) {
                            toggler.click();
                            // Esperamos a que la animación de Bootstrap termine (aprox 350-400ms)
                            setTimeout(() => this.next(), 400); 
                        } else {
                            this.next();
                        }
                    }
                }
            ]
        });
    }

    // Pasos Comunes (Ahora visibles en móvil tras la apertura)
    
    // Directorio Académico
    steps.push({
        id: 'step-academic-directory',
        title: 'Directorio Académico',
        text: 'Navega por la estructura oficial (Universidades, Grados, Asignaturas). Encuentra los materiales organizados por planes de estudio para preparar tus materias.',
        attachTo: { element: '#tour-nav-academic-directory', on: 'bottom' }
    });

    // Agenda Personal
    steps.push({
        id: 'step-nav-schedule',
        title: 'Nueva Agenda',
        text: '¡Novedad! Organiza tu tiempo, planifica exámenes y entregas en tu calendario personal.',
        attachTo: { element: '#tour-nav-schedule', on: 'bottom' }
    });


    // Verificamos autenticación
    const isAuthenticated = !!document.getElementById('tour-nav-user-menu');

    if (isAuthenticated) {
        steps.push(
            {
                id: 'step-intellectual-directory',
                title: 'Contenidos Libres',
                text: 'Empieza aquí: Busca apuntes y guías. Es el primer paso para poder evaluarte con IA sobre ellos.',
                attachTo: { element: '#tour-nav-intellectual-directory', on: 'bottom' }
            },
            {
                id: 'step-translation-room',
                title: 'Sala de Traducción',
                text: 'Nueva herramienta IA. Traduce textos o documentos PDF/Word completos conservando el formato.',
                attachTo: { element: '#tour-nav-translation', on: 'bottom' }
            },
            {
                id: 'step-personal-directory',
                title: 'Directorio Personal',
                text: 'Gestiona tus carpetas y materiales propios desde aquí.',
                attachTo: { element: '#tour-nav-personal-directory', on: 'bottom' }
            },
            {
                id: 'step-study-room',
                title: 'Sala de Estudio',
                text: 'Donde estudias de verdad. Aquí puedes subrayar tus copias y pedirle a la IA que te haga un examen de cualquier contenido.',
                attachTo: { element: '#tour-nav-study-room', on: 'bottom' }
            },
            {
                id: 'step-user-menu',
                title: 'Tu Cuenta',
                text: 'Panel de control, perfil y configuración de seguridad.',
                attachTo: { element: '#tour-nav-user-menu', on: 'bottom' }
            }
        );
    } else {
        steps.push({
            id: 'step-login-register-guest',
            title: 'Únete a nosotros',
            text: 'Inicia sesión o regístrate para acceder a todas las herramientas.',
            attachTo: { element: '#tour-nav-login', on: 'bottom' }
        });
    }

    
    // UniversIA (Asistente)
    steps.push({
        id: 'step-universia-widget',
        title: 'UniversIA: Tu Asistente IA',
        text: `
            <p>Este es tu asistente inteligente. Tiene dos modos de funcionamiento:</p>
            <ul>
                <li><strong>🐶 Perro Guía y Secretaria (Global):</strong> Te ayuda a navegar y gestiona tus eventos por chat.</li>
                <li><strong>🎓 Profesora (Sólo en Sala de Estudio):</strong> Se convierte en experta académica para resolver dudas.</li>
            </ul>
            <p><small><i class="fas fa-arrows-alt"></i> <strong>Tip:</strong> El icono es flotante. ¡Puedes arrastrarlo si te molesta!</small></p>
        `,
        attachTo: { element: '#universia-widget-container', on: 'top' }
    });

    // Filtrar pasos cuyos elementos no existen (seguridad adicional)
    const finalSteps = steps.filter(step => step && step.attachTo && document.querySelector(step.attachTo.element));

    if (finalSteps.length > 0) {
        const tour = initializeTour({
            tourId: tourId,
            steps: finalSteps
        });
    
        if (tour) {
            startTour(tour, tourId, 'start-home-tour-btn');
        }
    }
});
