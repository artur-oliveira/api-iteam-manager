from django.urls import path
from .views import AddInformationView

urlpatterns = [
    path('add-information/', AddInformationView.as_view(), name='add-profile-information'),
]
