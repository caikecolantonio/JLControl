from django.contrib import admin
from .models import Locacao, Item, Ficha, Lancamento, Traje, Cliente

# Register your models here.


class Locacoes(admin.ModelAdmin):
    list_display= ('cliente', 'data_locacao', 'data_previsao_devolucao', 'data_devolucao', 'status', 'descricao', 'lancamento')
    list_display_links = ('data_locacao', 'data_devolucao', 'data_previsao_devolucao', 'status', 'descricao', 'cliente', 'lancamento')
    search_fields = ('cliente', 'status')
    list_per_page = 20
    
admin.site.register(Locacao, Locacoes)
admin.site.register(Item)
admin.site.register(Ficha)

class Trajes(admin.ModelAdmin):
    list_display = ('codigo', 'modelo', 'nome', 'valor', 'ativo')
    list_display_links = ('codigo', 'modelo', 'nome', 'valor', 'ativo')
    search_fields = ('codigo', 'modelo', 'nome')
    list_per_page = 20

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Traje, Trajes)

class Lancamentos(admin.ModelAdmin):
    list_display = ('id', 'data', 'hora', 'valor')
    list_display_links = ('id', 'data', 'hora', 'valor')
    list_per_page = 20

admin.site.register(Lancamento, Lancamentos)
admin.site.register(Cliente)
