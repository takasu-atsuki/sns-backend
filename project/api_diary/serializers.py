from rest_framework import serializers
from core.models import Diary


class DiarySerializer(serializers.ModelSerializer):

    createdAt = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    updatedAt = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = Diary
        fields = ('id', 'userId', 'image', 'message', 'createdAt', 'updatedAt', 'liked')
        extra_kwargs = {'userId': {'read_only': True}}





