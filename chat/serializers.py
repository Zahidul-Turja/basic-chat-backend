from rest_framework import serializers

from chat.models import *
from usermanager.serializers import UserDetailsSerializer


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = "__all__"


class ConversationMessageSerializer(serializers.ModelSerializer):
    sender = UserDetailsSerializer()

    class Meta:
        model = ConversationMessage
        fields = "__all__"
