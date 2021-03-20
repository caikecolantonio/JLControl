from django import forms

class ConsultarCliente(forms.Form):
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

class ConsultarClienteNovo(forms.Form):
    CPF = forms.IntegerField(label='CPF', required=False)
    RG = forms.IntegerField(label='RG', required=False)
    Telefone = forms.IntegerField(label='Telefone', required=False)
    Nome = forms.CharField(label='Nome', required=False)
    Endereco = forms.CharField(label='Endereco', required=False)
    Email = forms.EmailField(label='email', required=False)
    DocumentoExterno = forms.CharField(label='Documento Externo', required=False)