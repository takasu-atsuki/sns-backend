from rest_framework import authentication, permissions
from api_chat import serializers
from core.models import Group, Chat, GroupIn, DMail
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from core import custompermissions
from django.db.models import Q
from rest_framework.exceptions import ValidationError


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(openGrouper=self.request.user)


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = serializers.ChatSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, custompermissions.ChatPermissions)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class GroupInViewSet(viewsets.ModelViewSet):
    queryset = GroupIn.objects.all()
    serializer_class = serializers.GroupInSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self, serializer):
        try:
            serializer.save()
        except:
            raise ValidationError('The combination of group and invited users is unique')

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Delete is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class DMailViewSet(viewsets.ModelViewSet):
    queryset = DMail.objects.all()
    serializer_class = serializers.DMailSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, custompermissions.DMailPermissions)

    def get_queryset(self):
        return self.queryset.filter(Q(sendUser=self.request.user) | Q(getUser=self.request.user))

    def perform_create(self, serializer):
        serializer.save(sendUser=self.request.user)

