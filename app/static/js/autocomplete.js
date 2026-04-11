const input = document.querySelector('input[name="q"]');
const lista = document.createElement('ul');
lista.style.cssText = 'position:absolute; top:100%; background:white; border:1px solid #ddd; list-style:none; padding:0; margin:0; width:100%; z-index:999;';
input.parentElement.style.position = 'relative';
input.parentElement.appendChild(lista);

input.addEventListener('input', async function() {
    const termo = this.value;
    if (termo.length < 2) { lista.innerHTML = ''; return; }

    const res = await fetch(`/busca/sugestoes?q=${termo}`);
    const sugestoes = await res.json();

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
});

document.addEventListener('click', e => {
    if (!input.contains(e.target)) lista.innerHTML = '';
});