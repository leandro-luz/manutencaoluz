function pesquisar_cnpj() {
    cnpj_select = document.getElementById('cnpj')
    var cnpj = cnpj_select.value.replace(/\D/g, '');

    //Verifica se campo cep possui valor informado.
        if (cnpj != "") {
            //Expressão regular para validar o CNPJ.
            var validacnpj = /^[0-9]{14}$/;

             //Valida o formato do CEP.
            if(validacnpj.test(cnpj)) {
                //Preenche os campos com "..." enquanto consulta webservice.

                document.getElementById('razao_social').value="...";
                document.getElementById('nome_fantasia').value="...";
                document.getElementById('data_abertura').value="...";
                document.getElementById('situacao').value="...";
                document.getElementById('porte').value="...";
                document.getElementById('nome_responsavel').value="...";
                document.getElementById('natureza_juridica').value="...";
                document.getElementById('cnae_principal').value="...";
                document.getElementById('cnae_principal_texto').value="...";
                document.getElementById('inscricao_estadual').value="...";
                document.getElementById('inscricao_municipal').value="...";
                document.getElementById('cep').value="...";
                document.getElementById('numero').value="...";
                document.getElementById('complemento').value="...";
                document.getElementById('logradouro').value="...";
                document.getElementById('bairro').value="...";
                document.getElementById('municipio').value="...";
                document.getElementById('uf').value="...";
                document.getElementById('localizacao').value="...";
                document.getElementById('email').value="...";
                document.getElementById('telefone').value="...";

                //Cria um elemento javascript.
                var script_cnpj = document.createElement('script');

                //Sincroniza com o callback.
                script_cnpj.src = 'https://receitaws.com.br/v1/cnpj/' + cnpj +'?callback=callback_cnpj';

                //Insere script no documento e carrega o conteúdo.
                document.body.appendChild(script_cnpj);
            }
            else {
                //cnpj é inválido.
                limpa_formulário_cnpj();
                alert("CNPJ inválido");
            }
        }
        else {
            limpa_formulário_cnpj();
        }
    }


function limpa_formulário_cnpj() {
        //Limpa valores do formulário de cnpj.
        document.getElementById('razao_social').value="";
        document.getElementById('nome_fantasia').value="";
        document.getElementById('data_abertura').value="";
        document.getElementById('situacao').value="";
        document.getElementById('porte').value="";
        document.getElementById('nome_responsavel').value="";
        document.getElementById('natureza_juridica').value="";
        document.getElementById('cnae_principal').value="";
        document.getElementById('cnae_principal_texto').value="";
        document.getElementById('inscricao_estadual').value="";
        document.getElementById('inscricao_municipal').value="";
        document.getElementById('cep').value="";
        document.getElementById('numero').value="";
        document.getElementById('complemento').value="";
        document.getElementById('logradouro').value="";
        document.getElementById('bairro').value="";
        document.getElementById('municipio').value="";
        document.getElementById('uf').value="";
        document.getElementById('localizacao').value="";
        document.getElementById('email').value="";
        document.getElementById('telefone').value="";
}


function callback_cnpj(conteudo_cnpj) {
    if (!("erro" in conteudo_cnpj)) {
        //Atualiza os campos com os valores.
        document.getElementById('razao_social').value=(conteudo_cnpj.nome);
        document.getElementById('nome_fantasia').value=(conteudo_cnpj.fantasia);

        //document.getElementById('data_abertura').value=((conteudo_cnpj.abertura);

        document.getElementById('situacao').value=(conteudo_cnpj.situacao);
        document.getElementById('porte').value=(conteudo_cnpj.porte);
        document.getElementById('natureza_juridica').value=(conteudo_cnpj.natureza_juridica);
        document.getElementById('cnae_principal').value=(conteudo_cnpj.atividade_principal[0]['code']);
        document.getElementById('cnae_principal_texto').value=(conteudo_cnpj.atividade_principal[0]['text']);
        document.getElementById('cep').value=(conteudo_cnpj.cep);
        document.getElementById('numero').value=(conteudo_cnpj.numero);
        document.getElementById('complemento').value=(conteudo_cnpj.complemento);
        document.getElementById('logradouro').value=(conteudo_cnpj.logradouro);
        document.getElementById('bairro').value=(conteudo_cnpj.bairro);
        document.getElementById('municipio').value=(conteudo_cnpj.municipio);
        document.getElementById('uf').value=(conteudo_cnpj.uf);
        document.getElementById('nome_responsavel').value=(conteudo_cnpj.qsa[0]['nome']);
        document.getElementById('email').value=(conteudo_cnpj.email);
        document.getElementById('telefone').value=(conteudo_cnpj.telefone);

    } //end if.
    else {
        //CEP não Encontrado.
        limpa_formulário_cnpj();
        alert("CNPJ não encontrado");
    }
}
