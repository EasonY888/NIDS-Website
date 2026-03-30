from django.contrib import admin
from .models import ChatMessage, UploadedFiles, ChatSession, User

# Register your models here.
admin.site.register(ChatMessage)
admin.site.register(UploadedFiles)
admin.site.register(ChatSession)
admin.site.register(User)