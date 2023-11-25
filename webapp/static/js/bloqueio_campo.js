$('#tipodata').on('change', function() {
        // Obtém o valor selecionado
        var selectedValue = $(this).val();
        // Verifica se o 1 = DATA_FIXA, 2 = DATA_MÓVEL
        if (selectedValue == 2) {
            // Bloqueia o campo cancelamento_data
            $('#cancelamento_data').prop('disabled', true);
        } else {
            // Desbloqueia o campo cancelamento_data
            $('#cancelamento_data').prop('disabled', false);
        }
    });