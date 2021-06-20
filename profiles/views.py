from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from .serializers import ProfileSerializer, SimpleProfileSerializer
from .models import Profile


class AddInformationView(CreateAPIView):
    """
    Endpoint que Lista/Adiciona as informações básicas no perfil do usuário
    Devem ser passados os seguintes atributos:

    descricao (String): Descrição do usuário, uma apresentação
    interesses (Array[Categoria]): Lista de categorias que o usuário se interessa
    mostrar_perfil (Boolean): true, se o usuário quer que seu perfil apareça na pesquisa, false, caso contrário
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class MyInformationView(RetrieveUpdateAPIView):
    """
    Endpoint que mostra/atualiza as informações do usuário
    Para atualizar, devem ser passados os seguintes atributos:

    descricao (String): Descrição do usuário, uma apresentação
    interesses (Array[Categoria]): Lista de categorias que o usuário se interessa
    mostrar_perfil (Boolean): true, se o usuário quer que seu perfil apareça na pesquisa, false, caso contrário
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = None

    def get_object(self):
        return self.request.user.profile


class ListProfileView(ListAPIView):
    serializer_class = SimpleProfileSerializer
    queryset = Profile.get_browsable()
