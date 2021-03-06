from django.contrib import admin
from .models import Locacao, Item, Ficha, Lancamento, Traje, Cliente

# Register your models here.

admin.site.register(Locacao)
admin.site.register(Item)
admin.site.register(Ficha)
admin.site.register(Traje)
admin.site.register(Lancamento)
admin.site.register(Cliente)
