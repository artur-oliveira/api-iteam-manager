from django.urls import path
from .views import CategorieListCreateView

urlpatterns = [
    path('', CategorieListCreateView.as_view(), name='category-list-create'),
]
