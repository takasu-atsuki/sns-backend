from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profile, FriendRequest, Group, Chat, Diary, GroupIn, DMail
from django.test import TestCase
from datetime import datetime
from rest_framework.test import APIClient
from api_chat import serializers as cserializers
import os
from django.db.models import Q
time = datetime.now()

PASSWORD='pbkdf2_sha256$260000$O2CJugvRp7L8GMfcLfv8eZ$X8Mf8PPmtf37Emg2nD42bJ/m3PQF+jYVpgKEifiDbHo='

# ユーザーのテスト(tokenのテストも含む)
class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create(
            username='test',
            password=PASSWORD,
        )

    def test_postUser(self):
        self.client = APIClient()
        payload = {
            'username': 'test2',
            'password': PASSWORD
        }
        res = self.client.post('/api/user/create/', payload)
        
        user = User.objects.get(id=res.data['id'])
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(payload['username'], user.username)

    def test_token(self):
        token_data = self.client.post('/authen/', data={'username': 'test', 'password': 'password'})
        
        self.assertEqual(token_data.status_code, 200)
        self.assertTrue("token" in token_data.json().keys())

# プロフィールのテスト(viewも含む)
class ProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test1', password=PASSWORD)
        user2 = User.objects.create(username='test2', password=PASSWORD)
        user3 = User.objects.create(username='test3', password=PASSWORD)
        Profile.objects.create(userPro=user, nickName='test1', createdAt=time, updatedAt=time, image='test')
        Profile.objects.create(userPro=user2, nickName='test2', createdAt=time, updatedAt=time, image='test')
        
    def test_get_myprof(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        profiles = Profile.objects.all()
        self.assertEqual(profiles.count(), 2)
        
        res = self.client.get('/api/user/myprof/')
        
        profile = Profile.objects.get(id=res.data[0]['id'])
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(profile.userPro, user)
        self.assertEqual(profile.nickName, 'test1')
        self.assertEqual(profile.image, 'test')

    def test_profile_get(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        profile = self.client.get('/api/user/profile/')
        self.assertEqual(profile.status_code, 200)
        self.assertEqual(len(profile.data), 2)

    def test_profile_post(self):
        self.client = APIClient()
        user = User.objects.get(username='test3')
        self.client.force_authenticate(user=user)
        
        payload = {
            'nickName': 'hoge',
            'createdAt': time,
            'updatedAt': time,
            'image': open((os.path.dirname(os.path.abspath(__file__))) + '/../media/media/image/noimage.png', 'rb'),
        }
        
        res = self.client.post('/api/user/profile/', payload)
        
        profile = Profile.objects.get(id=res.data['id'])
        
        self.assertEqual(profile.nickName, payload['nickName'])
        self.assertEqual(res.status_code, 201)

    def test_profile_patch(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        profile = Profile.objects.get(userPro=user)
        
        self.assertEqual('test1', profile.nickName)
        
        payload = {
            'nickName': 'update_name',
            'image': open((os.path.dirname(os.path.abspath(__file__))) + '/../media/media/image/noimage.png', 'rb'),
        }
        
        res = self.client.patch(f'/api/user/profile/{profile.id}/' , payload)
        
        profile = Profile.objects.get(id=res.data['id'])
        
        self.assertEqual(profile.nickName, payload['nickName'])
        self.assertEqual(res.status_code, 200)

    def test_profile_delete(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)

        self.assertEqual(2, Profile.objects.count())

        profile = Profile.objects.get(userPro=user)
        
        res = self.client.delete(f'/api/user/profile/{profile.id}/')
        
        self.assertEqual(res.status_code, 204)
        self.assertEqual(1, Profile.objects.count())

# フレンドリストのテスト(viewも含む)
class FriendRequestTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username='test1', password=PASSWORD)
        user2 = User.objects.create(username='test2', password=PASSWORD)
        user3 = User.objects.create(username='test3', password=PASSWORD)
        FriendRequest.objects.create(askTo=user1, askFrom=user2, approved=False)
        FriendRequest.objects.create(askTo=user2, askFrom=user3, approved=True)

    def test_get_friendReq(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        friendReq = self.client.get('/api/user/approval/')

        self.assertEqual(friendReq.status_code, 200)
        self.assertEqual(len(friendReq.data), 1)
        self.assertEqual(FriendRequest.objects.count(), 2)

    def test_post_friendReq(self):
        self.client = APIClient()
        user3 = User.objects.get(username='test3')
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        payload = {
            'askTo': user3.id,
            'approved': False
        }
        
        res = self.client.post('/api/user/approval/', payload)
        
        friendreq = FriendRequest.objects.get(id=res.data['id'])

        self.assertEqual(res.status_code, 201)
        self.assertEqual(friendreq.askTo, user3)
        self.assertEqual(friendreq.approved, payload['approved'])

        # 重複していないか確認
        friendreq = self.client.post('/api/user/approval/', payload)
        
        self.assertEqual(friendreq.status_code, 400)

    def test_patch_friendReq(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        user2 = User.objects.get(username='test2')
        self.client.force_authenticate(user=user)
        
        friendreq = FriendRequest.objects.get(askTo=user.id, askFrom=user2.id)
        
        self.assertEqual(friendreq.approved, False)
        
        payload = {
            'approved': True
        }
        
        res = self.client.patch(f'/api/user/approval/{friendreq.id}/', payload)
        
        friendreq = FriendRequest.objects.get(askTo=user.id, askFrom=user2.id)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(friendreq.approved, True)

# チャットグループのテスト(viewも含む)
class GroupTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username='test1', password=PASSWORD)
        user2 = User.objects.create(username='test2', password=PASSWORD)
        user3 = User.objects.create(username='test3', password=PASSWORD)
        group1 = Group.objects.create(title='test_group', openGrouper=user1,
                                      createdAt=time, updatedAt=time)
        group2 = Group.objects.create(title='test_group2', openGrouper=user2,
                                      createdAt=time, updatedAt=time)

        group1.inUser.add(user2)
        group1.save()
        group2.inUser.add(user3)
        group2.save()

    def test_get_group(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        res = self.client.get('/api/chat/group/')
        
        groups = Group.objects.all()
        serializer = cserializers.GroupSerializer(groups, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)

    def test_post_group(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        payload = {
            'title': 'test_group3',
        }
        
        res = self.client.post('/api/chat/group/', payload)
        
        group = Group.objects.get(id=res.data['id'])
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(group.title, payload['title'])
        self.assertEqual(group.openGrouper, user)

    def test_patch_group(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        user3 = User.objects.get(username='test3')
        
        group = Group.objects.get(title='test_group')
        
        self.assertEqual(group.inUser.count(), 1)
        
        group.inUser.add(user3)
        group.save()
        
        payload = {
            'title': 'update'
        }
        
        res = self.client.patch(f'/api/chat/group/{group.id}/', payload)
        group = Group.objects.get(id=group.id)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(group.title, payload['title'])
        self.assertEqual(group.inUser.count(), 2)

    def test_delete_group(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        groups = Group.objects.all()
        
        self.assertEqual(groups.count(), 2)

        target_group = Group.objects.get(title='test_group')
        res = self.client.delete(f'/api/chat/group/{target_group.id}/')
        groups = Group.objects.all()
        
        self.assertEqual(res.status_code, 204)
        self.assertEqual(groups.count(), 1)

# チャットメッセージのテスト(viewも含む)
class ChatTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test1', password=PASSWORD)
        user2 = User.objects.create(username='test2', password=PASSWORD)
        group = Group.objects.create(title='test_group', openGrouper=user, createdAt=time, updatedAt=time)
        group.inUser.add(user2)
        Chat.objects.create(sender=user, group=group, message='test', createdAt=time, updatedAt=time)

    def test_get_chat(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        res = self.client.get('/api/chat/chat/')
        
        chats = Chat.objects.all()
        serializer = cserializers.ChatSerializer(chats, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)

    def test_post_chat(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        group = Group.objects.get(id=1)
        self.client.force_authenticate(user=user)
        
        payload = {
            'group': group.id,
            'message': 'test2'
        }
        
        res = self.client.post('/api/chat/chat/', payload)
        
        chat = Chat.objects.get(id=res.data['id'])
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(chat.sender, user)
        self.assertEqual(chat.group, group)
        self.assertEqual(chat.message, payload['message'])

    def test_patch_chat(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        chat = Chat.objects.get(id=1)
        
        self.assertEqual(chat.message, 'test')
        
        payload = {
            'message': 'update'
        }
        
        res = self.client.patch(f'/api/chat/chat/{chat.id}/', payload)
        
        chat = Chat.objects.get(id=1)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(chat.message, payload['message'])
    
    def test_delete_chat(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        chats = Chat.objects.all()
        self.assertEqual(chats.count(), 1)
        
        chat = Chat.objects.get(id=1)
        
        res = self.client.delete(f'/api/chat/chat/{chat.id}/')
        
        chats = Chat.objects.all()
        
        self.assertEqual(res.status_code, 204)
        self.assertEqual(chats.count(), 0)
   
# 日記のテスト(viewも含む)     
class DiaryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username='test1', password=PASSWORD)
        user2 = User.objects.create(username='test2', password=PASSWORD)
        diary = Diary.objects.create(userId=user1, message='test2', createdAt=time, updatedAt=time)
        diary.liked.add(user2)
        diary.save()
        diary2 = Diary.objects.create(userId=user2, message='test3', createdAt=time, updatedAt=time)
        diary2.liked.add(user1)
        diary2.save()
        
    def test_get_mydiary(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        diaries = Diary.objects.all()
        
        self.assertEqual(diaries.count(), 2)
        
        res = self.client.get('/api/diary/mydiary/')
        
        diary = Diary.objects.get(id=res.data[0]['id'])
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(diary.userId, user)
        self.assertEqual(diary.message, 'test2')
        
    def test_get_diary(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        res = self.client.get('/api/diary/diary/')
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)
        
    def test_post_diary(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        payload = {
            'image': open((os.path.dirname(os.path.abspath(__file__))) + '/../media/media/image/noimage.png', 'rb'),
            'message': 'test3'
        }
        
        res = self.client.post('/api/diary/diary/', payload)
        
        diary = Diary.objects.get(id=res.data['id'])
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(diary.message, payload['message'])
        
    def test_patch_diary(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        diary = Diary.objects.get(id=1)
        
        self.assertEqual('test2', diary.message)
        
        payload = {
            'message': 'update'
        }
        
        res = self.client.patch(f'/api/diary/diary/{diary.id}/', payload)
        
        diary = Diary.objects.get(id=res.data['id'])
        
        self.assertEqual(diary.message, payload['message'])
        self.assertEqual(res.status_code, 200)
        
    def test_delete_diary(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        diaries = Diary.objects.all()
        
        self.assertEqual(diaries.count(), 2)
        
        diary = Diary.objects.get(id=1)
        
        self.client.delete(f'/api/diary/diary/{diary.id}/')
        
        diaries = Diary.objects.all()
        
        self.assertEqual(diaries.count(), 1)
        
# グループメンバーのテスト(viewも含む) 
class GroupInTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username='test1', password=PASSWORD)
        user2 = User.objects.create(username='test2', password=PASSWORD)
        user3 = User.objects.create(username='test3', password=PASSWORD)
        group1 = Group.objects.create(title='test_group', openGrouper=user1, createdAt=time, updatedAt=time)
        group1.inUser.add(user2)
        group1.save()
        group2 = Group.objects.create(title='test_group2', openGrouper=user2, createdAt=time, updatedAt=time)
        group2.inUser.add(user3)
        group2.save()
        GroupIn.objects.create(showUser=user2, targetGroup=group1, approved=False)
        GroupIn.objects.create(showUser=user1, targetGroup=group2, approved=True)
    
    def test_get_groupIn(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        res = self.client.get('/api/chat/groupIn/')
        
        groupIns = GroupIn.objects.all()
        serializer = cserializers.GroupInSerializer(groupIns, many=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)
        
    def test_post_groupIn(self):
        self.client = APIClient()
        user3 = User.objects.get(username='test3')
        self.client.force_authenticate(user=user3)
        
        group = Group.objects.get(title='test_group')
        groupIns = GroupIn.objects.all()
        
        self.assertEqual(groupIns.count(), 2)
        
        payload = {
            'showUser': user3.id,
            'targetGroup': group.id,
            'approved': False
        }
        
        res = self.client.post('/api/chat/groupIn/', payload)
        
        groupIn = GroupIn.objects.get(id=res.data['id'])
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(groupIn.showUser, user3)
        self.assertEqual(groupIn.targetGroup, group)
        self.assertEqual(groupIn.approved, False)
        
        # 重複してないか確認
        res = self.client.post('/api/chat/groupIn/', payload)
        self.assertEqual(res.status_code, 400)
        
    def test_patch_groupIn(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        group2 = Group.objects.get(title='test_group2')
        groupIn = GroupIn.objects.get(showUser=user, targetGroup=group2)
        
        self.assertEqual(groupIn.approved, True)
        
        payload = {
            'approved': False
        }
        
        res = self.client.patch(f'/api/chat/groupIn/{groupIn.id}/', payload)
        
        groupIn = GroupIn.objects.get(id=res.data['id'])
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(groupIn.approved, payload['approved'])

# ダイレクトメッセージのテスト(viewも含む)      
class DMailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test1', password=PASSWORD)
        user2 = User.objects.create(username='test2', password=PASSWORD)
        user3 = User.objects.create(username='test3', password=PASSWORD)
        DMail.objects.create(sendUser=user, getUser=user2, message='test', createdAt=time, updatedAt=time)
        DMail.objects.create(sendUser=user2, getUser=user3, message='test', createdAt=time, updatedAt=time)
        
    def test_get_dmail(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        dmails = DMail.objects.all()
        
        self.assertEqual(dmails.count(), 2)
        
        res = self.client.get('/api/chat/dmail/')
        
        dmails = DMail.objects.all().filter(Q(sendUser=user) | Q(getUser=user))
        
        self.assertEqual(dmails.count(), len(res.data))
        self.assertEqual(res.status_code, 200)
        
    def test_post_dmail(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        user2 = User.objects.get(username='test2')
        dmails = DMail.objects.all()
        
        self.assertEqual(dmails.count(), 2)
        
        payload = {
            'getUser': user2.id,
            'message': 'test2'
        }
        
        res = self.client.post('/api/chat/dmail/', payload)
        
        dmail = DMail.objects.get(id=res.data['id'])
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(dmail.sendUser, user)
        self.assertEqual(dmail.getUser, user2)
        self.assertEqual(dmail.message, payload['message'])
        
    def test_patch_dmail(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        user2 = User.objects.get(username='test2')
        dmail = DMail.objects.get(sendUser=user, getUser=user2)
        
        self.assertEqual(dmail.message, 'test')
        
        payload = {
            'message': 'update'
        }
        
        res = self.client.patch(f'/api/chat/dmail/{dmail.id}/', payload)
        
        dmail = DMail.objects.get(id=res.data['id'])
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(dmail.message, payload['message'])
        
    def test_delete_dmail(self):
        self.client = APIClient()
        user = User.objects.get(username='test1')
        self.client.force_authenticate(user=user)
        
        dmails = DMail.objects.all()
        
        self.assertEqual(dmails.count(), 2)
        
        dmail = DMail.objects.get(id=1)
        
        res = self.client.delete(f'/api/chat/dmail/{dmail.id}/')
        
        dmails = DMail.objects.all()
        
        self.assertEqual(res.status_code, 204)
        self.assertEqual(dmails.count(), 1)
        





























