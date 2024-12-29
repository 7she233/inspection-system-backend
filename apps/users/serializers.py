from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'avatar_url', 'last_login_time']
        read_only_fields = ['id', 'last_login_time'] 