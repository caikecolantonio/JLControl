from django.shortcuts import render
from controle.models import Locacao, Cliente, Traje, Ficha, Lancamento
from controle.forms import ConsultarCliente, ConsultarTraje, FormFicha
from controle.funcoes import is_traje_disponivel, busca_locacao_por_cliente, busca_traje, validate_cpf, criar_cliente, \
    criar_locacao, procura_ou_cria_cliente
from django.http import JsonResponse
from django.forms.models import model_to_dict
from datetime import datetime
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
                # Verifica se encontrou o cliente pelo o cpf
                locacoes = busca_locacao_por_cliente(cliente)
                if locacoes:
                    locacao_detalhes = locacoes
        if campos['Telefone']:
            if len(Cliente.objects.filter(telefone=campos['Telefone'])) == 1:
                cliente = Cliente.objects.get(telefone=campos['Telefone'])
                # Verifica se encontrou o cliente pelo o telefone
                locacoes = busca_locacao_por_cliente(cliente)
                if locacoes:
                    locacao_detalhes = locacoes
            else:
                cliente = '#ERRO001'
        if campos['Nome']:
            if Cliente.objects.filter(nome=campos['Nome']):
                cliente = Cliente.objects.get(nome=campos['Nome'])
                # Verifica se encontrou o cliente pelo o nome
                locacoes = busca_locacao_por_cliente(cliente)
                if locacoes:
                    locacao_detalhes = locacoes

    # FORMULARIO CONSULTAR TRAJE
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

