from django.urls import path
from .views import AddInformationView, MyInformationView, ListProfileView

urlpatterns = [
    path('', ListProfileView.as_view(), name='list-profiles'),
    path('add-information/', AddInformationView.as_view(), name='add-profile-information'),
    path('me/', MyInformationView.as_view(), name='my-profile'),
]
