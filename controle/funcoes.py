from controle.models import Locacao, Cliente, Traje

#Função que busca se o traje está disponivel ou alocado
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
        locacao_detalhes[QntLocacao]['item'] = {}
        count = 0
        for locacao in locacaoRelacionados:
            items = locacao.item.all().values()
            #Pega todas as informações dos Trajes.
            for trajes in items:
                count += 1
                #Adiciona a informação do Traje no dicionario de retorno.
                locacao_detalhes[QntLocacao]['item'][count] = trajes
    
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

