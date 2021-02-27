from django import forms

class ConsultarContrato(forms.Form):
    cpf = forms.IntegerField(label='CPF', required=False)
    telefone = forms.IntegerField(label='Telefone', required=False)
    nome = forms.CharField(label='Nome', required=False)
    documento_externo = forms.CharField(label='Documento Externo', required=False)

class ConsultarTraje(forms.Form):
    nome = forms.CharField(label='Nome', required=False)
    modelo = forms.CharField(label='Modelo', required=False)
    corte = forms.CharField(label='Corte', required=False)
    todos = forms.BooleanField(label='Consultar Todos Disponíveis', required=False)
