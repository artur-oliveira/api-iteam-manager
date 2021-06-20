from django.urls import path
from .views import (ListCreateProjectView, RequestParticipationView, ListAdminProjectsView, ListMyProjectsView,
                    AcceptParticipationView, DenyParticipationView, RequestInviteView, AcceptInviteView,
                    DeclineInviteView)


urlpatterns = [
    path('', ListCreateProjectView.as_view(), name='list-create-project'),
    path('my/', ListMyProjectsView.as_view(), name='my-projects'),
    path('admin/', ListAdminProjectsView.as_view(), name='my-projects'),

    path('request-participation/', RequestParticipationView.as_view(), name='request-participation'),
    path('accept-participation/', AcceptParticipationView.as_view(), name='accept-participation'),
    path('deny-participation/', DenyParticipationView.as_view(), name='deny-participation'),

    path('request-invite/', RequestInviteView.as_view(), name='request-invite'),
    path('accept-invite/', AcceptInviteView.as_view(), name='accept-invite'),
    path('decline-invite/', DeclineInviteView.as_view(), name='decline-invite'),
]
