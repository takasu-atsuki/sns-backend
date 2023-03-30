from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import random


def upload_user_path(instance, filename):
    ext = filename.split('.')[-1]
    rd = random.randrange(10, 15)
    filename = get_random_string(rd)
    return 'media/' + '/'.join(['user', str(filename) + str('.') + str(ext)])


def upload_diary_path(instance, filename):
    ext = filename.split('.')[-1]
    rd = random.randrange(10, 15)
    filename = get_random_string(rd)
    return 'media/' + '/'.join(['diary', str(filename) + str('.') + str(ext)])


class Profile(models.Model):
    userPro = models.OneToOneField(User, related_name='userPro', on_delete=models.CASCADE)
    nickName = models.CharField(max_length=20)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, null=True, upload_to=upload_user_path)

    def __str__(self):
        return self.nickName


class FriendRequest(models.Model):
    askFrom = models.ForeignKey(User, related_name='askFrom', on_delete=models.CASCADE)
    askTo = models.ForeignKey(User, related_name='askTo', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    class Meta:
        unique_together = (('askFrom', 'askTo'),)

    def __str__(self):
        return str(self.askFrom) + '--------->' + str(self.askTo)


class Group(models.Model):
    title = models.CharField(max_length=20)
    openGrouper = models.ForeignKey(User, related_name='opener', on_delete=models.CASCADE)
    inUser = models.ManyToManyField(User, related_name='inUser', blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='sender', null=True, on_delete=models.SET_NULL)
    group = models.ForeignKey(Group, related_name='group', on_delete=models.CASCADE)
    message = models.CharField(max_length=30)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.sender) + '------------>' + str(self.group)


class Diary(models.Model):
    userId = models.ForeignKey(User, related_name='user_id', on_delete=models.CASCADE)
    # image = models.ImageField(blank=True, null=True, upload_to=upload_diary_path)
    image = models.ImageField(default='media/image/noimage.png', upload_to=upload_diary_path)
    message = models.CharField(max_length=30, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    liked = models.ManyToManyField(User, related_name='liked', blank=True)

    def __str__(self):
        return str(self.createdAt) + ' : ' + str(self.userId)


class GroupIn(models.Model):
    showUser = models.ForeignKey(User, related_name='show_user', on_delete=models.CASCADE)
    targetGroup = models.ForeignKey(Group, related_name='target_group', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    class Meta:
        unique_together = (('showUser', 'targetGroup'),)

    def __str__(self):
        return str(self.target_group) + '--------->' + str(self.show_user)


class DMail(models.Model):
    sendUser = models.ForeignKey(User, related_name='send_user', null=True, on_delete=models.SET_NULL)
    getUser = models.ForeignKey(User, related_name='get_user', null=True, on_delete=models.CASCADE)
    message = models.CharField(max_length=15)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.sendUser) + '--------->' + str(self.getUser)
