from rest_framework import serializers
from .models import Veiculo

class SerializadorVeiculo(serializers.ModelSerializer):
    """
    Serializador para o modelo Veiculo.
    """

    class Meta:
        model = Veiculo
        exclude = []