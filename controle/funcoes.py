from controle.models import Locacao, Cliente, Traje, Lancamento, Item, Ficha
from datetime import date, time, datetime
import random
import string
import keyword
import re

#"""Função que busca se o traje está disponivel ou alocado"""
#Recebe o objeto traje e o true or false do MostraAlocados.
def is_traje_disponivel(traje, MostraAlocados):
    mostrar = False
    #Verifica se esse traje está dentro de um Item
    itens_usados = traje.item_set.select_related()
    if not itens_usados and not MostraAlocados:
        #se não estiver, e não estiver mostrando os alocados, já retorna seta pra retornar o traje.
        mostrar = True
    # For de todos os Item que está relacionado a esse traje
    for item_usado in itens_usados:
        #pega a locação relacionada a esse Item
        locados = item_usado.locacao_set.select_related()
        for location in locados:
            if MostraAlocados:
                if location.status in ('Alocado', 'Atraso'):
                    mostrar = True
                    break                
            else:
                if location.status not in ('Alocado', 'Atraso') and traje.ativo == 'sim':
                    mostrar = True
                elif location.status in ('Alocado', 'Atraso') and traje.ativo == 'sim':
                    mostrar = False
                    break               
    if mostrar:
        return traje
            
            

# retorna um dicionario de todas as locações e itens das locações por cliente
# recebe objeto Cliente
def busca_locacao_por_cliente(cliente):
    locacao_detalhes = {}
    QntLocacao = 0
    #Procura as locações pela o dado do cliente, pegando os relacionados.
    for locacoes in cliente.locacao_set.select_related().values():
        QntLocacao += 1
        #Começa a montar o dicionario para realizar o retorno
        #lembrando que um cliente pode ter mais de uma locação, por isso o indice do dicionario é a quantidade de locações
        locacao_detalhes[QntLocacao] = locacoes
        #pega os Item(Trajes) relacionados com o ID da locação
        locacaoRelacionados = Locacao.objects.filter(id=locacoes['id']).select_related()
        #Aqui a mesma coisa, pode ter mais de um Item, prepara o Dicionario.
        locacao_detalhes[QntLocacao]['cliente'] = cliente
        locacao_detalhes[QntLocacao]['item'] = {}
        count = 0
        for locacao in locacaoRelacionados:
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
    
    #verifica se tem algo no Dicionario para retornar, se não tiver o return da função será None
    if locacao_detalhes:
        return locacao_detalhes

#Metodo que busca um traje no banco, pode pesquisar por qualquer atributo de um Traje.
#Parametros: Tipo = O tipo de busca, por exemplo, nome, metodo
#            pesquisa = a palavra a ser buscada
#            MostraAlocados = se vai retornar os trajes alocados ou não alocados, é true or false
def busca_traje(tipo, pesquisa, MostraAlocados):
    volta = []
    todos_trajes = Traje.objects.filter(**{tipo: pesquisa})
    for traje in todos_trajes:
        is_disponivel = is_traje_disponivel(traje, MostraAlocados)
        if is_disponivel:
            volta.append(is_disponivel)
    return volta

def validate_cpf(cpf):
    ''' Efetua a validação do CPF, tanto formatação quando dígito verificadores.

    Parâmetros:
        cpf (str): CPF a ser validado

    Retorno:
        bool:
            - Falso, quando o CPF não possuir o formato 999.999.999-99;
            - Falso, quando o CPF não possuir 11 caracteres numéricos;
            - Falso, quando os dígitos verificadores forem inválidos;
            - Verdadeiro, caso contrário.'''

    # Verifica a formatação do CPF
    if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        return False

    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True

def criar_locacao(cliente, dataPrevisao, listaTrajes, valorTotal):
    try:
        lanc = Lancamento(data=date.today(), hora=str(datetime.now().hour)+':'+str(datetime.now().minute), valor=valorTotal)
        lanc.save()
        locacao = Locacao(data_previsao_devolucao = dataPrevisao, 
        status='Alocado', 
        descricao= '', 
        cliente = cliente, 
        lancamento = lanc)
        locacao.save()
        for traje in listaTrajes:
            for verifica_traje in Traje.objects.filter(codigo=traje['codigo']):
                traje_retorno = is_traje_disponivel(verifica_traje, False)
            if not traje_retorno:
                locacao.delete()
                lanc.delete()
                return 400
            item = Item(valor=traje['valor'], 
            status='Pronto' if traje['precisaAjuste']==False else 'Aguardando', 
            data_entrega=datetime.now().strftime('%Y-%m-%d %H:%M:%S') if traje['precisaAjuste']==False else None,
            medidas=None if 'id_medida' not in traje else Ficha.objects.get(id=traje['id_medida']),
            traje = traje_retorno)
            item.save()
            locacao.item.add(item)
        return 200
    except:
        locacao.delete()
        lanc.delete()
        return 400

       
def procura_ou_cria_cliente(info, tipo, pesquisa):
    query = Cliente.objects.filter(**{tipo: pesquisa})
    if query:
        cliente = Cliente.objects.get(**{tipo: pesquisa}) 
        cliente.endereco = info["Endereco"]
        if "RG" in info:
            cliente.rg = info["RG"]
        else:
            cliente.rg = None        
        cliente.nome = info["Nome"]
        cliente.telefone = info["Telefone"]
        cliente.email = info["Email"]
        cliente.save()
        return cliente
    else:
        criar_cliente(info)
        return Cliente.objects.get(**{tipo: pesquisa})

def criar_cliente(info):
    if info['isEstrangeiro'] == True:
        cliente = Cliente(nome=info["Nome"].strip(), email=info["Email"], endereco=info["Endereco"], telefone=info["Telefone"], documento_externo=info["DocumentoExterno"])
    else:
        cliente = Cliente(nome=info["Nome"].strip(), email=info["Email"], endereco=info["Endereco"], telefone=info["Telefone"], rg=info["RG"], cpf=info["CPF"])
    cliente.save()

def remover_caracteres(recebe):
    characters_to_remove = "().-"
    pattern = "[" + characters_to_remove + "]"
    return re.sub(pattern, "", str(recebe))

def randomiza_senha():
    length = 8
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    all = lower + upper + num
    temp = random.sample(all,length)
    password = "".join(temp)
    all = string.ascii_letters + string.digits
    password = "".join(random.sample(all,length))
    return password