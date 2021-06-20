from rest_framework.generics import ListCreateAPIView
from .serializers import CategoriaSerializer
from .models import Categoria


class CategorieListCreateView(ListCreateAPIView):
    """
    Endpoint de listagem e criação de categorias
    Para criação, devem ser passados os seguintes atributos:

    nome (String): Nome da categoria
    """

    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all()
