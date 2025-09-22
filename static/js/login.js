document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginBox = document.getElementById('loginBox');
    const usernameField = document.getElementById('usernameField');
    const passwordField = document.getElementById('passwordField');
    const usernameError = document.getElementById('usernameError');
    const passwordError = document.getElementById('passwordError');
    const loginError = document.getElementById('loginError');
    const loginButton = document.getElementById('loginButton');
    const spinner = document.querySelector('.spinner');
    const buttonText = document.querySelector('.button-text');

    // Credenciales válidas (esto será reemplazado por la validación del backend)
    const validUsername = 'admin';
    const validPassword = 'admin123';

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Resetear errores
        resetErrors();
        
        const username = document.getElementById('usuario').value.trim();
        const password = document.getElementById('contrasena').value.trim();
        
        let isValid = true;
        
        // Validar usuario
        if (!username) {
            showError(usernameField, usernameError, 'Por favor ingrese su usuario');
            isValid = false;
        }
        
        // Validar contraseña
        if (!password) {
            showError(passwordField, passwordError, 'Por favor ingrese su contraseña');
            isValid = false;
        } else if (password.length < 6) {
            showError(passwordField, passwordError, 'La contraseña debe tener al menos 6 caracteres');
            isValid = false;
        }
        
        if (!isValid) {
            loginBox.classList.add('shake');
            setTimeout(() => loginBox.classList.remove('shake'), 500);
            return;
        }
        
        // Simular proceso de autenticación
        simulateLogin(username, password);
    });

    function simulateLogin(username, password) {
        // Mostrar estado de carga
        loginButton.disabled = true;
        loginButton.classList.add('loading');
        buttonText.textContent = 'Verificando...';
        
        // Simular delay de red (esto será reemplazado por una llamada AJAX al backend)
        setTimeout(() => {
            if (username === validUsername && password === validPassword) {
                // Login exitoso
                loginSuccess();
            } else {
                // Login fallido
                loginFailed();
            }
            
            // Restaurar estado del botón
            loginButton.disabled = false;
            loginButton.classList.remove('loading');
            buttonText.textContent = 'Iniciar Sesión';
        }, 1500);
    }

    function loginSuccess() {
        // Aquí redirigirías al usuario a la página principal
        alert('¡Inicio de sesión exitoso! Redirigiendo al sistema...');
        // window.location.href = 'dashboard.html';
    }

    function loginFailed() {
        loginError.style.display = 'block';
        usernameField.classList.add('error');
        passwordField.classList.add('error');
        loginBox.classList.add('shake');
        setTimeout(() => loginBox.classList.remove('shake'), 500);
    }

    function showError(field, errorElement, message) {
        field.classList.add('error');
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }

    function resetErrors() {
        usernameField.classList.remove('error');
        passwordField.classList.remove('error');
        usernameError.style.display = 'none';
        passwordError.style.display = 'none';
        loginError.style.display = 'none';
    }

    // Limpiar errores cuando el usuario comience a escribir
    document.getElementById('usuario').addEventListener('input', function() {
        usernameField.classList.remove('error');
        usernameError.style.display = 'none';
        loginError.style.display = 'none';
    });

    document.getElementById('contrasena').addEventListener('input', function() {
        passwordField.classList.remove('error');
        passwordError.style.display = 'none';
        loginError.style.display = 'none';
    });
});