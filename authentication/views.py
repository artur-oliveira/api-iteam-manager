from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    """
    Endpoint para criação de usuários
    Devem ser passados os seguintes atributos:

    username (String): Username
    email (Email/String): Email do usuário
    first_name (String): Nome
    last_name (String): Sobrenome
    password (String): Senha do usuário
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )
