//abre e configura alerta de Toast 
function atoastAlertaGenerico(titulo, mensagem) {
  var numero = parseInt(Math.random() * (2000 - 0) + 0)

  var seuNode = document.getElementById('toastAlertaGenerico');
  var clone = seuNode.cloneNode(true);
  clone.id = "toastAlertaGenerico-" + numero

  for (childs in clone.childNodes) {
    if (typeof clone.childNodes[childs]["childNodes"] !== 'undefined' && clone.childNodes[childs]["childNodes"].length > 0) {
      for (dentro in clone.childNodes[childs]["childNodes"]) {
        clone.childNodes[childs]["childNodes"][dentro].id = clone.childNodes[childs]["childNodes"][dentro].id + "-" + numero
        if (typeof clone.childNodes[childs]["childNodes"][dentro].parentNode !== 'undefined') {
          clone.childNodes[childs]["childNodes"][dentro].parentNode.id = clone.childNodes[childs]["childNodes"][dentro].parentNode.id + "-" + numero
        }
      }
    }
  }
  document.getElementById("areaToast").appendChild(clone);
  var fadeToast = new bootstrap.Toast(document.getElementById("toastAlertaGenerico-" + numero));
  fadeToast.show();
  document.getElementById("toastTitulo-" + numero).innerHTML = titulo
  document.getElementById("toastMensagem-" + numero).innerHTML = mensagem
  document.getElementById("buttonFechaToast-" + numero).setAttribute("onClick", "ftoastAlertaGenerico(" + numero + ")")
  document.getElementById("timer-" + numero).classList.add("timer")
  document.getElementById("timer-" + numero).setAttribute("name", Date.now())

  clone.addEventListener('hidden.bs.toast', function () {
    setTimeout(function () {
      clone.parentNode.removeChild(clone)
    }, 200);
  })
}
// Fecha Toast
function ftoastAlertaGenerico(numero) {
  $("#toastAlertaGenerico-" + numero).toast('hide')
}

// Atualiza segundos de todos os Toast da tela
function AtualizaDataToast() {
  var toastTimers = document.getElementsByClassName("timer");
  for (timer in toastTimers) {
    if (typeof toastTimers[timer] == "object") {
      toastTimers[timer].innerHTML = parseInt((Date.now() - toastTimers[timer].getAttribute("name")) / 1000) + " seg atrás"
    }
  }
}
setInterval(AtualizaDataToast, 100);