from django.db import models
# Create your models here.

class Contrato(models.Model):
    nome = models.CharField(max_length=100, null=False)
    rg = models.IntegerField(null=True)
    cpf = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    telefone = models.IntegerField()
    descricao = models.CharField(max_length=3000, null=True, blank=True)
    documento_externo = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.nome.capitalize()

class Lancamento(models.Model):
    data = models.DateField(auto_now=False, auto_now_add=False)
    hora = models.TimeField(auto_now=False, auto_now_add=False)
    valor = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.id)

class Traje(models.Model):
    codigo = models.CharField(max_length=20, null=False, unique=True)
    nome = models.CharField(max_length=80, null=False)
    modelo = models.CharField(max_length=80, null=False)
    corte = models.CharField(max_length=80, null=False)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    ATIVO_CHOISE = [
        ('nao', 'Não'),
        ('sim', 'Sim'),
    ]
    ativo = models.CharField(choices=ATIVO_CHOISE, max_length=100, default='sim')


    def __str__(self):
        return self.nome.capitalize() + ' - ' + self.corte.capitalize() + ' - ' + 'R$' + str(self.valor)

class Ficha(models.Model):
    paleto_barra = models.DecimalField(max_digits=5, decimal_places=2)
    calca_barra = models.DecimalField(max_digits=5, decimal_places=2)
    torax = models.DecimalField(max_digits=5, decimal_places=2)
    costas = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.id)

class Item(models.Model):
    quantidade = models.IntegerField()
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    STATUS_CHOISE = [
        ('Pronto', 'Pronto'),
        ('Aguardando', 'Aguardando'),
    ]
    status = models.CharField(choices=STATUS_CHOISE, max_length=100)
    data_entrega = models.DateTimeField(auto_now=False, auto_now_add=False)
    medidas = models.ForeignKey(Ficha, on_delete=models.CASCADE, null=True, blank=True)
    traje = models.ForeignKey(Traje, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.traje.nome + ' - ' + self.status

class Locacao(models.Model):
    data_locacao = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    data_previsao_devolucao = models.DateTimeField(auto_now=False, auto_now_add=False)
    STATUS_CHOISE = [
        ('Alocado', 'Alocado'),
        ('Devolvido', 'Devolvido'),
        ('Atraso', 'Em Atraso'),
    ]
    status = models.CharField(choices=STATUS_CHOISE, max_length=100)
    item = models.ManyToManyField(Item)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    lancamento = models.ForeignKey(Lancamento, on_delete=models.CASCADE)
    def __str__(self):

        return str(self.id) + ' - ' + self.contrato.nome + ' - Data Devolução: ' + str(self.data_devolucao.strftime("%d-%m-%Y %H:%M:%S"))