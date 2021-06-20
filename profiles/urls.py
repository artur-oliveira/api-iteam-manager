from django.urls import path
from .views import AddInformationView, MyInformationView

urlpatterns = [
    path('add-information/', AddInformationView.as_view(), name='add-profile-information'),
    path('me/', MyInformationView.as_view(), name='my-profile'),
]
