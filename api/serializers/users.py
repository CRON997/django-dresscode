from rest_framework import serializers
from apps.users.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
