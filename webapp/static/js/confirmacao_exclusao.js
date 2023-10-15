function deleteItem() {
    let userConfirmation = confirm("Você tem certeza de que deseja deletar este item?");
    var resultado = false;
    if(userConfirmation) {
        resultado = true;
    }
    return resultado;
}