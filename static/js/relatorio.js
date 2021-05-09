// Script para validar campos do Form de Relatorio de locações por data
function validaCamposLocData() {
if (formLocData.dPrevFinal.value == "" || formLocData.dPrevInicial.value == "") {
    atoastAlertaGenerico("Relatório Locações por data", "Preencha a data inicial/final para visualizar o relatório.")
}
else {
    formLocData.submit()
}
}

// Script para validar campos do Form de Relatorio de Traje
function validaCamposRelTraje() {
if (formTrajeRel.codigo.value == "" && formTrajeRel.nome.value == "" && formTrajeRel.modelo.value == "" && formTrajeRel.corte.value == "") {
    atoastAlertaGenerico("Relatório por traje", "Preencha pelo menos um dos campos para pesquisar.")
}
else {
    formTrajeRel.submit()
}
}
