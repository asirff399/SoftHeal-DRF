from django.shortcuts import render
from rest_framework import viewsets
from .models import Team
from .serializers import TeamSerializer
# Create your views here.

class TeamViewset(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer