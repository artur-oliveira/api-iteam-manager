from rest_framework.generics import ListCreateAPIView, CreateAPIView
from .models import Projeto
from .serializers import ProjetoSerializer, RequestParticipationSerializer, AcceptParticipationSerializer


class ListCreateProjectView(ListCreateAPIView):
    """
    Endpoint responsável pela listagem/criação de projetos
    """
    serializer_class = ProjetoSerializer

    def get_queryset(self):
        return Projeto.projetos_para_explorar(self.request.user)


class ListAdminProjectsView(ListCreateAPIView):
    """
    Endpoint responsável pela listagem de projetos que o usuário é criador ou administrador
    """
    serializer_class = ProjetoSerializer

    def get_queryset(self):
        return Projeto.projetos_com_acesso(self.request.user)


class ListMyProjectsView(ListCreateAPIView):
    """
    Endpoint responsável pela listagem de projetos que o usuário participa
    """
    serializer_class = ProjetoSerializer

    def get_queryset(self):
        return Projeto.projetos_que_participa(self.request.user)


class RequestParticipationView(CreateAPIView):
    """
    Endpoint responsável pela solicitação da participação em um projeto. A solicitação é feita pelo usuário autenticado
    """
    serializer_class = RequestParticipationSerializer

    def get_queryset(self):
        return []


class AcceptParticipationView(CreateAPIView):
    """
    Endpoint responsável pela aceitação da solicitação feita por um outro usuário, o usuário que aceitar deve possuir os
    privilégios necessários
    """
    serializer_class = AcceptParticipationSerializer

    def get_queryset(self):
        return []


class InviteView(CreateAPIView):
    """
    Endpoint responsável pela aceitação da solicitação feita por um outro usuário, o usuário que aceitar deve possuir os
    privilégios necessários
    """