from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'city', 'phone']
        verbose_name_plural = 'Объекты'
        ordering = ['name']