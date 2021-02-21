from django.shortcuts import render
from controle.models import Locacao

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
    }

    return render(request, 'consultar.html', consultas)

