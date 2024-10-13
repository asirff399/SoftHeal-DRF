from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Deposite
from account.models import CustomUser
from .serializers import DepositSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class DeposiMoneyAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def put(self,request,*args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = DepositSerializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            amount = serializer._validated_data['amount']
            CSuser = user.customuser
            CSuser.balance += amount
            CSuser.save(update_fields=['balance'])

            serializer.save(user=user,balance_after_transaction = CSuser.balance)

            try:
                email_subject = "Deposit Message"
                email_body = render_to_string('deposit_email.html',{'user':user,'amount':amount})
                email = EmailMultiAlternatives(email_subject,'',to=[user.email])
                email.attach_alternative(email_body,"text/html")
                email.send()
            except Exception as e:
                print(f"Failed to send email: {e}")

            return Response({"success":"Amount deposited successfully!"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

