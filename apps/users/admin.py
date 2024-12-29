from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'nickname', 'openid', 'is_staff', 'last_login_time')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'nickname', 'openid')
    ordering = ('-last_login_time',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('微信信息', {'fields': ('openid', 'unionid', 'session_key')}),
        ('用户资料', {'fields': ('nickname', 'avatar_url')}),
    ) 