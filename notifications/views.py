from rest_framework.generics import ListAPIView
from .serializers import NotificationSerializer
from projects.models import (UsuarioRecusado, UsuarioAceito, UsuarioConviteRecusado, UsuarioConvidado)


class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return_list = []
        [return_list.append(item) for item in UsuarioRecusado.objects.filter(user=self.request.user, visualizou=False)]
        [return_list.append(item) for item in UsuarioAceito.objects.filter(user=self.request.user, visualizou=False)]
        [return_list.append(item) for item in UsuarioConviteRecusado.objects.filter(user=self.request.user, visualizou=False)]
        [return_list.append(item) for item in UsuarioConvidado.objects.filter(user=self.request.user, visualizou=False)]
