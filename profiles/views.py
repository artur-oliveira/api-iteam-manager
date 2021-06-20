from rest_framework.generics import CreateAPIView
from .serializers import ProfileSerializer
from .models import Profile


class AddInformationView(CreateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
