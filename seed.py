import django
import os
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from faker import Faker
from validate_docbr import CPF
import random
from controle.models import Cliente


def criar_clientes(numero_clientes):
    fake = Faker('pt-br')
    Faker.seed(10)
    for x in range(numero_clientes):
        cpf = CPF()
        nome = fake.name()
        rg = "{}{}{}{}".format(random.randrange(10, 99), random.randrange(100, 999), random.randrange(100, 999),
                               random.randrange(0, 9))
        telefone = "{}{}".format(random.randrange(10000, 99999),random.randrange(100000, 999999))
        cpf = cpf.generate()
        endereco = fake.city()
        email = re.sub('[^A-Za-z0-9]+', '', nome).lower() + '@hotmail.com'
        a = Cliente(nome=nome, rg=rg, cpf=cpf, email=email, telefone=telefone, endereco=endereco)
        a.save()


criar_clientes(2)