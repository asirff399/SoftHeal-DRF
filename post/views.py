from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Post,PostType,Donation
from account.models import CustomUser
from .serializers import PostSerializer,PostTypeSerializer,DonationSerializer
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.utils import timezone
from django_filters import rest_framework as django_filters
from rest_framework import filters, pagination
from decimal import Decimal,InvalidOperation

class PostViewset(viewsets.ModelViewSet):   
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['post_type__name','name',]

class PostTypeViewset(viewsets.ModelViewSet):
    queryset = PostType.objects.all()
    serializer_class = PostTypeSerializer

class DonationViewset(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    filter_backends = [filters.SearchFilter]
    serializer_class = DonationSerializer
    search_fields = ['user__id','post__name']

class PostList(APIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

    def get(self,request,format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetails(APIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_object(self,pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self,request,pk,format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from decimal import Decimal

class DonationAPIView(APIView):
    def put(self, request, post_id, format=None):
        post = get_object_or_404(Post, id=post_id)
        custom_user = get_object_or_404(CustomUser, user=request.user)
        amount = request.data.get('amount')

        try:
            # Convert amount to a decimal instead of float
            amount = Decimal(amount)
        except (ValueError, InvalidOperation):
            return Response({"error": "Invalid donation amount."}, status=status.HTTP_400_BAD_REQUEST)

        if amount <= 0:
            return Response({"error": "Donation amount must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

        if custom_user.balance < amount:
            return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct the amount from the user's balance
        custom_user.balance -= amount
        custom_user.save()

        # Add the amount to the post's collected amount
        post.collected += amount
        post.save()

        # Record the donation
        donation = Donation.objects.create(
            user=request.user,
            post=post,
            amount=amount,
            balance_after_donation=custom_user.balance
        )

        # Serialize the donation object and return the response
        serializer = DonationSerializer(donation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
