from django.shortcuts import render
from controle.models import Locacao
from controle.forms import ConsultarLocacoes

# Create your views here.

def devolver(request):
    pass

def locar(request):
    pass

def cancelar(request):
    pass

def consultar(request):

    consulta = Locacao.objects.all()
    consultas = {
        'consulta': consulta,
        'form': ConsultarLocacoes,
    }


    return render(request, 'consultar.html', consultas)

