from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile


class UserAdmin(UserAdmin):
    list_display = ('username','email','first_name','last_name','is_active','date_joined')

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Profile)