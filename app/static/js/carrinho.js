document.addEventListener('DOMContentLoaded', () => {

    const forms = document.querySelectorAll('form[action="/carrinho/adicionar"]');

    function mostrarToast(mensagem, tipo) {
        const toast = document.getElementById('toast');
        if (!toast) return;

        toast.textContent = mensagem;
        toast.classList.toggle('toast-erro', tipo === 'erro');
        toast.style.display = 'block';

        clearTimeout(toast._timeoutId);
        toast._timeoutId = setTimeout(() => {
            toast.style.display = 'none';
        }, tipo === 'erro' ? 3000 : 1500);
    }

    forms.forEach(form => {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            if (!usuarioLogado) {
                window.location.href = '/login?msg=carrinho';
                return;
            }

            const formData = new FormData(this);

            try {
                const resposta = await fetch('/carrinho/adicionar', {
                    method: 'POST',
                    body: formData
                });

                let dados = {};
                try {
                    dados = await resposta.json();
                } catch (e) {
                    // resposta sem corpo JSON
                }

                if (!resposta.ok) {
                    mostrarToast(dados.erro || 'Não foi possível adicionar o produto.', 'erro');
                    return;
                }

                mostrarToast('Adicionado com sucesso ✅', 'sucesso');
                atualizarContadorCarrinho();

            } catch (error) {
                console.error('Erro ao adicionar ao carrinho:', error);
                mostrarToast('Erro de conexão. Tente novamente.', 'erro');
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

    if (typeof usuarioLogado !== 'undefined' && usuarioLogado) {
        atualizarContadorCarrinho();
    }

});
