from django.urls import path

from usermanager.views import *

auth_urls = [
    path("signup/", SignUp.as_view(), name="signup"),
    path("login/", Login.as_view(), name="login"),
]

user_urls = [
    path("", AllUsers.as_view(), name="users"),
    path("profile/", UserDetails.as_view(), name="user"),
]
