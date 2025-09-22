document.addEventListener('DOMContentLoaded', () => {
    const sendRequestBtn = document.getElementById('send-request-btn');
    const backToHomeBtn = document.getElementById('back-to-home-btn');
    const messageText = document.getElementById('message-text');
    const titleText = document.getElementById('title-text');

    sendRequestBtn.addEventListener('click', () => {
        // Oculta el botón de "Enviar solicitud"
        sendRequestBtn.style.display = 'none';

        // Muestra el botón de "Volver al inicio"
        backToHomeBtn.style.display = 'block';

        // Cambia título y mensaje
        titleText.textContent = 'Solicitud enviada';
        messageText.textContent = 'La Solicitud se ha enviado exitosamente';
        // ya no agregamos clase verde, se mantiene gris
    });

    backToHomeBtn.addEventListener('click', () => {
        window.location.href = 'index.html'; 
    });
});
