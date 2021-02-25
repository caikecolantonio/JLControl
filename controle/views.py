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
    contrato = None
    if  ConsultarContratoForm.is_valid:
        cpf =  ConsultarContratoForm.data['cpf']
        if cpf != '':
            contrato = Contrato.objects.filter(cpf=cpf)
            if contrato.count == 0:
                contrato = 'Contrato não encontrado'
        else:
            contrato = 'Digite a porra do cpf'
    
    consultas = {
        'contrato': contrato,
        'form': ConsultarContrato,
    }


    return render(request, 'consultar.html', consultas)



