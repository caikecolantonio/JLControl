from django import forms

class ConsultarLocacoes(forms.Form):
    cpf = forms.IntegerField(label='cpf', required=False)
    telefone = forms.IntegerField(label='telefone', required=False)
    nome = forms.CharField(label='nome', required=False)
    documento_externo = forms.CharField(label='documento-externo', required=False)

