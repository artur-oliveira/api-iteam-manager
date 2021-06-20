from django.urls import path
from .views import (ListCreateProjectView, RequestParticipationView, ListAdminProjectsView, ListMyProjectsView,
                    AcceptParticipationView)

urlpatterns = [
    path('', ListCreateProjectView.as_view(), name='list-create-project'),
    path('my/', ListMyProjectsView.as_view(), name='my-projects'),
    path('admin/', ListAdminProjectsView.as_view(), name='my-projects'),

    path('request/', RequestParticipationView.as_view(), name='request-participation'),
    path('accept/', AcceptParticipationView.as_view(), name='accept-participation'),
]
