from controle.models import Locacao, Contrato, Traje

def is_traje_disponivel(traje, MostraAlocados):
    mostrar = False
    itens_usados = traje.item_set.select_related()
    if not itens_usados and not MostraAlocados:
        mostrar = True

    for item_usado in itens_usados:
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
            
            

# retorna um dicionario de todas as locações e itens das locações por contrato
# recebe objeto contrato
def busca_locacao_por_contrato(contrato):
    locacao_detalhes = {}
    QntLocacao = 0
    for locacoes in contrato.locacao_set.select_related().values():
        QntLocacao += 1
        locacao_detalhes[QntLocacao] = locacoes
        locacaoRelacionados = Locacao.objects.filter(id=locacoes['id']).select_related()
        locacao_detalhes[QntLocacao]['item'] = {}
        count = 0
        for locacao in locacaoRelacionados:
            items = locacao.item.all().values()
            for trajes in items:
                count += 1
                locacao_detalhes[QntLocacao]['item'][count] = trajes
    
    if locacao_detalhes:
        return locacao_detalhes

def busca_traje(tipo, pesquisa, MostraAlocados):
    volta = []
    todos_trajes = Traje.objects.filter(**{tipo: pesquisa})
    for traje in todos_trajes:
        is_disponivel = is_traje_disponivel(traje, MostraAlocados)
        if is_disponivel:
            volta.append(is_disponivel)
    return volta

def busca_contrato_por_telefone(telefone):
    pass
