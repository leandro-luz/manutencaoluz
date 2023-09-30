function coletar_valores_atividade(value) {

    var value = value;
    var resultado = true;
    var limite = 2;
    // Variavel para armazenar o tabela final
    var kvpairs = [];
    // Definindo o formulario a ser coletado as informações
    var form = document.forms.form_atividade;
//    var formData = new FormData(form);

    // alterando o limitador de elementos
    if (value) {
        limite = 1;
    }

    // percorrendo por todos os elementos na tela
    for(var i = 1; i < form.elements.length-limite; i++) {
        // variavel que recebe os elementos
        var e = form.elements[i];

        // variavel que recebe a chave
        var chave = encodeURIComponent(e.name);
        // variavel que recebe o valor
        var valor = encodeURIComponent(e.value);
        // verifica se o valor não foi preenchido

        if (value == true) {
            if(chave == 'observacao' && valor == '') {
                resultado = false;
            }
        } else {
            if ((chave == 'valorbinario_id' && valor == 0) || (valor == '')) {
                resultado = false;
            }
        }
        // concotenando a chave e valor
        kvpairs.push(chave + ": " + valor);
    }

    var queryString = kvpairs.join(";");
    document.getElementById("valores").value = queryString;
    // verifica se o resultado e false e emite uma mensagem
    if (resultado == false) {
        alert("Algum campo não preenchido!");
    }
    return resultado;
}