def consultar_avancado(request):
          
    if 'dados' in request.POST:
        lista = list(request.POST['dados'].split(","))
        locacoes = Locacao.objects.filter(id__in=lista)

    else:
        datainicial = request.POST['datainicial']
        datafinal = request.POST['datafinal']
        status = request.POST['status']
        if status == 'todos':
            locacoes = Locacao.objects.filter(data_locacao__range=(datainicial, datafinal))
        else:
            locacoes = Locacao.objects.filter(data_locacao__range=(datainicial, datafinal), status=status)

    locacao_detalhes = {}
    QntLocacao = 0
    if locacoes:
        for locacao in locacoes:
            QntLocacao += 1
            locacao_detalhes[QntLocacao] = locacao.__dict__
            locacao_detalhes[QntLocacao]['cliente'] = Cliente.objects.get(id=locacao.cliente_id)
            #Aqui a mesma coisa, pode ter mais de um Item, prepara o Dicionario.
            locacao_detalhes[QntLocacao]['item'] = {}
            count = 0
            items = locacao.item.all().values()
            #Pega todas as informações dos Trajes.
            for traje in items:
                count += 1
                traje["traje"] = Traje.objects.get(id=traje["traje_id"])
                if traje["medidas_id"] != None and traje["medidas_id"] != "":
                    traje["medida"] = Ficha.objects.get(id=traje["medidas_id"])
                else:
                    traje["medida"] = None
                #Adiciona a informação do Traje no dicionario de retorno.
                locacao_detalhes[QntLocacao]['item'][count] = traje

    consultas = {
        'locacoes': locacao_detalhes
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
        query = Traje.objects.filter(**{request.GET.get('tipo') + "__contains": request.GET.get('term')})
        results = list()
        for trajes in query:
            # Verifica se já não adicionou, não faz sentido aparecer varias vezes
            if request.GET.get('Unifica') == 'True':
                if getattr(trajes, request.GET.get('tipo')) not in results:
                    results.append(getattr(trajes, request.GET.get('tipo')))
            else:
                trajeDisponivel = is_traje_disponivel(trajes, False)
                if trajeDisponivel != None:
                    results.append("Codigo:" + trajeDisponivel.codigo + " Modelo: " + trajeDisponivel.modelo)
        return JsonResponse(results, safe=False)


def cria_ficha_medidas(request):
    try:
        info = json.loads(request.GET.get('info'))
        ficha = Ficha(paleto_barra=float(info['paleto_barra']), calca_barra=float(info['calca_barra']),
                      torax=float(info['torax']), costas=float(info['costas']))
        ficha.save()
        return JsonResponse(ficha.id, safe=False)
    except:
        return JsonResponse("status 400", safe=False)


def retornaTrajeSelecionado(request):
    query = Traje.objects.filter(codigo=request.GET.get('Traje'))
    if query:
        for traje in query:
            trajeDisponivel = is_traje_disponivel(traje, False)
            if trajeDisponivel:
                return JsonResponse(model_to_dict(trajeDisponivel), safe=False)
            return JsonResponse("NAODISPONIVEL", safe=False)
    else:
        return JsonResponse("CODIGOINVALIDO", safe=False)


def salvar_locacao(request):
    infoCliente = json.loads(request.GET.get('form'))
    listaTrajes = json.loads(request.GET.get('listatraje'))
    dataPrevisao = request.GET.get('dPrevDevolucao')
    valorTotal = request.GET.get('valorTotal')
    retorno = {}

    if infoCliente['isEstrangeiro'] == False:
        if validate_cpf(infoCliente['CPF']):
            cliente = procura_ou_cria_cliente(infoCliente, "cpf", infoCliente['CPF'])
        else:
            cliente = procura_ou_cria_cliente(infoCliente, "cpf", infoCliente['CPF'])
            # return JsonResponse("CPF digitado invalido", safe=False)
    else:
        cliente = procura_ou_cria_cliente(infoCliente, "documento_externo", infoCliente['DocumentoExterno'])

    if criar_locacao(cliente, dataPrevisao, listaTrajes, valorTotal) == 200:
        retorno["id_cliente"] = cliente.id
        retorno["status"] = 200

        return JsonResponse(retorno, safe=False)
    else:
        retorno["id_cliente"] = cliente.id
        retorno["status"] = 400
        return JsonResponse(retorno, safe=False)


def devolver_locacao(request):
    try:
        id_locacao = json.loads(request.GET.get('id_locacao'))
        locacao = Locacao.objects.get(id=id_locacao)
        if locacao.status != 'Devolvido':
            locacao.status = 'Devolvido'
            locacao.data_devolucao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            locacao.save()
            return JsonResponse("200", safe=False)
        else:
            return JsonResponse("400", safe=False)
    except:
        return JsonResponse("deu ruim", safe=False)


def atualizar_ficha(request):
    try:
        infoFicha = json.loads(request.GET.get('infoFicha'))
        ficha = Ficha.objects.get(id=infoFicha["id"])
        ficha.paleto_barra = infoFicha["paleto_barra"]
        ficha.calca_barra = infoFicha["calca_barra"]
        ficha.torax = infoFicha["torax"]
        ficha.costas = infoFicha["costas"]
        ficha.save()
        return JsonResponse("200", safe=False)
    except:
        return JsonResponse("deu ruim", safe=False)


def consultar_cliente(request):
    cliente = Cliente.objects.get(id=request.GET.get('id'))
    locacao_detalhes = busca_locacao_por_cliente(cliente)
    consultas = {
        'cliente': cliente,
        'locacoes': locacao_detalhes
    }
    return render(request, 'consultar.html', consultas)


def consulta_ficha_medida(request):
    ficha = Ficha.objects.get(id=request.GET.get('id'))
    return JsonResponse(model_to_dict(ficha), safe=False)

def relatorio(request):
    return render(request, 'relatorio.html')


def mais_menos_alocados(request):
    locacoes = Locacao.objects.all()
    trajes = {}
    for locacao in locacoes:
        items = locacao.item.all().values()
        for item in items:
            codigo = Traje.objects.get(id=item["traje_id"])
            if codigo in trajes:
                trajes[codigo] += 1
            else:
                trajes[codigo] = 1

    maximo = max(trajes, key=trajes.get)
    minimo = min(trajes, key=trajes.get)
    trajes = {k: v for k, v in sorted(trajes.items(), key=lambda item: item[1], reverse=True)}
    relatorio = {
        'maximo': [maximo, trajes[maximo]],
        'minimo': [minimo, trajes[minimo]],
        'trajes': trajes
    }

    return render(request, 'resultado-max-min.html', relatorio)


def busca_por_data(request):
    locacao, loc_atrasada, loc_alocado, loc_devolvido = [], [], [], []
    locacoes = Locacao.objects.filter(
        data_locacao__range=(request.POST['dPrevInicial'], request.POST['dPrevFinal']))
    locacoes_atrasadas = Locacao.objects.filter(status='Atraso', data_locacao__range=(
    request.POST['dPrevInicial'], request.POST['dPrevFinal']))
    locacoes_alocado = Locacao.objects.filter(status='Alocado', data_locacao__range=(
    request.POST['dPrevInicial'], request.POST['dPrevFinal']))
    locacoes_devolvido = Locacao.objects.filter(status='Devolvido', data_locacao__range=(
    request.POST['dPrevInicial'], request.POST['dPrevFinal']))

    if locacoes:
        for x in locacoes:
            locacao.append(x)

    if locacoes_atrasadas:
        for x in locacoes_atrasadas:
            loc_atrasada.append(x)

    if locacoes_alocado:
        for x in locacoes_alocado:
            loc_alocado.append(x)

    if locacoes_devolvido:
        for x in locacoes_devolvido:
            loc_devolvido.append(x)

    resultados = {
        'locacao': len(locacao),
        'locacoes_atrasadas': len(loc_atrasada),
        'locacoes_alocado': len(loc_alocado),
        'locacoes_devolvido': len(loc_devolvido),
    }
    return render(request, 'resultado-datas.html', resultados)

def busca_por_traje(request):
    trajes = []
    if request.POST['nome'] != '':
        pesquisa = request.POST['nome']
        tipo = 'nome'
    if request.POST['corte'] != '':
        pesquisa = request.POST['corte']
        tipo = 'corte'
    if request.POST['modelo'] != '':
        pesquisa = request.POST['modelo']
        tipo = 'modelo'
    if request.POST['codigo'] != '':
        pesquisa = request.POST['codigo']
        tipo = 'codigo'
    trajes = busca_traje(tipo, pesquisa, True)
    trajes += busca_traje(tipo, pesquisa, False)
    resultados= {
        'trajes' : trajes
    }
    return render(request, 'busca-por-traje.html', resultados)

def busca_financeiro(request):
    valores = 0
    if request.GET.get('data-inicial') != '':
        data_inicial = request.GET.get('data-inicial')
    if request.GET.get('data-final') != '':
        data_final = request.GET.get('data-final')
    if request.GET.get('hora') != '':
        hora = request.GET.get('hora')
    lancamentos = Lancamento.objects.filter(data__range=(
    data_inicial, data_final))
    for lanc in lancamentos:
        valores += lanc.valor
    resultados = {
        'lancamentos': len(lancamentos),
        'valores': valores
    }
    return JsonResponse(resultados, safe=False)
