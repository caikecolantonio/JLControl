from django import forms

class ConsultarContrato(forms.Form):
    cpf = forms.IntegerField(label='cpf', required=False)
    telefone = forms.IntegerField(label='telefone', required=False)
    nome = forms.CharField(label='nome', required=False)
    documento_externo = forms.CharField(label='documento-externo', required=False)

class ConsultarTraje(forms.Form):
    nome = forms.CharField(label='nome', required=False)
    modelo = forms.CharField(label='modelo', required=False)
    corte = forms.CharField(label='corte', required=False)

