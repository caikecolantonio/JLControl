function abreModalConfirma(id, acao, event){
    event.stopPropagation();
    document.getElementById("botaoSimConfirma").onclick = function(event) {
      devolver_ou_cancelar_locacao(id, acao)
    }

    $('#confirmacao').modal('toggle')
    if (acao == 1){
      document.getElementById("confirmaTitulo").innerHTML = "Voce deseja devolver a locação?" 
    }
    if (acao == 2){
      document.getElementById("confirmaTitulo").innerHTML = "Voce deseja cancelar a locação?" 
    }
  }

  function fechaModalConfirma(){
    $('#confirmacao').modal('hide')
}