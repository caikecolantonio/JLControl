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
    DocumentoExterno = forms.CharField(label='DocumentoExterno', required=False)

class FormFicha(forms.Form):
    paleto_barra = forms.DecimalField(label='paleto_barra', max_digits=5, decimal_places=2)
    calca_barra = forms.DecimalField(label='calca_barra', max_digits=5, decimal_places=2)
    torax = forms.DecimalField(label='torax', max_digits=5, decimal_places=2)
    costas = forms.DecimalField(label='costas', max_digits=5, decimal_places=2)