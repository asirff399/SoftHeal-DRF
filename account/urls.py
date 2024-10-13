from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewset,ReviewViewSet,UserRegistrationApiView,UserLoginApiView,UserLogoutApiView,activate,PasswordChangeView,ReviewCreateView,UserProfileUpdateApiView
from django.http import HttpResponseRedirect

router = DefaultRouter()
router.register('list',CustomUserViewset)
router.register('review',ReviewViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationApiView.as_view(),name='register'),
    path('login/', UserLoginApiView.as_view(),name='login'),
    path('logout/', UserLogoutApiView.as_view(),name='logout'),
    path('profile/update/', UserProfileUpdateApiView.as_view(),name='update_profile'),
    path('profile/pass_change/', PasswordChangeView.as_view(),name='pass_change'),
    path('create_review/', ReviewCreateView.as_view(),name='create_review'),
    path('active/<uid64>/<token>/', activate, name = 'activate'),
]