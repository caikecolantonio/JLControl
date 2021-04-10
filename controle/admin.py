from django.contrib import admin
from .models import Locacao, Item, Ficha, Lancamento, Traje, Cliente

# Register your models here.


class Locacoes(admin.ModelAdmin):
    list_display= ('data_locacao', 'data_devolucao', 'data_previsao_devolucao', 'status', 'descricao', 'cliente', 'lancamento')
    list_display_links = ('data_locacao', 'data_devolucao', 'data_previsao_devolucao', 'status', 'descricao', 'cliente', 'lancamento')
    search_fields = ('cliente', 'status')
    list_per_page = 20
admin.site.register(Locacao, Locacoes)
admin.site.register(Item)
admin.site.register(Ficha)
admin.site.register(Traje)
admin.site.register(Lancamento)
admin.site.register(Cliente)
