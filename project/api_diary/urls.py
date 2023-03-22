from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_diary import views

router = DefaultRouter()
router.register('diary', views.AllUserDiaryViewSet)

urlpatterns = [
    path('mydiary/', views.PersonDiaryViewSet.as_view(), name='mydiary'),
    path('', include(router.urls))
]