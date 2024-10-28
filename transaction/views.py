from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render,get_object_or_404,redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from account.models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from sslcommerz_lib import SSLCOMMERZ 
from post.models import Post,Donation
from account.models import CustomUser
from django.contrib.auth.models import User
# Create your views here.
from decimal import Decimal
import uuid
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt


class InitiatePaymentView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        amount = request.data.get('amount')
        transaction_id = str(uuid.uuid4())
        post = get_object_or_404(Post, id=post_id)
        cus_user = CustomUser.objects.get(user=request.user)

        settings = {'store_id': 'exipe6719a3b69d208', 'store_pass': 'exipe6719a3b69d208@ssl', 'issandbox': True }

        sslcz = SSLCOMMERZ(settings)
        post_body = {
            'total_amount': amount,
            'currency': "BDT",
            'tran_id': transaction_id,
            'success_url': f'https://soft-heal.vercel.app/transaction/payment/success/{request.user.id}/{post_id}/{amount}/{transaction_id}',
            'fail_url': 'https://soft-heal.vercel.app/transaction/payment/fail/',
            'cancel_url': 'https://soft-heal.vercel.app/transaction/payment/cancel/',
            'emi_option': 0,
            'cus_name': request.user.username,
            'cus_email': request.user.email,
            'cus_phone': cus_user.phone,
            'cus_add1': cus_user.address,
            'cus_city': "Dhaka",
            'cus_country': "Bangladesh",
            'shipping_method': "NO",
            'multi_card_name': "",
            'num_of_item': 1,
            'product_name': post.name,
            'product_category': post.post_type,
            'product_profile': "general"
        }

        response = sslcz.createSession(post_body)
        if response and 'GatewayPageURL' in response:
            return JsonResponse({'gateway_url': response['GatewayPageURL']})
        else:
            return JsonResponse({'error': 'Failed to initiate payment'}, status=400)
    

@csrf_exempt
def payment_success(request,user_id,post_id,amount,tran_id):

    if not amount or not post_id or not tran_id or not user_id:
        return HttpResponse("Invalid payment details", status=400)
    
    try:
        post = get_object_or_404(Post,id=post_id)
        post.collected += int(amount)
        post.save()

        print(post.collected)
        print(amount)

        user = get_object_or_404(User,id=user_id)

        donation = Donation.objects.create(
            user = user,
            post = post,
            amount = amount,
            transaction_id = tran_id
        )
        donation.save()

    except Exception as e:
        return HttpResponse(f"Error updating post: {str(e)}", status=500)
    
    return render(request, "payment_success.html", {"amount": amount, "post": post , "tran_id": tran_id, "user":user})


@csrf_exempt
def payment_fail(request):
    return render(request, "payment_fail.html",{"message": "Payment failed !!"},status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def payment_cancel(request):
    return render(request, "payment_cancel.html",{"message": "Payment canceled !!"},status=status.HTTP_200_OK)