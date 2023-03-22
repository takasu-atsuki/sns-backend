from django.contrib import admin
from core import models

admin.site.register(models.Profile)
admin.site.register(models.FriendRequest)
admin.site.register(models.Group)
admin.site.register(models.Chat)
admin.site.register(models.Diary)
admin.site.register(models.GroupIn)
admin.site.register(models.DMail)