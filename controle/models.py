from django.db import models
# Create your models here.

class Cliente(models.Model):
    nome = models.CharField(max_length=100, null=False)
    rg = models.IntegerField(null=True, blank=True)
    cpf = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    telefone = models.IntegerField()
    documento_externo = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nome.capitalize()

class Lancamento(models.Model):
    data = models.DateField(auto_now=False, auto_now_add=False)
    hora = models.TimeField(auto_now=False, auto_now_add=False)
    valor = models.DecimalField(max_digits=7, decimal_places=2)

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
        return self.nome.capitalize() + ' - ' + self.corte.capitalize() + ' - ' + self.modelo.capitalize() + ' - ' +'R$' + str(self.valor)

class Ficha(models.Model):
    paleto_barra = models.DecimalField(max_digits=5, decimal_places=2)
    calca_barra = models.DecimalField(max_digits=5, decimal_places=2)
    torax = models.DecimalField(max_digits=5, decimal_places=2)
    costas = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.id)

class Item(models.Model):
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    STATUS_CHOISE = [
        ('Pronto', 'Pronto'),
        ('Aguardando', 'Aguardando'),
    ]
    status = models.CharField(choices=STATUS_CHOISE, max_length=100)
    data_entrega = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
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
    descricao = models.CharField(max_length=3000, null=True, blank=True)
    item = models.ManyToManyField(Item)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    lancamento = models.ForeignKey(Lancamento, on_delete=models.CASCADE)
    def __str__(self):

        return str(self.id) + ' - ' + self.cliente.nome