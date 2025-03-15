from django.contrib import admin
from .models import ChatMessage

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user_message", "bot_response", "timestamp")
    search_fields = ("user_message", "bot_response")

admin.site.register(ChatMessage, ChatMessageAdmin)
