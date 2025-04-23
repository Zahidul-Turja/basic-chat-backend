from django.urls import path

from chat.views import Conversations, ConversationMessages


url_patterns = [
    path("conversations/", Conversations.as_view(), name="conversations"),
    path(
        "conversation/<int:id>/",
        ConversationMessages.as_view(),
        name="conversation_messages",
    ),
]
