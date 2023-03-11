from django.contrib import admin
from .models import Video, Like, Save, Comment

admin.site.register(Video)
admin.site.register(Like)
admin.site.register(Save)
admin.site.register(Comment)