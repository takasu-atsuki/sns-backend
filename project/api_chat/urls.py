from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_chat import views

router = DefaultRouter()
router.register('group', views.GroupViewSet)
router.register('chat', views.ChatViewSet)
router.register('groupIn', views.GroupInViewSet)
router.register('dmail', views.DMailViewSet)

urlpatterns = [
    path('', include(router.urls))
]