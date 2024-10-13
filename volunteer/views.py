from rest_framework import viewsets
from .models import Volunteer
from .serializers import VolunteerSerializer

# Create your views here.

class VolunteerViewset(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
