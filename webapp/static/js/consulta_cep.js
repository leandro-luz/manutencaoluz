function pesquisar_cep() {
    cep_select = document.getElementById('cep')
    var cep = cep_select.value.replace(/\D/g, '');
    //Verifica se campo cep possui valor informado.
        if (cep != "") {
            //Expressão regular para validar o CEP.
            var validacep = /^[0-9]{8}$/;

             //Valida o formato do CEP.
            if(validacep.test(cep)) {

                 //Preenche os campos com "..." enquanto consulta webservice.
                document.getElementById('numero').value="...";
                document.getElementById('complemento').value="...";
                document.getElementById('logradouro').value="...";
                document.getElementById('bairro').value="...";
                document.getElementById('municipio').value="...";
                document.getElementById('uf').value="...";

                //Cria um elemento javascript.
                var script_cep = document.createElement('script');

                //Sincroniza com o callback.
                script_cep.src = 'https://viacep.com.br/ws/'+ cep + '/json/?callback=callback_cep';

                //Insere script no documento e carrega o conteúdo.
                document.body.appendChild(script_cep);
            }
            else {
                //cep é inválido.
                limpa_formulário_cep();
                alert("Formato de CEP inválido.");
            }
        }
        else {
            limpa_formulário_cep();
        }
    }


function limpa_formulário_cep() {
        //Limpa valores do formulário de cep.
        document.getElementById('numero').value="";
        document.getElementById('complemento').value="";
        document.getElementById('logradouro').value="";
        document.getElementById('bairro').value="";
        document.getElementById('municipio').value="";
        document.getElementById('uf').value="";
}

function callback_cep(conteudo) {
    if (!("erro" in conteudo)) {
        //Atualiza os campos com os valores.
        document.getElementById('logradouro').value=(conteudo.logradouro);
        document.getElementById('bairro').value=(conteudo.bairro);
        document.getElementById('municipio').value=(conteudo.localidade);
        document.getElementById('uf').value=(conteudo.uf);
    } //end if.
    else {
        //CEP não Encontrado.
        limpa_formulário_cep();
        alert("CEP não encontrado.");
    }
}
