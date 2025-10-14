from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from veiculo.models import Veiculo
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from veiculo.forms import FormularioVeiculo
from django.db.models import Q  # <<---- IMPORTE O Q
from django.views import View
from django.http import FileResponse , Http404
from django.core.exceptions import ObjectDoesNotExist


class ListarVeiculos(LoginRequiredMixin, ListView):
    """
    View para listar os veículos cadastrados.
    """
    model = Veiculo
    context_object_name = 'lista_veiculos'
    template_name = 'veiculo/listar.html'

    def get_queryset(self):
        """
        Sobrescreve o método original para adicionar o filtro de busca.
        """
        queryset = super().get_queryset().order_by('-id')
        
        # Pega o valor do campo 'busca' da URL
        busca = self.request.GET.get('busca')
        
        # Se houver um valor para 'busca', filtra os resultados
        if busca:
            # Filtra por modelo OU placa que contenham o termo da busca
            queryset = queryset.filter(modelo__icontains=busca)
                
            
        return queryset

class CriarVeiculo(LoginRequiredMixin, CreateView):
    """
    View para criar um novo veículo.
    """
    model = Veiculo
    form_class = FormularioVeiculo
    template_name = 'veiculo/novo.h.html'
    template_name = 'veiculo/novo.html'
    success_url = reverse_lazy('listar-veiculos')

class FotoVeiculo(View):
    """
    Class Based View para exibir a foto do veículo.
    """
    def get(self, request, arquivo):

        try:
            veiculo = Veiculo.objects.get(foto='veiculo/fotos/{}'.format(arquivo))
            return FileResponse(veiculo.foto)
        except Veiculo.DoesNotExist:
            raise Http404('Foto não encontrada.')
        except Exception as exception:
            raise exception
        
class EditarVeiculo(LoginRequiredMixin, UpdateView):
    """
    View para editar um veículo existente.
    """
    model = Veiculo
    form_class = FormularioVeiculo
    template_name = 'veiculo/editar.html'
    success_url = reverse_lazy('listar-veiculos')
    pk_url_kwarg = 'pk'

class ApagarVeiculo(LoginRequiredMixin, DeleteView):
    """
    View para apagar um veículo existente.
    """
    model = Veiculo
    template_name = 'veiculo/apagar.html'
    success_url = reverse_lazy('listar-veiculos')
    pk_url_kwarg = 'pk'       

class AnunciarVeiculo(LoginRequiredMixin, ListView):
    """
    View para listar os veículos disponíveis para anúncio.
    """
    model = Veiculo
    context_object_name = 'lista_veiculos'
    template_name = 'veiculo/anunciar.html'

    def get_queryset(self):
        """
        Sobrescreve o método original para adicionar o filtro de busca.
        """
        queryset = super().get_queryset().order_by('-id')
        
        # Pega o valor do campo 'busca' da URL
        busca = self.request.GET.get('busca')
        
        # Se houver um valor para 'busca', filtra os resultados
        if busca:
            # Filtra por modelo OU placa que contenham o termo da busca
            queryset = queryset.filter(Q(modelo__icontains=busca) | Q(placa__icontains=busca))
                
            
        return queryset