from django import forms

class ConsultarContrato(forms.Form):
    CPF = forms.IntegerField(label='CPF', required=False)
    Telefone = forms.IntegerField(label='Telefone', required=False)
    Nome = forms.CharField(label='Nome', required=False)
    DocumentoExterno = forms.CharField(label='Documento Externo', required=False)

class ConsultarTraje(forms.Form):
    codigo = forms.CharField(label='Codigo', required=False)
    nome = forms.CharField(label='Nome', required=False)
    modelo = forms.CharField(label='Modelo', required=False)
    corte = forms.CharField(label='Corte', required=False)
    todos = forms.BooleanField(label='todos controle', required=False)
    alocados = forms.BooleanField(label='Consultar os alocados', required=False)
