from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_user import views

router = DefaultRouter()
router.register('profile', views.ProfileViewSet)
router.register('approval', views.FriendRequestViewSet)

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('myprof/', views.MyProfileListView.as_view(), name='myprof'),
    path('', include(router.urls)),
]