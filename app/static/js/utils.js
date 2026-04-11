function alterarQtd(btn, delta) {
    const input = btn.closest('div').querySelector('input[name="quantidade"]');
    const novoValor = parseInt(input.value) + delta;
    const min = parseInt(input.min);
    const max = parseInt(input.max);

    if (novoValor >= min && novoValor <= max) {
        input.value = novoValor;
    }
}

function alterarQtdCarrinho(btn, delta) {
    const input = btn.closest('div').querySelector('input[name="quantidade"]');
    const novoValor = parseInt(input.value) + delta;
    const min = parseInt(input.min);
    const max = parseInt(input.max);

    if (novoValor >= min && novoValor <= max) {
        input.value = novoValor;
    }
}

function confirmarRemocao(btn) {
    const input = btn.closest('form').querySelector('input[name="quantidade"]');
    const qtdRemover = parseInt(input.value);
    const qtdAtual = parseInt(btn.dataset.atual);

    if (qtdRemover >= qtdAtual) {
        return confirm('Isso vai remover este item do carrinho. Tem certeza?');
    }

    return true;
}