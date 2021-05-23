$(function(){
    $('.button-checkbox').each(function(){
		var $widget = $(this),
			$button = $widget.find('button'),
			$checkbox = $widget.find('input:checkbox'),
			color = $button.data('color'),
			settings = {
					on: {
						icon: 'glyphicon glyphicon-check'
					},
					off: {
						icon: 'glyphicon glyphicon-unchecked'
					}
			};

		$button.on('click', function () {
			$checkbox.prop('checked', !$checkbox.is(':checked'));
			$checkbox.triggerHandler('change');
			updateDisplay();
		});

		$checkbox.on('change', function () {
			updateDisplay();
		});

		function updateDisplay() {
			var isChecked = $checkbox.is(':checked');
			// Set the button's state
			$button.data('state', (isChecked) ? "on" : "off");

			// Set the button's icon
			$button.find('.state-icon')
				.removeClass()
				.addClass('state-icon ' + settings[$button.data('state')].icon);

			// Update the button's color
			if (isChecked) {
				$button
					.removeClass('btn-default')
					.addClass('btn-' + color + ' active');
			}
			else
			{
				$button
					.removeClass('btn-' + color + ' active')
					.addClass('btn-default');
			}
		}
		function init() {
			updateDisplay();
			// Inject the icon if applicable
			if ($button.find('.state-icon').length == 0) {
				$button.prepend('<i class="state-icon ' + settings[$button.data('state')].icon + '"></i> ');
			}
		}
		init();
	});
});

async function esqueci(url) {
	if (document.getElementById("id_username").value == ""){
		 document.getElementById("submit").click()
		}
	else{
 		url = url+'?user=' + document.getElementById("id_username").value
		 document.getElementById("gamb").style.display = "inline"
		 document.getElementById("gambtext").innerHTML = "Enviando solicitação, espere por favor"
		await fetch(url).then(response => {
		  return response.json();
		}).then(resposta => {
			if (resposta == 200){
				alert("Nova senha enviada para o email.")
			}
			else if (resposta == 400){
				alert("Usuario não encontrado.")
			}
			else if (resposta == 402){
				alert("Erro no envio do email")
			}
			else if (resposta == 401){
				alert("Usuario sem e-mail, por favor contatar o administrador.")
			}
		});
		document.getElementById("gamb").style.display = "none"
		
	}
	
}