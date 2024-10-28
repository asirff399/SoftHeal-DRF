from django.urls import path,include
from .views import InitiatePaymentView,payment_success,payment_fail,payment_cancel

urlpatterns = [
    path('payment/initiate/<int:post_id>', InitiatePaymentView.as_view(), name='initiate_payment'),
    path('payment/success/<int:user_id>/<int:post_id>/<int:amount>/<tran_id>', payment_success, name='payment_success'),
    path('payment/fail/', payment_fail, name='payment_fail'),
    path('payment/cancel/', payment_cancel, name='payment_cancel'),
] 