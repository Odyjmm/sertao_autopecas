document.addEventListener('DOMContentLoaded', () => {

    const forms = document.querySelectorAll('form[action="/carrinho/adicionar"]');

    forms.forEach(form => {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            const formData = new FormData(this);

            try {
                await fetch('/carrinho/adicionar', {
                    method: 'POST',
                    body: formData
                });

                // Toast
                const toast = document.getElementById('toast');
                if (toast) {
                    toast.style.display = 'block';
                    setTimeout(() => {
                        toast.style.display = 'none';
                    }, 1000);
                }

                atualizarContadorCarrinho();

            } catch (error) {
                console.error('Erro ao adicionar ao carrinho:', error);
            }
        });
    });

    async function atualizarContadorCarrinho() {
        try {
            const res = await fetch('/carrinho/quantidade');
            const data = await res.json();

            const badge = document.getElementById('badge-carrinho');

            if (!badge) return;

            if (data.total > 0) {
                badge.textContent = data.total;
                badge.style.display = 'flex';
            } else {
                badge.style.display = 'none';
            }

        } catch (error) {
            console.error('Erro ao atualizar carrinho:', error);
        }
    }

    atualizarContadorCarrinho();

});