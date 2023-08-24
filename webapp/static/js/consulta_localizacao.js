function atualizar_locais() {
    // localiza os select
    setor_select = document.getElementById('setor');
    local_select = document.getElementById('local');
    // coleta o id
    setor_id = setor_select.value;
    // solicita ao servidor a lista de locais a partir de um setor
    fetch('/sistema/local_setor_lista/' + setor_id).then(function(response) {
        response.json().then(function(data) {
            optionHTML = '';
            // criar lista atualizada
            for (local of data.locais_lista) {
                optionHTML += '<option value="' + local.id +'">' + local.nome + '</option>'
            }
            // insere a lista no select de locais
            local_select.innerHTML = optionHTML;
        });
    });
}
