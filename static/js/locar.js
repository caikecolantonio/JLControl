
// Na pagina Locar, botão Encontrar Cliente se modal não estiver 1 preenchido, mostra msg
function validaCamposLocar() {
    if (formClienteLocar.CPF.value == '' && formClienteLocar.Telefone.value == '' && formClienteLocar.Nome.value == '' && formClienteLocar.DocumentoExterno.value == '') {
        document.getElementById("botaoAlerta").click();
    } else {
        formClienteLocar.submit();
    }
}

//Script que mostra ou esconde as infos de cliente estrangeiro
function Esconde(value) {
    if (document.getElementById("isEstrangeiro").checked) {
        document.getElementById("FormNovoCPF").id = "DocumentoExterno"
        document.getElementById("DocumentoExterno").placeholder = "Documento Externo"
        document.getElementById("DocumentoExterno").name = "DocumentoExterno"
        document.getElementById("DocumentoExterno").maxLength = "50"
        document.getElementById("DocumentoExterno").value = ""
        document.getElementById("labelNovoCPF").innerHTML = "Documento Externo"
        document.getElementById("FormNovoRG").style.visibility = "hidden"
        document.getElementById("labelNovoRG").style.visibility = "hidden"

    } else {
        document.getElementById("DocumentoExterno").id = "FormNovoCPF"
        document.getElementById("FormNovoCPF").placeholder = "CPF"
        document.getElementById("FormNovoCPF").value = ""
        document.getElementById("FormNovoCPF").name = "CPF"
        document.getElementById("FormNovoCPF").maxLength = "11"
        document.getElementById("labelNovoCPF").innerHTML = "CPF"
        document.getElementById("FormNovoRG").style.visibility = "visible"
        document.getElementById("labelNovoRG").style.visibility = "visible"
    }
};

// Seleciona o Traje na Table (deixando azul)
function seleciona(id) {
    if (document.getElementById(id).classList.contains("table-primary")) {
        document.getElementById(id).classList.remove("table-primary")
        document.getElementById(id).classList.remove("listaSelecionada")
    } else {
        document.getElementById(id).classList.add("table-primary")
        document.getElementById(id).classList.add("listaSelecionada")
    }
}    

// Logica do botão de Precisa ajuste
function precisa_ajuste(trajeID) {
    animaBotaoMedida("botaoMedida-"+trajeID)
    for (var traje in listaTrajes) {
        if (listaTrajes[traje]["codigo"] == trajeID) {
            if (listaTrajes[traje]["precisaAjuste"] == true){
                listaTrajes[traje]["precisaAjuste"] = false
                document.getElementById("precisaAjuste"+trajeID).innerHTML = "Não precisa"
                document.getElementById("btn-check-2-outlined"+trajeID).removeAttribute("checked", null)
            }
            else {
                listaTrajes[traje]["precisaAjuste"] = true
                document.getElementById("btn-check-2-outlined"+trajeID).setAttribute("checked", "")
                document.getElementById("precisaAjuste"+trajeID).innerHTML = "  Precisa  "
            }
        }
    }
}

// Script que coloca classe no botão para anima-lo-->
function animaBotaoMedida(id)
{
    var el = document.getElementById(id);
    
    if (el.style.visibility == "visible"){
        el.style.visibility = "hidden"
    }
    else
    {
        el.style.visibility = "visible"
    }

}

//Script pra atualizar o valor de todos os trajes da table
var totalLista = 0

function AtualizaValor() {
    if (listaTrajes.length > 0){
        document.getElementById("tabelaTrajes").style.display = "table"
    }
    totalLista = 0
    //Atualiza valor
    for (var traje in listaTrajes) {
        totalLista = totalLista + parseInt(listaTrajes[traje]["valor"])
    }
    document.getElementById("trValor").innerHTML = "Total: R$" + totalLista
    //fim Atualiza valor}
}
setInterval(AtualizaValor, 300);

//Script pra remover o traje da table e da listaTrajes 
function RemoverTraje() {
    var linhas = document.getElementsByClassName("listaSelecionada");
    var linhasDeletadas = []
    for (linha in linhas) {
        if (linhas[linha].id) {
            for (traje in listaTrajes) {
                if (listaTrajes[traje]["codigo"] == linhas[linha].id) {
                    listaTrajes.splice(traje, 1);
                    linhasDeletadas.push(linhas[linha].id)
                }
            }
        }
    }
    for (id in linhasDeletadas) {
        $(document.getElementById(linhasDeletadas[id])).remove();
    }
}
