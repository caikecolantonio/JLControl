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
    contrato, locacoes, items = None,None,None
    locacao_detalhes = {}
    if  ConsultarContratoForm.is_valid:
        for cpf in ConsultarContratoForm.data.items():
            if 'cpf' in cpf:
                if cpf[1] != '':
                   contrato = Contrato.objects.get(cpf=cpf[1])
                   #Verifica se encontrou o contrato
                   if contrato:
                        QntLocacao = 0
                        for locacoes in contrato.locacao_set.select_related().values():
                            QntLocacao += 1
                            locacao_detalhes[QntLocacao] = locacoes
                            locacaoRelacionados = Locacao.objects.filter(id=locacoes['id']).select_related()
                            locacao_detalhes[QntLocacao]['item'] = {}
                            count = 0
                            for locacao in locacaoRelacionados:
                                items  = locacao.item.all().values()
                                for trajes in items:
                                    count += 1
                                    locacao_detalhes[QntLocacao]['item'][count] = trajes
                   else:
                       contrato = 'Nenhum contrato encontrado'
                else:
                    contrato = 'CPF não digitado'
            
    
    consultas = {
        'contrato': contrato,
        'locacoes': locacao_detalhes,
        'form': ConsultarContrato,
    }


    return render(request, 'consultar.html', consultas)



