from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
from veiculo.models import *
from veiculo.forms import *

class VeiculoTests(TestCase):

    def setUp(self):
        self.instancia = Veiculo(
            marca=1,
            modelo='ABCDE',
            ano=datetime.now().year,
            cor=2,
            combustivel=3
        )

    def test_is_new(self):
        self.assertTrue(self.instancia.veiculo_novo)
        self.instancia.ano = datetime.now().year - 5
        self.assertFalse(self.instancia.veiculo_novo)

    def test_years_of_use(self):
        self.instancia.ano = datetime.now().year - 10
        self.assertEqual(self.instancia.anos_de_uso(), 10)

class TestesViewListarVeiculos(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345@teste')
        self.client.force_login(self.user)
        self.url = reverse('listar-veiculos')
        Veiculo(marca=1, modelo='ABCDE', ano=2020, cor=3, combustivel=4).save()

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['lista_veiculos']), 1)

class TestesViewCriarVeiculo(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345@teste')
        self.client.force_login(self.user)
        self.url = reverse('criar-veiculo')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], FormularioVeiculo)

    def test_post(self):
        dados = {
            'marca': 1,
            'modelo': 'ABCDE',
            'ano': 2020,
            'cor': 3,
            'combustivel': 4
        }
        response = self.client.post(self.url, dados)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-veiculos'))

        self.assertEqual(Veiculo.objects.count(), 1)
        self.assertEqual(Veiculo.objects.first().modelo, 'ABCDE')

class TestesViewEditarVeiculo(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345@teste')
        self.client.force_login(self.user)
        self.veiculo = Veiculo.objects.create(marca=1, modelo='ABCDE', ano=2020, cor=3, combustivel=4)
        self.url = reverse('editar-veiculo', kwargs={'pk': self.veiculo.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['object'], Veiculo)
        self.assertIsInstance(response.context['form'], FormularioVeiculo)
        self.assertEqual(response.context['object'].pk, self.veiculo.pk)
        self.assertEqual(response.context['object'].marca, 1)

    def test_post(self):
        data = {
            'marca': 5, 'modelo': 'FGHIJ', 'ano': 2021, 'cor': 2, 'combustivel': 1
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-veiculos'))
        self.assertEqual(Veiculo.objects.count(), 1)
        self.assertEqual(Veiculo.objects.first().marca, 5)
        self.assertEqual(Veiculo.objects.first().pk, self.veiculo.pk) 

class TestesViewApagarVeiculo(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345@teste')
        self.client.force_login(self.user)
        self.intancia = Veiculo.objects.create(marca=1, modelo='ABCDE', ano=2020, cor=3, combustivel=4)
        self.url = reverse('apagar-veiculo', kwargs={'pk': self.intancia.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['object'], Veiculo)
        self.assertEqual(response.context['object'].pk, self.intancia.pk)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-veiculos'))
        self.assertEqual(Veiculo.objects.count(), 0)