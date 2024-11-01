from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import PostViewset,PostTypeViewset,DonationViewset,PostList,PostDetails


router = DefaultRouter()
router.register('list',PostViewset)
router.register('types',PostTypeViewset)
router.register('donation',DonationViewset)
 
 
urlpatterns = [
    path('', include(router.urls)),
    path('add/', PostList.as_view(),name='post_list'),
    path('details/<int:pk>/', PostDetails.as_view(),name='post_details'),
]


