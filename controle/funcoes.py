from controle.models import Contrato


def is_traje_disponivel(traje):
    mostrar = True
    itens_usados = traje.item_set.select_related()
    for item_usado in itens_usados:

        locados = item_usado.locacao_set.select_related()
        for location in locados:
            if location.status in ('Alocado', 'Atraso'):
                mostrar = False
                break
    if mostrar and traje.ativo == 'sim':
        return traje

def busca_locacao_por_contrato(contrato):
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
    else:
        # Contrato não encontrado
        contrato = '#ERRO1'

def busca_contrato_por_telefone(telefone):
    pass