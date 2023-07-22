function exportar_lista(nome_arquivo,colunas) {
    // Variavel para armazenar o tabela final
    var csv_data = [];
    // Total de linhas, incluíndo os títulos
    var rows = document.getElementsByTagName('tr');
    for (var i = 0; i < rows.length; i++) {
        // Total de colunas
        var cols = rows[i].querySelectorAll('td,th');
        // Variavel para armazenar os valores das linhas
        var csvrow = [];
        for (var j = 0; j < cols.length-colunas; j++) {
            // Armazena os valores de cada celula
            csvrow.push(cols[j].innerHTML);
        }
        // Insere um separador entre as celulas
        csv_data.push(csvrow.join(";"));
    }
    // Insere o separador de linhas
    csv_data = csv_data.join('\n');
    // função para gerar o arquivo csv
    downloadCSVFile(csv_data,nome_arquivo);
}

function downloadCSVFile(csv_data, nome_arquivo) {
    // Cria um arquivo csv
    CSVFile = new Blob([csv_data], {
        type: "text/csv;charset=utf-8;"
    });

    // Create to temporary link to initiate
    // download process
    var temp_link = document.createElement('a');

    // Download csv file
    temp_link.download = nome_arquivo;
    var url = window.URL.createObjectURL(CSVFile);
    temp_link.href = url;

    // This link should not be displayed
    temp_link.style.display = "none";
    document.body.appendChild(temp_link);

    // Automatically click the link to
    // trigger download
    temp_link.click();
    document.body.removeChild(temp_link);
}
