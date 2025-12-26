// --- Funciones Globales (Accesibles desde HTML onclick) ---
var bsModal;
var modalEl;

window.loadModalContent = function(url) {
    if (!modalEl) modalEl = document.getElementById('eventModal');
    if (!bsModal) bsModal = new bootstrap.Modal(modalEl);
    
    // Mostrar spinner inicial
    modalEl.querySelector('.modal-body').innerHTML = '<div class="text-center py-4"><div class="spinner-border text-primary"></div></div>';
    bsModal.show();
    
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then(function(r) { return r.ok ? r.text() : Promise.reject(r); })
        .then(function(html) { 
            var container = modalEl.querySelector('.modal-body');
            container.innerHTML = html;
            
            // FORZAR EJECUCIÓN DE SCRIPTS (Necesario para disparar el evento de cierre)
            var scripts = container.querySelectorAll('script');
            scripts.forEach(function(oldScript) {
                var newScript = document.createElement('script');
                newScript.text = oldScript.text;
                oldScript.parentNode.replaceChild(newScript, oldScript);
            });
        })
        .catch(function(e) { 
            console.error('Error loadModalContent:', e);
            modalEl.querySelector('.modal-body').innerHTML = '<div class="alert alert-danger">Error de comunicación con el servidor</div>'; 
        });
};

window.openEventModal = function(id) {
    var url = '/schedule/update/' + id + '/';
    window.loadModalContent(url);
};

// --- Inicialización del Calendario ---
document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    if (!calendarEl) return;

    var createEventBtn = document.getElementById('fab-add-event');
    
    var calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'es',
        initialView: 'dayGridMonth',
        height: '80vh',
        navLinks: true,
        nowIndicator: true,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
        },
        buttonText: {
            today: 'Hoy', month: 'Mes', week: 'Semana', day: 'Día', list: 'Agenda'
        },
        views: {
            timeGridWeek: { slotMinTime: '08:00:00', slotMaxTime: '22:00:00' },
            timeGridDay: { slotMinTime: '08:00:00', slotMaxTime: '22:00:00' }
        },
        events: '/schedule/api/feed/',
        dateClick: function(info) {
            var dateObj = new Date(info.dateStr);
            if (info.view.type === 'dayGridMonth' || info.view.type === 'listMonth') {
                var now = new Date();
                dateObj.setHours(now.getHours() + 1, 0, 0);
            }
            var offsetMs = dateObj.getTimezoneOffset() * 60000;
            var localISOTime = (new Date(dateObj.getTime() - offsetMs)).toISOString().slice(0, 16);
            window.loadModalContent('/schedule/create/?start_time=' + encodeURIComponent(localISOTime));
        },
        eventClick: function(info) {
            window.openEventModal(info.event.id);
        }
    });

    calendar.render();

    if (createEventBtn) {
        createEventBtn.addEventListener('click', function() {
            var now = new Date();
            var offsetMs = now.getTimezoneOffset() * 60000;
            var localISOTime = (new Date(now.getTime() - offsetMs)).toISOString().slice(0, 16);
            window.loadModalContent('/schedule/create/?start_time=' + encodeURIComponent(localISOTime));
        });
    }

    // Escuchador del evento de actualización con burbujeo (Bubbles: true)
    document.body.addEventListener('calendarUpdated', function() {
        if (bsModal) bsModal.hide();
        calendar.refetchEvents();
    });
});