from rest_framework import serializers
from core.models import Diary


class DiarySerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = Diary
        fields = ('id', 'user_id', 'image', 'message', 'created_at', 'updated_at', 'liked')
        extra_kwargs = {'user_id': {'read_only': True}}





