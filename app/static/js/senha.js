function validarSenha() {
    const senha = document.getElementById("senha").value;
    const confirmar = document.getElementById("confirmar_senha").value;

    if (senha !== confirmar) {
        alert("As senhas não coincidem!");
        return false;
    }
    return true;
}

document.getElementById("cep").addEventListener("input", function(e) {
    let valor = e.target.value.replace(/\D/g, "");

    if (valor.length > 5) {
        valor = valor.slice(0,5) + "-" + valor.slice(5,8);
    }

    e.target.value = valor;
});