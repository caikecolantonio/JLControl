function validaCampos() {
  if (formContrato.CPF.value == '' && formContrato.Telefone.value == '' && formContrato.Nome.value == '' && formContrato.DocumentoExterno.value == '') {
    document.getElementById("botaoAlerta").click();
  }
  else {
    formContrato.submit();
  }
}
