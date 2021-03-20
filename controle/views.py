from django.shortcuts import render
from controle.models import Locacao, Cliente, Traje
from controle.forms import ConsultarCliente, ConsultarTraje
from controle.funcoes import is_traje_disponivel, busca_locacao_por_cliente, busca_traje
from django.http import JsonResponse
import json

# Create your views here.

def devolver(request):
    pass

def locar(request):
    cliente = None
    if request.method == 'POST':
        ConsultarClienteForm = ConsultarCliente(request.POST)
        
        if ConsultarClienteForm.is_valid():
            campos = ConsultarClienteForm.cleaned_data
            if campos['CPF']:
                if Cliente.objects.filter(cpf=campos['CPF']):
                    cliente = Cliente.objects.get(cpf=campos['CPF'])
            if campos['Telefone']:
                if len(Cliente.objects.filter(telefone=campos['Telefone'])) == 1:
                    cliente = Cliente.objects.get(telefone=campos['Telefone'])
                else:
                    cliente = '#ERRO001'
            if campos['Nome']:
                if Cliente.objects.filter(nome=campos['Nome']):
                    cliente = Cliente.objects.get(nome=campos['Nome'])
            
            if cliente == None:
                cliente = 0
    
    consultas = {
        'cliente': cliente
    }
    return render(request, 'locar.html', consultas)

def cancelar(request):
    pass

def consultar(request):
    ConsultarClienteForm = ConsultarCliente(request.POST)
    cliente = None
    locacao_detalhes = {}
    if ConsultarClienteForm.is_valid():
        campos = ConsultarClienteForm.cleaned_data
        if campos['CPF']:
            if Cliente.objects.filter(cpf=campos['CPF']):
                cliente = Cliente.objects.get(cpf=campos['CPF'])
                #Verifica se encontrou o cliente pelo o cpf
                locacoes = busca_locacao_por_cliente(cliente)
                if locacoes:
                    locacao_detalhes = locacoes
        if campos['Telefone']:
            if len(Cliente.objects.filter(telefone=campos['Telefone'])) == 1:
                cliente = Cliente.objects.get(telefone=campos['Telefone'])
                #Verifica se encontrou o cliente pelo o telefone
                locacoes = busca_locacao_por_cliente(cliente)
                if locacoes:
                    locacao_detalhes = locacoes
            else:
                cliente = '#ERRO001'
        if campos['Nome']:
            if Cliente.objects.filter(nome=campos['Nome']):
                cliente = Cliente.objects.get(nome=campos['Nome'])
                #Verifica se encontrou o cliente pelo o nome
                locacoes = busca_locacao_por_cliente(cliente)
                if locacoes:
                    locacao_detalhes = locacoes

                
                 
                

    #FORMULARIO CONSULTAR TRAJE
    ConsultarTrajeForm = ConsultarTraje(request.POST)
    trajes_disponiveis = []
    entrou = False
    MostraAlocados = None

    if request.method == 'POST' and ConsultarTrajeForm.is_valid() and not ConsultarClienteForm.has_changed():
        campos_trajes = ConsultarTrajeForm.cleaned_data
        MostraAlocados = (True if campos_trajes['alocados'] else False)
        if campos_trajes['codigo']:
            trajes_disponiveis = busca_traje('codigo', campos_trajes['codigo'], MostraAlocados)
            entrou = True

        if campos_trajes['nome']:
            trajes_disponiveis = busca_traje('nome', campos_trajes['nome'], MostraAlocados)
            entrou = True

        if campos_trajes['modelo']:
            trajes_disponiveis = busca_traje('modelo', campos_trajes['modelo'], MostraAlocados)
            entrou = True

        if campos_trajes['corte']:
            trajes_disponiveis = busca_traje('corte', campos_trajes['corte'], MostraAlocados)
            entrou = True

        if not entrou:
            todos_trajes = Traje.objects.all()
            for traje in todos_trajes:
                is_disponivel = is_traje_disponivel(traje, MostraAlocados)
                if is_disponivel:
                    trajes_disponiveis.append(is_disponivel)

    

    consultas = {
        'cliente': cliente,
        'locacoes': locacao_detalhes,
        'form': ConsultarCliente,
        'form_traje': ConsultarTraje,
        'trajes_disponiveis': trajes_disponiveis,
        'MostraAlocados': MostraAlocados,
        'count_trajes': 1,
        'paginaConsultar': '/consultar/'
    }


    return render(request, 'consultar.html', consultas)

def autocomplete_nome(request):
    if 'term' in request.GET:
        query = Cliente.objects.filter(nome__contains=request.GET.get('term'))
        results = list()
        for clientes in query:
            results.append(clientes.nome)
        return JsonResponse(results, safe=False)

def autocomplete_traje(request):
    if 'term' in request.GET:
        #                               Pega o "Tipo" que é qual atributo que ele vai buscar
        query = Traje.objects.filter(**{request.GET.get('tipo')+"__contains": request.GET.get('term')})
        results = list()
        for trajes in query:
            #Verifica se já não adicionou, não faz sentido aparecer varias vezes
            if request.GET.get('Unifica') == 'True':
                if getattr(trajes,request.GET.get('tipo')) not in results:
                    results.append(getattr(trajes,request.GET.get('tipo')))
            else:
                trajeDisponivel = is_traje_disponivel(trajes, False)
                if trajeDisponivel != None:
                    results.append("Codigo:" + trajeDisponivel.codigo+ " Modelo: "+ getattr(trajeDisponivel,request.GET.get('tipo')))
        return JsonResponse(results, safe=False)

def retornaTrajeSelecionado(request):
    return JsonResponse(list(Traje.objects.filter(codigo=request.GET.get('Traje')[7:request.GET.get('Traje').index(" ")]).values()), safe=False)


