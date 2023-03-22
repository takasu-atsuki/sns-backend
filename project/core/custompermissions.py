from rest_framework import permissions


class ProfilePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.userPro.id == request.user.id


class LikePermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.liker.id == request.user.id


class ChatPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method is permissions.SAFE_METHODS:
            return True
        return obj.sender.id == request.user.id


class DMailPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method is permissions.SAFE_METHODS:
            return True
        return obj.send_user.id == request.user.id


