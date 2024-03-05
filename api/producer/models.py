from django.db import models

from utils.choices import BRAZIL_STATES, CROPS


class Crop(models.Model):

    type = models.CharField(
        verbose_name='Nome',
        max_length=2,
        choices=CROPS,
    )
    producer = models.ForeignKey(verbose_name='Produtor', to='producer.Producer', on_delete=models.CASCADE, related_name='crops')

    def __str__(self):
        return self.type


class Producer(models.Model):

    # Producer info
    register_number = models.CharField(
        verbose_name='Número de registro (CPF/CNPJ)',
        max_length=20,
    )
    name = models.CharField(
        verbose_name='Nome',
        max_length=100
    )

    # Farm info
    farm_name = models.CharField(
        verbose_name='Nome da fazenda',
        max_length=100
    )
    city = models.CharField(
        verbose_name='Cidade',
        max_length=100
    )
    state = models.CharField(
        verbose_name='Estado',
        max_length=2,
        choices=BRAZIL_STATES,
    )
    total_area = models.DecimalField(
        verbose_name='Área total',
        max_digits=10,
        decimal_places=2,
    )
    arable_area = models.DecimalField(
        verbose_name='Área agriculturável',
        max_digits=10,
        decimal_places=2,
    )
    vegetation_area = models.DecimalField(
        verbose_name='Área de vegetação',
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return self.name
