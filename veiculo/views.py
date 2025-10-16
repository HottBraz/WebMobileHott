from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from veiculo.models import Veiculo, Anuncio
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from veiculo.forms import FormularioVeiculo, FormularioAnuncio
from django.db.models import Q, F  # <<---- IMPORTE O Q e F
from django.views import View
from django.http import FileResponse , Http404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


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

class ListarAnuncios(ListView):
    """
    View para listar todos os anúncios ativos.
    """
    model = Anuncio
    context_object_name = 'lista_anuncios'
    template_name = 'veiculo/anuncios.html'
    paginate_by = 12

    def get_queryset(self):
        """
        Filtra apenas anúncios ativos e adiciona busca.
        """
        queryset = Anuncio.objects.filter(status='ativo').select_related('veiculo', 'usuario')
        
        # Filtros de busca
        busca = self.request.GET.get('search')  # Alterado de 'busca' para 'search'
        cidade = self.request.GET.get('cidade')
        preco_min = self.request.GET.get('preco_min')
        preco_max = self.request.GET.get('preco_max')
        
        if busca:
            queryset = queryset.filter(
                Q(titulo__icontains=busca) | 
                Q(veiculo__modelo__icontains=busca) |
                Q(descricao__icontains=busca)
            )
        
        if cidade:
            queryset = queryset.filter(cidade__icontains=cidade)
            
        if preco_min:
            queryset = queryset.filter(preco__gte=preco_min)
            
        if preco_max:
            queryset = queryset.filter(preco__lte=preco_max)
        
        return queryset

class DetalheAnuncio(DetailView):
    """
    View para exibir detalhes de um anúncio específico.
    """
    model = Anuncio
    template_name = 'veiculo/detalhe_anuncio.html'
    context_object_name = 'anuncio'

    def get_object(self):
        """
        Incrementa o contador de visualizações.
        """
        obj = get_object_or_404(Anuncio, pk=self.kwargs['pk'], status='ativo')
        # Incrementa visualizações
        Anuncio.objects.filter(pk=obj.pk).update(visualizacoes=F('visualizacoes') + 1)
        return obj

class CriarAnuncio(LoginRequiredMixin, CreateView):
    """
    View para criar um novo anúncio.
    """
    model = Anuncio
    form_class = FormularioAnuncio
    template_name = 'veiculo/criar_anuncio.html'
    success_url = reverse_lazy('listar-anuncios')

    def form_valid(self, form):
        """
        Define o usuário logado como autor do anúncio.
        """
        form.instance.usuario = self.request.user
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        """
        Filtra apenas veículos que não possuem anúncios ativos.
        """
        form = super().get_form(form_class)
        # Filtrar veículos que não têm anúncios ativos
        veiculos_com_anuncios = Anuncio.objects.filter(status='ativo').values_list('veiculo_id', flat=True)
        form.fields['veiculo'].queryset = Veiculo.objects.exclude(id__in=veiculos_com_anuncios)
        return form

class EditarAnuncio(LoginRequiredMixin, UpdateView):
    """
    View para editar um anúncio existente.
    """
    model = Anuncio
    form_class = FormularioAnuncio
    template_name = 'veiculo/editar_anuncio.html'
    success_url = reverse_lazy('meus-anuncios')

    def get_queryset(self):
        """
        Permite editar apenas anúncios do usuário logado.
        """
        return Anuncio.objects.filter(usuario=self.request.user)

class MeusAnuncios(LoginRequiredMixin, ListView):
    """
    View para listar anúncios do usuário logado.
    """
    model = Anuncio
    template_name = 'veiculo/meus_anuncios.html'
    context_object_name = 'anuncios'
    paginate_by = 10

    def get_queryset(self):
        """
        Filtra anúncios do usuário logado com filtros opcionais.
        """
        queryset = Anuncio.objects.filter(usuario=self.request.user).select_related('veiculo')
        
        # Filtros opcionais
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        tipo = self.request.GET.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo_anuncio=tipo)
        
        return queryset.order_by('-data_criacao')
    
    def get_context_data(self, **kwargs):
        """
        Adiciona estatísticas ao contexto.
        """
        context = super().get_context_data(**kwargs)
        user_anuncios = Anuncio.objects.filter(usuario=self.request.user)
        
        context['anuncios_ativos'] = user_anuncios.filter(status='ativo').count()
        context['anuncios_pausados'] = user_anuncios.filter(status='pausado').count()
        context['anuncios_vendidos'] = user_anuncios.filter(status='vendido').count()
        
        return context

class ApagarAnuncio(LoginRequiredMixin, DeleteView):
    """
    View para apagar um anúncio.
    """
    model = Anuncio
    template_name = 'veiculo/apagar_anuncio.html'
    success_url = reverse_lazy('meus-anuncios')

    def get_queryset(self):
        """
        Permite apagar apenas anúncios do usuário logado.
        """
        return Anuncio.objects.filter(usuario=self.request.user)