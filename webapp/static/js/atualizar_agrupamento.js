function atualizar_subgrupo() {
    // localiza os select
    grupo_select = document.getElementById('grupo');
    subgrupo_select = document.getElementById('subgrupo');
    // coleta o id
    grupo_id = grupo_select.value;
    // solicita ao servidor a lista de locais a partir de um setor
    fetch('/sistema/subgrupo_lista/' + grupo_id).then(function(response) {
        response.json().then(function(data) {
            optionHTML = '';
            // criar lista atualizada
            for (subgrupo of data.subgrupo_lista) {
                optionHTML += '<option value="' + subgrupo.id +'">' + subgrupo.nome + '</option>'
            }
            // insere a lista no select de locais
            subgrupo_select.innerHTML = optionHTML;
        });
    });
}


document.addEventListener('DOMContentLoaded', function () {
    const agrupamentoModal = document.getElementById('agrupamentoModal');
    agrupamentoModal.addEventListener('show.bs.modal', function (event) {

        const listItem = event.relatedTarget;
        const tipo = listItem.getAttribute('data-tipo');
        const grupo_id = listItem.getAttribute('data-grupo-id');
        const subgrupo_id = listItem.getAttribute('data-subgrupo-id');
        const agp_nome = listItem.getAttribute('data-nome');

        const modal_tipo = document.getElementById('agp_tipo');
        const modal_grupo_id = document.getElementById('agp_grupo_id');
        const modal_subgrupo_id = document.getElementById('agp_subgrupo_id');
        const modal_agp_nome = document.getElementById('agp_nome');
        const modal_titulo = document.getElementById('agrupamentoModalLabel');

        modal_tipo.value = tipo;
        modal_grupo_id.value = grupo_id;
        modal_subgrupo_id.value = subgrupo_id;
        modal_agp_nome.value = agp_nome;
        modal_titulo.textContent = 'Atualizar ' + tipo;
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const localizacaoModal = document.getElementById('localizacaoModal');
    localizacaoModal.addEventListener('show.bs.modal', function (event) {

        const listItem = event.relatedTarget;
        const localizacao_tipo = listItem.getAttribute('data-tipo');
        const localizacao_id = listItem.getAttribute('data-id');
        const localizacao_sigla = listItem.getAttribute('data-sigla');
        const localizacao_nome = listItem.getAttribute('data-nome');

        const modal_tipo = document.getElementById('localizacao_tipo');
        const modal_id = document.getElementById('localizacao_id');
        const modal_sigla = document.getElementById('localizacao_sigla');
        const modal_nome = document.getElementById('localizacao_nome');
        const modal_titulo = document.getElementById('localizacaoModalLabel');

        modal_tipo.value = localizacao_tipo;
        modal_id.value = localizacao_id;
        modal_sigla.value = localizacao_sigla;
        modal_nome.value = localizacao_nome;
        modal_titulo.textContent = 'Atualizar ' + localizacao_tipo;
    });
});