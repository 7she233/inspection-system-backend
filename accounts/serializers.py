from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone', 'is_verified', 'created_at')
        read_only_fields = ('created_at', 'is_verified') 