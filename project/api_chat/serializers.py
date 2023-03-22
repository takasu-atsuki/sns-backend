from rest_framework import serializers
from core.models import Group, Chat, DMail, GroupIn


class GroupSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'title', 'openGrouper', 'inUser', 'created_at', 'updated_at')
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
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = Chat
        fields = ('id', 'sender', 'group', 'message', 'created_at', 'updated_at')
        extra_kwargs = {'sender': {'read_only': True}}


class GroupInSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupIn
        fields = ('id', 'show_user', 'target_group', 'approved')


class DMailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = DMail
        fields = ('id', 'send_user', 'get_user', 'message', 'created_at', 'updated_at')
        extra_kwargs = {'send_user': {'read_only': True}}

    def validate(self, value):
        request = self.context['request']
        if('get_user' in value and request.user == value['get_user']):
            raise serializers.ValidationError('送信者と受信者が同じにすることはできません。')
        return value