from django.contrib import admin

from .models import *


# Register your models here.
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "sorted_user_ids", "created_at")


class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ("conversation", "id", "sender", "message", "created_at")
    list_per_page = 15


admin.site.register(Conversation, ConversationAdmin)
admin.site.register(ConversationMessage, ConversationMessageAdmin)
