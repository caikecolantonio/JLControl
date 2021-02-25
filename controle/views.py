from django.shortcuts import render
from controle.models import Locacao
from controle.models import Contrato
from controle.forms import ConsultarContrato

# Create your views here.

def devolver(request):
    pass

def locar(request):
    pass

def cancelar(request):
    pass

def consultar(request):
    ConsultarContratoForm = ConsultarContrato(request.POST or None)
    contrato, locacao, items = None,None,None
    if  ConsultarContratoForm.is_valid:
        for cpf in ConsultarContratoForm.data.items():
            if 'cpf' in cpf:
                if cpf[1] != '':
                   contrato = Contrato.objects.get(cpf=cpf[1])
                   #Verifica se encontrou o contrato
                   if contrato:
                        locacao = contrato.locacao_set.select_related()
                        #items = locacao.item
                   else:
                       contrato = 'Nenhum contrato encontrado'
                else:
                    contrato = 'CPF não digitado'
            
    
    consultas = {
        'contrato': contrato,
        'locacoes': locacao,
        'itens':items,
        'form': ConsultarContrato,
    }


    return render(request, 'consultar.html', consultas)



