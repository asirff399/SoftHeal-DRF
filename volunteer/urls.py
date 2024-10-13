from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import VolunteerViewset

router = DefaultRouter()
router.register('',VolunteerViewset)

urlpatterns = [
    path('',include(router.urls)),
] 