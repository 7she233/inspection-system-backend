from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """自定义用户模型"""
    # 修改关联字段名
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set'
    )
    
    # 微信相关字段
    openid = models.CharField(max_length=64, unique=True, verbose_name='openid')
    unionid = models.CharField(max_length=64, blank=True, null=True, verbose_name='unionid') 
    session_key = models.CharField(max_length=64, blank=True, verbose_name='session_key')
    
    # 用户信息
    nickname = models.CharField(max_length=64, blank=True, verbose_name='昵称')
    avatar_url = models.URLField(blank=True, verbose_name='头像')
    
    # 状态字段
    last_login_time = models.DateTimeField(auto_now=True, verbose_name='最后登录时间')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.nickname or self.username 