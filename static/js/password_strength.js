// /static/js/password_strength.js
// ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'.
// ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'.

document.addEventListener('DOMContentLoaded', function () {
    const pass1 = document.getElementById('id_password1');
    const pass2 = document.getElementById('id_password2');
    const strengthBar = document.getElementById('password-strength-bar');
    const strengthText = document.getElementById('password-strength-text');
    const matchText = document.getElementById('password-match-text');

    if (!pass1 || !pass2 || !strengthBar || !strengthText || !matchText) {
        // Si alguno de los elementos no existe, no hacemos nada.
        // Esto evita errores en consola en otras páginas que no sean el registro.
        return;
    }

    // --- LÓGICA DE FUERZA DE CONTRASEÑA ---
    pass1.addEventListener('keyup', function () {
        checkPasswordStrength(pass1.value);
        checkPasswordMatch(); // También comprobamos si coinciden por si el usuario cambia pass1 después de pass2
    });

    function checkPasswordStrength(password) {
        let score = 0;
        if (password.length > 8) score++;
        if (password.match(/[a-z]/)) score++;
        if (password.match(/[A-Z]/)) score++;
        if (password.match(/[0-9]/)) score++;
        if (password.match(/[^a-zA-Z0-9]/)) score++;

        // Actualizar la barra de progreso y el texto
        switch (score) {
            case 0:
            case 1:
            case 2:
                strengthBar.style.width = '25%';
                strengthBar.className = 'progress-bar bg-danger';
                strengthText.textContent = 'Débil';
                strengthText.className = 'form-text text-danger';
                break;
            case 3:
                strengthBar.style.width = '50%';
                strengthBar.className = 'progress-bar bg-warning';
                strengthText.textContent = 'Aceptable';
                strengthText.className = 'form-text text-warning';
                break;
            case 4:
                strengthBar.style.width = '75%';
                strengthBar.className = 'progress-bar bg-info';
                strengthText.textContent = 'Buena';
                strengthText.className = 'form-text text-info';
                break;
            case 5:
                strengthBar.style.width = '100%';
                strengthBar.className = 'progress-bar bg-success';
                strengthText.textContent = 'Fuerte';
                strengthText.className = 'form-text text-success';
                break;
        }

        if (password.length === 0) {
            strengthBar.style.width = '0%';
            strengthText.textContent = '';
        }
    }

    // --- LÓGICA DE COINCIDENCIA DE CONTRASEÑAS ---
    pass2.addEventListener('keyup', checkPasswordMatch);

    function checkPasswordMatch() {
        const val1 = pass1.value;
        const val2 = pass2.value;

        if (val2.length === 0) {
            matchText.textContent = '';
            return;
        }

        if (val1 === val2) {
            matchText.textContent = 'Las contraseñas coinciden';
            matchText.className = 'form-text text-success';
        } else {
            matchText.textContent = 'Las contraseñas no coinciden';
            matchText.className = 'form-text text-danger';
        }
    }
});