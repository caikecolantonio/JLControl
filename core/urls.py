"""trajes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from controle.views import costura, locar, consultar, cancelar, autocomplete_nome, autocomplete_traje, \
    retornaTrajeSelecionado, salvar_locacao, cria_ficha_medidas, devolver_locacao, cancelar_locacao, atualizar_ficha, consultar_cliente, \
    consulta_ficha_medida, relatorio, mais_menos_alocados, busca_por_data, busca_por_traje,busca_financeiro, consultar_avancado, finaliza_ajustes
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('locar/', locar, name= 'locar'),
    path('cancelar/', cancelar),
    path('relatorio/', relatorio, name='relatorio'),
    path('', consultar),
    path('consultar/', consultar),
    path('costura/', costura, name= 'costura'),
    path('consultar_avancado/', consultar_avancado),
    path('autocomplete-nome/', autocomplete_nome, name='autocomplete-nome'),
    path('autocomplete-traje/', autocomplete_traje, name='autocomplete-traje'),
    path('retornatrajeselecionado/', retornaTrajeSelecionado, name='retornaTrajeSelecionado'),
    path('salvar-locacao/', salvar_locacao, name='SalvarLocacao'),
    path('cria_ficha_medidas/', cria_ficha_medidas, name='cria_ficha_medidas'),
    path('devolver-locacao/', devolver_locacao, name='devolver_locacao'),
    path('cancelar_locacao/', cancelar_locacao, name='cancelar_locacao'),
    path('atualiza-ficha/', atualizar_ficha, name='atualizar_ficha'),
    path('consulta-cliente/', consultar_cliente, name='consultar_cliente'),
    path('consulta-ficha-medida/', consulta_ficha_medida, name='consulta_ficha_medida'),
    path('mais-menos-alocados', mais_menos_alocados, name='mais-menos-alocados'),
    path('busca-por-data/', busca_por_data, name="busca-por-data"),
    path('busca-por-traje/', busca_por_traje, name="busca_por_traje"),
    path('finaliza-ajustes/', finaliza_ajustes, name="finaliza_ajustes"),
    path('busca-financeiro/', busca_financeiro, name="busca-financeiro")
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
