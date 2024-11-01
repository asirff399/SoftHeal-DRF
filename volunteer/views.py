from rest_framework import viewsets
from .models import Volunteer
from .serializers import VolunteerSerializer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

class VolunteerViewset(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

    def perform_create(self, serializer):
        volunteer_inst = serializer.save()

        email_subject = "Confirmation Of Your Register Submission"
        email_body = render_to_string('volunteer_mail.html',{
            'name': volunteer_inst.name,
        })
        email = EmailMultiAlternatives(
            subject = email_subject,
            body='',
            to = [volunteer_inst.email]
        )
        email.attach_alternative(email_body,"text/html")
        email.send()

        return Response({'message': 'Your message has been sent! Check your email for confirmation.'},status=status.HTTP_201_CREATED)

    
