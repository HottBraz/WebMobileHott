from django.urls import path
from veiculo.views import *
from veiculo.views import APIListarVeiculos

urlpatterns = [
    path('', ListarVeiculos.as_view(), name='listar-veiculos'),
    path('novo/', CriarVeiculo.as_view(), name='criar-veiculo'),
    path('editar/<int:pk>/', EditarVeiculo.as_view(), name='editar-veiculo'),
    path('apagar/<int:pk>/', ApagarVeiculo.as_view(), name='apagar-veiculo'),
    path('api/', APIListarVeiculos.as_view(), name='api-listar-veiculos'),

    path('fotos/<str:arquivo>/' , FotoVeiculo.as_view(), name='foto-veiculo'),
    
    # URLs para Anúncios
    path('anuncios/', ListarAnuncios.as_view(), name='listar-anuncios'),
    path('anuncio/<int:pk>/', DetalheAnuncio.as_view(), name='detalhe-anuncio'),
    path('anuncios/criar/', CriarAnuncio.as_view(), name='criar-anuncio'),
    path('anuncios/editar/<int:pk>/', EditarAnuncio.as_view(), name='editar-anuncio'),
    path('meus-anuncios/', MeusAnuncios.as_view(), name='meus-anuncios'),
    path('anuncios/apagar/<int:pk>/', ApagarAnuncio.as_view(), name='apagar-anuncio'),
]
