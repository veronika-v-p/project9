from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Saller, Material

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class SallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saller
        fields = ['first_name', 'last_name']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['name_n', 'price', 'saller']