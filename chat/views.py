from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from chat.models import *
from chat.serializers import *


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page_number"
    page_size_query_param = "page_size"
    max_page_size = 100


class Conversations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        conversations = user.conversations.all()

        paginator = CustomPagination()
        conversations = paginator.paginate_queryset(conversations, request)
        serializer = ConversationSerializer(conversations, many=True)

        return paginator.get_paginated_response(serializer.data)


class ConversationMessages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        messages = ConversationMessage.objects.filter(conversation=id).order_by(
            "-created_at"
        )

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(messages, request)
        serializer = ConversationMessageSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
