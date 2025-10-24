# -*- coding: utf-8 *-
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response



class Login(View):
    """
    Class Based View para autenticação de usuários.
    """

    def get(self,request):
        contexto = {}
        if request.user.is_authenticated:
            return redirect("/veiculo")
        else:
            return render(request, 'autenticacao.html', contexto)
    
    def post(self,request):
        # Obtem as credenciais de autenticação
        usuario = request.POST.get('usuario', None)
        senha = request.POST.get('senha', None)

        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/veiculo")
        else:
            return render(request, 'autenticacao.html', {'mensagem': 'Usuário ou senha inválidos!'})

class LoginAPI(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response = super(LoginAPI, self).post(request, *args, **kwargs)
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request}
                                           )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id': user.id,
            'nome': user.firt_name,
            'email': user.email,
            'token': token.key
        })


class Logout(View):
    """
    Class Based View para fazer logout do usuário.
    """
    def get(self, request):
        logout(request)
        return redirect('/')
    
