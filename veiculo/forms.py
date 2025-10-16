from django import forms
from django.forms import ModelForm
from veiculo.models import Veiculo, Anuncio

class FormularioVeiculo(ModelForm):
    """ 
    Formulário para o modelo Veiculo
    """

    class Meta:
        model = Veiculo
        fields = ['marca', 'modelo', 'ano', 'cor', 'combustivel', 'foto']
        widgets = {
            'marca': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecione a marca'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o modelo do veículo'
            }),
            'ano': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o ano do veículo',
                'min': 1900,
                'max': 2025
            }),
            'cor': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecione a cor'
            }),
            'combustivel': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecione o combustível'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'marca': 'Marca',
            'modelo': 'Modelo',
            'ano': 'Ano',
            'cor': 'Cor',
            'combustivel': 'Combustível',
            'foto': 'Foto do Veículo'
        }
    
    def clean_ano(self):
        """
        Validação customizada para o campo ano
        """
        ano = self.cleaned_data.get('ano')
        if ano and (ano < 1900 or ano > 2025):
            raise forms.ValidationError('O ano deve estar entre 1900 e 2025.')
        return ano
    
    def clean_modelo(self):
        """
        Validação customizada para o campo modelo
        """
        modelo = self.cleaned_data.get('modelo')
        if modelo and len(modelo.strip()) < 2:
            raise forms.ValidationError('O modelo deve ter pelo menos 2 caracteres.')
        return modelo.strip() if modelo else modelo

class FormularioAnuncio(ModelForm):
    """
    Formulário para o modelo Anuncio
    """

    class Meta:
        model = Anuncio
        fields = ['veiculo', 'titulo', 'descricao', 'preco', 'quilometragem', 
                  'tipo_anuncio', 'telefone', 'cidade', 'estado']
        widgets = {
            'veiculo': forms.Select(attrs={
                'class': 'form-control',
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Civic 2020 impecável, baixa quilometragem'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva as características, estado de conservação, acessórios...'
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'quilometragem': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quilometragem em KM'
            }),
            'tipo_anuncio': forms.Select(attrs={
                'class': 'form-control',
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da cidade'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: São Paulo, SP'
            }),
        }
        labels = {
            'veiculo': 'Veículo',
            'titulo': 'Título do Anúncio',
            'descricao': 'Descrição',
            'preco': 'Preço (R$)',
            'quilometragem': 'Quilometragem',
            'tipo_anuncio': 'Tipo',
            'telefone': 'Telefone de Contato',
            'cidade': 'Cidade',
            'estado': 'Estado',
        }
    
    def clean_preco(self):
        """
        Validação para preço
        """
        preco = self.cleaned_data.get('preco')
        if preco and preco <= 0:
            raise forms.ValidationError('O preço deve ser maior que zero.')
        return preco
    
    def clean_quilometragem(self):
        """
        Validação para quilometragem
        """
        km = self.cleaned_data.get('quilometragem')
        if km and km < 0:
            raise forms.ValidationError('A quilometragem não pode ser negativa.')
        return km
    
    def clean_telefone(self):
        """
        Validação básica para telefone
        """
        telefone = self.cleaned_data.get('telefone')
        if telefone and len(telefone) < 10:
            raise forms.ValidationError('Digite um telefone válido.')
        return telefone

