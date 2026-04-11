document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('input[name="quantidade"]').forEach(input => {
        input.addEventListener('change', function () {
            const min = parseInt(this.min);
            const max = parseInt(this.max);
            let valor = parseInt(this.value);

            if (isNaN(valor) || valor < min) this.value = min;
            if (valor > max) this.value = max;
        });
    });

});