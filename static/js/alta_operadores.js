document.addEventListener('DOMContentLoaded', () => {
    const formAlta = document.getElementById('form-alta-operador');

    formAlta.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Operador registrado correctamente ✅');
        window.location.href = '/home_admin/';
    });
});
