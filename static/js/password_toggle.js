// /static/js/password_toggle.js
// ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'.
// ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'.

document.addEventListener('DOMContentLoaded', function () {
    // Selecciona todos los campos de contraseña que queremos mejorar.
    const passwordFields = document.querySelectorAll('.password-toggle-field');

    passwordFields.forEach(function (field) {
        // Crear el icono para mostrar/ocultar
        const toggleIcon = document.createElement('i');
        toggleIcon.className = 'fas fa-eye';
        toggleIcon.style.cursor = 'pointer';

        // Crear el span que actuará como botón dentro del input-group
        const toggleButton = document.createElement('span');
        toggleButton.className = 'input-group-text';
        toggleButton.appendChild(toggleIcon);

        // Crear el contenedor 'input-group'
        const wrapper = document.createElement('div');
        wrapper.className = 'input-group';
        
        // Mover el campo de contraseña dentro del nuevo contenedor
        field.parentNode.insertBefore(wrapper, field);
        wrapper.appendChild(field);
        
        // Añadir el botón con el icono al contenedor
        wrapper.appendChild(toggleButton);

        // Añadir el evento de clic al botón (no al icono directamente)
        toggleButton.addEventListener('click', function () {
            // Alternar el tipo de input entre 'password' y 'text'
            const type = field.getAttribute('type') === 'password' ? 'text' : 'password';
            field.setAttribute('type', type);

            // Alternar la clase del icono
            toggleIcon.className = type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
        });
    });
});