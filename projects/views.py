from rest_framework.generics import ListCreateAPIView, CreateAPIView
from .models import Projeto
from .serializers import (ProjetoSerializer, RequestParticipationSerializer, AcceptParticipationSerializer,
                          DenyParticipationSerializer, RequestInviteSerializer, AcceptInviteSerializer,
                          DeclineInviteSerializer)


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


class DenyParticipationView(CreateAPIView):
    """
        Endpoint responsável pela negação da solicitação feita por um outro usuário, o usuário que negar deve possuir os
        privilégios necessários
        """
    serializer_class = DenyParticipationSerializer

    def get_queryset(self):
        return []


class RequestInviteView(CreateAPIView):
    """
    Endpoint responsável pelo convite de novos usuários no projeto
    """
    serializer_class = RequestInviteSerializer

    def get_queryset(self):
        return []


class AcceptInviteView(CreateAPIView):
    """
    Endpoint responsável pela aceitação do convite
    """
    serializer_class = AcceptInviteSerializer

    def get_queryset(self):
        return []


class DeclineInviteView(CreateAPIView):
    """
    Endpoint responsável pela aceitação do convite
    """
    serializer_class = DeclineInviteSerializer

    def get_queryset(self):
        return []
