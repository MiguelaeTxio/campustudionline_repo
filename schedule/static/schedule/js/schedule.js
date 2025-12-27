document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var createEventBtn = document.getElementById('fab-add-event');
    var modalEl = document.getElementById('eventModal');
    if (!calendarEl || !modalEl) return;

    var bsModal = new bootstrap.Modal(modalEl);
    var modalBody = modalEl.querySelector('.modal-body');
    var agendaTitleEl = document.getElementById('selected-date-display');

    if (agendaTitleEl) agendaTitleEl.style.display = 'none';
    if (createEventBtn) {
        createEventBtn.style.bottom = '90px'; 
        createEventBtn.style.zIndex = '1050';
    }

    var calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'es',
        initialView: 'dayGridMonth',
        height: '80vh',
        navLinks: true,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
        },
        buttonText: { today: 'Hoy', month: 'Mes', week: 'Semana', day: 'Día', list: 'Agenda' },
        events: '/schedule/api/feed/',
        dayMaxEvents: true,
        dateClick: (info) => loadModalContent(buildCreateUrl(info.dateStr, info.view.type)),
        eventClick: (info) => loadModalContent(`/schedule/update/${info.event.id}/`)
    });
    calendar.render();

    function loadModalContent(url) {
        modalBody.innerHTML = ''; 
        bsModal.show();
        
        // Inyección de señal explícita: ?is_ajax=true
        // Usamos URL() para manejar seguramente los parámetros existentes
        const targetUrl = new URL(url, window.location.origin);
        targetUrl.searchParams.set('is_ajax', 'true');

        fetch(targetUrl, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(r => r.ok ? r.text() : Promise.reject(r))
            .then(html => { modalBody.innerHTML = html; })
            .catch(() => { modalBody.innerHTML = '<div class="alert alert-danger mx-3">Error de carga</div>'; });
    }

    function buildCreateUrl(dateStr, viewType) {
        let dateObj = new Date(dateStr);
        if (viewType === 'dayGridMonth' || viewType === 'listMonth') {
            const now = new Date();
            dateObj.setHours(now.getHours() + 1, 0, 0);
        }
        const offset = dateObj.getTimezoneOffset() * 60000;
        return `/schedule/create/?start_time=${encodeURIComponent((new Date(dateObj.getTime() - offset)).toISOString().slice(0, 16))}`;
    }

    modalEl.addEventListener('click', (e) => {
        const link = e.target.closest('.ajax-link');
        if (link) { e.preventDefault(); loadModalContent(link.href); }
    });

    modalEl.addEventListener('submit', (e) => {
        const form = e.target.closest('.ajax-form');
        if (!form) return;
        e.preventDefault();

        // Inyección de señal explícita en el action del formulario
        const targetUrl = new URL(form.action || window.location.href, window.location.origin);
        targetUrl.searchParams.set('is_ajax', 'true');

        fetch(targetUrl, {
            method: 'POST',
            body: new FormData(form),
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(r => r.headers.get('content-type')?.includes('application/json') ? r.json() : r.text())
        .then(data => {
            if (typeof data === 'object' && data.success) {
                bsModal.hide();
                calendar.refetchEvents();
            } else {
                modalBody.innerHTML = data;
            }
        });
    });
    
    if (createEventBtn) {
        createEventBtn.addEventListener('click', () => {
            const now = new Date();
            const offset = now.getTimezoneOffset() * 60000;
            loadModalContent(`/schedule/create/?start_time=${encodeURIComponent((new Date(now.getTime() - offset)).toISOString().slice(0, 16))}`);
        });
    }
});
