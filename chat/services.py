from datetime import datetime

from chat.models import *
from usermanager.models import UserModel


def get_or_create_conversation(ids):
    sorted_ids = sorted(ids)
    sorted_user_ids = f"{sorted_ids[0]}_{sorted_ids[1]}"

    conversation = Conversation.objects.filter(sorted_user_ids=sorted_user_ids).first()
    if not conversation:
        sender = UserModel.objects.filter(id=ids[0]).first()
        reciever = UserModel.objects.filter(id=ids[1]).first()
        conversation = Conversation.objects.create(sorted_user_ids=sorted_user_ids)
        conversation.participants.add(sender)
        conversation.participants.add(reciever)
    conversation.save()

    return conversation


def create_message(message, sender_id, reciever_id):
    conversation = get_or_create_conversation(ids=[sender_id, reciever_id])
    sender = UserModel.objects.filter(id=sender_id).first()

    message = ConversationMessage.objects.create(
        message=message,
        sender=sender,
        conversation=conversation,
    )

    return message
