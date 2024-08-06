document.querySelectorAll('form[action*="seleccionar_asientos"]').forEach(form => {
    form.addEventListener('submit', function(event) {
        const pasajeroInput = this.querySelector('input[name="nombre_pasajero"]');
        if (pasajeroInput) {
            this.querySelector('input[name="nombre_pasajero"]').value = pasajeroInput.value;
        }
    });
});