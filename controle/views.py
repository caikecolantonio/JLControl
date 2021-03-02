from django.shortcuts import render
from controle.models import Locacao, Contrato, Traje
from controle.forms import ConsultarContrato, ConsultarTraje
from controle.funcoes import is_traje_disponivel, busca_locacao_por_contrato, busca_traje
from django.http import JsonResponse
import json

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
    locacao_detalhes = {}
    if ConsultarContratoForm.is_valid():
        campos = ConsultarContratoForm.cleaned_data
        if campos['CPF']:
            if Contrato.objects.filter(cpf=campos['CPF']):
                contrato = Contrato.objects.get(cpf=campos['CPF'])
                #Verifica se encontrou o contrato
                locacoes = busca_locacao_por_contrato(contrato)
                if locacoes:
                    locacao_detalhes = locacoes
        if campos['Telefone']:
            if len(Contrato.objects.filter(telefone=campos['Telefone'])) == 1:
                contrato = Contrato.objects.get(telefone=campos['Telefone'])
                #Verifica se encontrou o contrato
                locacoes = busca_locacao_por_contrato(contrato)
                if locacoes:
                    locacao_detalhes = locacoes
            else:
                contrato = '#ERRO001'
        if campos['Nome']:
            if Contrato.objects.filter(nome=campos['Nome']):
                contrato = Contrato.objects.get(nome=campos['Nome'])
                #Verifica se encontrou o contrato
                locacoes = busca_locacao_por_contrato(contrato)
                if locacoes:
                    locacao_detalhes = locacoes

                
                 
                

    #FORMULARIO CONSULTAR TRAJE
    ConsultarTrajeForm = ConsultarTraje(request.POST or None)
    trajes_disponiveis = []
    if ConsultarTrajeForm.is_valid():
        campos_trajes = ConsultarTrajeForm.cleaned_data
        if campos_trajes['todos']:
            todos_trajes = Traje.objects.all()
            for traje in todos_trajes:
                is_disponivel = is_traje_disponivel(traje)
                if is_disponivel:
                    trajes_disponiveis.append(is_disponivel)

        if campos_trajes['codigo']:
            trajes_disponiveis = busca_traje('codigo', campos_trajes['codigo'])

        if campos_trajes['nome']:
            trajes_disponiveis = busca_traje('nome', campos_trajes['nome'])

        if campos_trajes['modelo']:
            trajes_disponiveis = busca_traje('modelo', campos_trajes['modelo'])
        
        if campos_trajes['corte']:
            trajes_disponiveis = busca_traje('corte', campos_trajes['corte'])

    

    consultas = {
        'contrato': contrato,
        'locacoes': locacao_detalhes,
        'form': ConsultarContrato,
        'form_traje': ConsultarTraje,
        'trajes_disponiveis': trajes_disponiveis,
        'count_trajes': 1
    }


    return render(request, 'consultar.html', consultas)

def autocomplete_nome(request):
    if 'term' in request.GET:
        query = Contrato.objects.filter(nome__contains=request.GET.get('term'))
        results = list()
        for contratos in query:
            results.append(contratos.nome)
        return JsonResponse(results, safe=False)


