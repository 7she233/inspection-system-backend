from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # 微信相关字段
    openid = models.CharField(max_length=64, unique=True, verbose_name='微信OpenID')
    unionid = models.CharField(max_length=64, blank=True, null=True, verbose_name='微信UnionID')
    nickname = models.CharField(max_length=64, blank=True, verbose_name='微信昵称')
    avatar_url = models.URLField(blank=True, verbose_name='头像URL')
    
    # 其他字段
    phone = models.CharField(max_length=11, blank=True, verbose_name='手机号')
    is_verified = models.BooleanField(default=False, verbose_name='是否验证')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name 