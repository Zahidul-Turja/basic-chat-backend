from django.contrib import admin
from .models import *


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "id", "phone", "name")


admin.site.register(UserModel, UserAdmin)
