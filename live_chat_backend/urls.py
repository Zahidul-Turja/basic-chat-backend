from django.contrib import admin
from django.urls import path, include

from chat.urls import url_patterns
from usermanager.urls import user_urls, auth_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/", include(url_patterns)),
    path("auth/", include(auth_urls)),
    path("user/", include(user_urls)),
]
