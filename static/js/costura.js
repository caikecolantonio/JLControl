function finalizaAjustes(id, url){
    console.log(id, url)
    url =  url + '?id=' + id

    fetch(url).then(response => {
        return response.json();
    }).then(resposta => {
        if (resposta == "200") {
        document.getElementById("testeSucess").style.display = "inline"
        }
        else if (resposta == "400"){
            atoastAlertaGenerico("Erro ao finalizar ajustes", "Traje com o ajuste já finalizado")
        }else {
        atoastAlertaGenerico("Finaliza ajustes", "Aconteceu algum erro ao finalizar o ajustes")
        }
    });
    setTimeout(function () {
        document.getElementById("testeSucess").style.display = "none"
        document.location.reload(true);
    }, 2000);      
}