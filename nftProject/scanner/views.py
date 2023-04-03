from rest_framework import generics

from .serializers import EventSerializer
from .models import Event


class EventListAPIView(generics.ListCreateAPIView):
    """Show events list, saved in database"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ['get']
