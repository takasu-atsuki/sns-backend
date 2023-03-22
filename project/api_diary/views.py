from rest_framework import generics, authentication, permissions
from api_diary import serializers
from core.models import Diary
from rest_framework import viewsets
from core import custompermissions


class AllUserDiaryViewSet(viewsets.ModelViewSet):
    queryset = Diary.objects.all()
    serializer_class = serializers.DiarySerializer

    authentication_classes = (authentication.TokenAuthentication,)
    permissions = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class PersonDiaryViewSet(generics.ListAPIView):
    queryset = Diary.objects.all()
    serializer_class = serializers.DiarySerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user)

