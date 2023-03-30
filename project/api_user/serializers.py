from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from core.models import Profile, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):

    createdAt = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    updatedAt = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'userPro', 'nickName', 'createdAt', 'updatedAt', 'image')
        extra_kwargs = {'userPro': {'read_only': True}}


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('id', 'askFrom', 'askTo', 'approved')
        extra_kwargs = {'askFrom': {'read_only': True}}
        
         
    def validate(self, data):
        request = self.context['request']
        if('askTo' in data and request.user == data['askTo']):
            raise serializers.ValidationError('友達申請者と友達受付者同じにすることはできません。')
        return data