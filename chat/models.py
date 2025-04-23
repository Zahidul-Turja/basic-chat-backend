from django.db import models
from usermanager.models import UserModel


# Create your models here.
class Conversation(models.Model):
    sorted_user_ids = models.CharField(
        max_length=255, unique=True, null=True
    )  # "12_89"
    participants = models.ManyToManyField(UserModel, related_name="conversations")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sorted_user_ids

    class Meta:
        db_table = "conversation"
        verbose_name_plural = "Conversations"


class ConversationMessage(models.Model):
    sender = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        null=True,
        related_name="conversation_message_sender",
    )
    conversation = models.ForeignKey(
        Conversation, related_name="conversation_message", on_delete=models.CASCADE
    )
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender} - {self.message}"

    class Meta:
        db_table = "conversation_message"
        verbose_name_plural = "Conversation Messages"
