from django.contrib.auth import login

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination


from usermanager.models import *
from usermanager.serializers import *


class CustomPaginator(PageNumberPagination):
    page_size = 10
    page_query_param = "page_number"
    page_size_query_param = "page_size"
    max_page_size = 100


class SignUp(APIView):
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)

            refresh = RefreshToken.for_user(serializer.instance)
            response = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "user_id": serializer.instance.pk,
                    "email": serializer.instance.email,
                    "name": serializer.instance.name,
                },
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "Login successful",
                    "data": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user": {
                            "user_id": user.pk,
                            "email": user.email,
                            "name": user.name,
                        },
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=400)


class UserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data)


class AllUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = UserModel.objects.all()
        paginator = CustomPaginator()
        users = paginator.paginate_queryset(users, request)
        serializer = UserDetailsSerializer(users, many=True)

        return paginator.get_paginated_response(serializer.data)
