from django import forms
from django.forms import ModelForm
from veiculo.models import Veiculo

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

