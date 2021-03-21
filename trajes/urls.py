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
from controle.views import devolver, locar, consultar, cancelar, autocomplete_nome, autocomplete_traje, retornaTrajeSelecionado
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('devolver/', devolver),
    path('locar/', locar, name= 'locar'),
    path('cancelar/', cancelar),
    path('', consultar),
    path('consultar/', consultar),
    path('autocomplete-nome/', autocomplete_nome, name='autocomplete-nome'),
    path('autocomplete-traje/', autocomplete_traje, name='autocomplete-traje'),
    path('retornatrajeselecionado/', retornaTrajeSelecionado, name='retornaTrajeSelecionado')
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
