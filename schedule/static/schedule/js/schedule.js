document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var createEventBtn = document.getElementById('fab-add-event');
    var modalEl = document.getElementById('eventModal');
    var bsModal = new bootstrap.Modal(modalEl);
    var agendaTitleEl = document.getElementById('selected-date-display');

    // Limpiar mensaje de "Cargando..." inmediatamente
    if (agendaTitleEl) agendaTitleEl.style.display = 'none';

    // Ajuste de posición del botón flotante
    if (createEventBtn) {
        createEventBtn.style.bottom = '90px'; 
        createEventBtn.style.zIndex = '1050';
    }

    const URLS = {
        feed: '/schedule/api/feed/',
        create: '/schedule/create/',
        update_base: '/schedule/update/' 
    };

    var calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'es',
        initialView: 'dayGridMonth', // Vista inicial: Mes
        height: '80vh',              // Altura fija para evitar colapsos
        navLinks: true,              // Permitir clicar en día/semana para navegar
        nowIndicator: true,          // Línea roja de hora actual
        
        // Cabecera completa tipo Agenda
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
        },
        buttonText: {
            today: 'Hoy',
            month: 'Mes',
            week: 'Semana',
            day: 'Día',
            list: 'Agenda' // Vista tipo lista (Referencia usuario)
        },
        
        // Vistas personalizadas
        views: {
            timeGridWeek: {
                slotMinTime: '08:00:00',
                slotMaxTime: '22:00:00',
                allDayText: 'Día', // Texto corto para reducir ancho columna
                dayHeaderFormat: { weekday: 'short', day: 'numeric', omitCommas: true } // Ej: 'dom 21'
            },
            timeGridDay: {
                slotMinTime: '08:00:00',
                slotMaxTime: '22:00:00',
                allDayText: 'Todo el día'
            }
        },

        events: URLS.feed,
        dayMaxEvents: true, // Mostrar "+X más" si hay muchos eventos
        
        // Comportamiento al clicar en un hueco vacío (Crear)
        dateClick: function(info) {
            // Preparar fecha/hora para el modal
            let dateStr = info.dateStr;
            let dateObj = new Date(dateStr);
            
            // Si es vista de mes (sin hora), poner hora actual o 09:00 por defecto
            if (info.view.type === 'dayGridMonth' || info.view.type === 'listMonth') {
                const now = new Date();
                dateObj.setHours(now.getHours() + 1, 0, 0); // Próxima hora en punto
            }
            
            // Ajuste zona horaria para input datetime-local
            const offsetMs = dateObj.getTimezoneOffset() * 60000;
            const localISOTime = (new Date(dateObj.getTime() - offsetMs)).toISOString().slice(0, 16);
            
            const url = `${URLS.create}?start_time=${encodeURIComponent(localISOTime)}`;
            loadModalContent(url);
        },

        // Comportamiento al clicar en un evento (Editar)
        eventClick: function(info) {
            openEventModal(info.event.id);
        },

        // Personalización de renderizado de eventos (Colores y Estilos)
        eventDidMount: function(info) {
            // Si estamos en vista de lista, estilizar la fila
            if (info.view.type === 'listMonth') {
                let dot = info.el.querySelector('.fc-list-event-dot');
                if (dot) dot.style.borderColor = info.event.backgroundColor;
            }
        }
    });

    calendar.render();

    // Handler Botón Flotante (+)
    if (createEventBtn) {
        createEventBtn.addEventListener('click', function() {
            const now = new Date();
            const offsetMs = now.getTimezoneOffset() * 60000;
            const localISOTime = (new Date(now.getTime() - offsetMs)).toISOString().slice(0, 16);
            
            const url = `${URLS.create}?start_time=${encodeURIComponent(localISOTime)}`;
            loadModalContent(url);
        });
    }

    window.openEventModal = function(id) {
        const url = `${URLS.update_base}${id}/`;
        loadModalContent(url);
    };

    function loadModalContent(url) {
        modalEl.querySelector('.modal-body').innerHTML = '<div class="text-center py-4"><div class="spinner-border text-primary"></div></div>';
        bsModal.show();
        
        fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(r => r.ok ? r.text() : Promise.reject(r))
            .then(html => { modalEl.querySelector('.modal-body').innerHTML = html; })
            .catch(e => { 
                console.error(e);
                modalEl.querySelector('.modal-body').innerHTML = '<div class="alert alert-danger">Error de carga</div>'; 
            });
    }

    document.body.addEventListener('calendarUpdated', function() {
        bsModal.hide();
        calendar.refetchEvents();
    });
});
