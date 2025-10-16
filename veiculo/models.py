from django.db import models
from django.contrib.auth.models import User
from veiculo.consts import OPCOES_MARCAS, OPCOES_COR, OPCOES_COMBUSTIVEL

# Create your models here.
class Veiculo(models.Model):
    marca = models.SmallIntegerField(choices=OPCOES_MARCAS)
    modelo = models.CharField(max_length=100)
    ano = models.SmallIntegerField()
    cor = models.SmallIntegerField(choices=OPCOES_COR)
    combustivel = models.SmallIntegerField(choices=OPCOES_COMBUSTIVEL)
    foto = models.ImageField( blank=True, null=True , upload_to='veiculo/fotos')

class Anuncio(models.Model):
    TIPO_CHOICES = [
        ('venda', 'Venda'),
        ('troca', 'Troca'),
    ]
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('vendido', 'Vendido'),
        ('pausado', 'Pausado'),
    ]
    
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='anuncios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='anuncios')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(max_length=1000)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quilometragem = models.IntegerField(help_text="Quilometragem em KM")
    tipo_anuncio = models.CharField(max_length=10, choices=TIPO_CHOICES, default='venda')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')
    telefone = models.CharField(max_length=15)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    visualizacoes = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
    
    def __str__(self):
        return f"{self.titulo} - R$ {self.preco}"
