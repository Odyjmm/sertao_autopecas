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

function toggleMenu() {
    const links = document.getElementById('navbar-links');
    links.classList.toggle('aberto');
}

document.addEventListener('click', function(e) {
    const navbar = document.querySelector('.navbar');
    const btn = document.getElementById('menu-btn');
    if (!navbar.contains(e.target)) {
        document.getElementById('navbar-links').classList.remove('aberto');
    }
});