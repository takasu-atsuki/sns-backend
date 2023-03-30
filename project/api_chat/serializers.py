from rest_framework import serializers
from core.models import Group, Chat, DMail, GroupIn


class GroupSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    updatedAt = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'title', 'openGrouper', 'inUser', 'createdAt', 'updatedAt')
        extra_kwargs = {'openGrouper': {'read_only': True}}
        
    def validate(self, data):
        request = self.context['request']
        if('inUser' in data):
            for user in data['inUser']:
                if(request.user == user):
                    raise serializers.ValidationError('グループ作成者はグループ作成者自身を招待できません。')
                if(data['inUser'].count(user) >= 2):
                    raise serializers.ValidationError('同じユーザーを招待することはできません。')
        return data


class ChatSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    updatedAt = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = Chat
        fields = ('id', 'sender', 'group', 'message', 'createdAt', 'updatedAt')
        extra_kwargs = {'sender': {'read_only': True}}


class GroupInSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupIn
        fields = ('id', 'showUser', 'targetGroup', 'approved')


class DMailSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    updatedAt = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = DMail
        fields = ('id', 'sendUser', 'getUser', 'message', 'createdAt', 'updatedAt')
        extra_kwargs = {'sendUser': {'read_only': True}}

    def validate(self, value):
        request = self.context['request']
        if('getUser' in value and request.user == value['getUser']):
            raise serializers.ValidationError('送信者と受信者が同じにすることはできません。')
        return value