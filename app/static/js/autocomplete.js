const input = document.querySelector('input[name="q"]');

if (input) {
    input.parentElement.style.position = 'relative';

    let lista = null;

    function criarLista() {
        if (lista) return;
        lista = document.createElement('ul');
        lista.style.cssText = 'position:absolute; top:100%; background:white; border:1px solid #ddd; list-style:none; padding:0; margin:0; width:100%; z-index:998;';
        input.parentElement.appendChild(lista);
    }

    function destruirLista() {
        if (lista) {
            lista.remove();
            lista = null;
        }
    }

    let debounceTimer = null;
    let requisicaoAtual = 0;

    async function buscarSugestoes(termo) {
        const idRequisicao = ++requisicaoAtual;

        try {
            const res = await fetch(`/busca/sugestoes?q=${encodeURIComponent(termo)}`);
            const sugestoes = await res.json();

            if (idRequisicao !== requisicaoAtual) return;

            if (!sugestoes.length) {
                destruirLista();
                return;
            }

            criarLista();
            lista.innerHTML = '';
            sugestoes.forEach(s => {
                const li = document.createElement('li');
                li.textContent = s.nome;
                li.style.cssText = 'padding:8px; cursor:pointer;';
                li.addEventListener('mouseover', () => li.style.background = '#f5f5f5');
                li.addEventListener('mouseout', () => li.style.background = 'white');
                li.addEventListener('click', (e) => {
                    e.stopPropagation();
                    e.preventDefault();
                    window.location.href = `/produto/${s.id}`;
                });
                lista.appendChild(li);
            });
        } catch (error) {
            console.error('Erro ao buscar sugestões:', error);
        }
    }

    input.addEventListener('input', function() {
        const termo = this.value.trim();

        clearTimeout(debounceTimer);

        if (termo.length < 2) {
            destruirLista();
            return;
        }

        debounceTimer = setTimeout(() => buscarSugestoes(termo), 250);
    });

    document.addEventListener('click', e => {
        if (!input.contains(e.target)) destruirLista();
    });
}
