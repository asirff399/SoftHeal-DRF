from django.urls import path,include
from .views import DeposiMoneyAPIView

urlpatterns = [
    path('deposit/',DeposiMoneyAPIView.as_view(),name='deposit'),
] 