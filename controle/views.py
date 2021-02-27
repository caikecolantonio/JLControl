from django.shortcuts import render
from controle.models import Locacao,Contrato, Traje
from controle.forms import ConsultarContrato, ConsultarTraje
from controle.funcoes import is_traje_disponivel

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
    if ConsultarContratoForm.is_valid():
        for cpf in ConsultarContratoForm.data.items():
            if 'cpf' in cpf:
                if cpf[1] != '':
                    if Contrato.objects.filter(cpf=cpf[1]):
                        contrato = Contrato.objects.get(cpf=cpf[1])
                        #Verifica se encontrou o contrato
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
                        #Contrato não encontrado
                        contrato = '#ERRO1'
                else:
                    #CPF não digitado
                    contrato = '#ERRO2'

    #FORMULARIO CONSULTAR TRAJE
    ConsultarTrajeForm = ConsultarTraje(request.POST or None)
    trajes_disponiveis = []
    if ConsultarTrajeForm.is_valid():
        todos_trajes = Traje.objects.all()
        if 'todos' in ConsultarTrajeForm.data and ConsultarTrajeForm.data['todos'] in 'on':
            for traje in todos_trajes:
                is_disponivel = is_traje_disponivel(traje)
                if is_disponivel:
                    trajes_disponiveis.append(is_disponivel)


    consultas = {
        'contrato': contrato,
        'locacoes': locacao_detalhes,
        'form': ConsultarContrato,
        'form_traje': ConsultarTraje,
        'trajes_disponiveis': trajes_disponiveis,
    }


    return render(request, 'consultar.html', consultas)



