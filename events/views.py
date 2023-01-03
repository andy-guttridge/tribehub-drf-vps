from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from django.http import Http404
from django_filters import rest_framework as filters
from tribehub_drf.permissions import (
    IsTribeAdmin,
    IsThisTribeAdmin,
    IsThisTribeAdminOrOwner,
    IsInTribeReadOnly,
    IsInTribe
)
from tribes.models import Tribe
from profiles.models import Profile
from .models import Event
from .serializers import EventSerializer
from .filters import EventFilter


class EventList(generics.ListCreateAPIView):
    """
    List all events for the authenticated user's tribe and create new event
    for the tribe.
    """
    serializer_class = EventSerializer
    permission_classes = [IsInTribe]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EventFilter
    filterset_fields = ['start']

    def get_queryset(self):
        user = self.request.user
        queryset = Event.objects.filter(tribe=user.profile.tribe.pk)
        return queryset
