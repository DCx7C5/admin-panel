from adrf.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import Host

AHSUser = get_user_model()


class HostSerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    address = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Host
        fields = '__all__'


class AHSUserSerializer(ModelSerializer):
    class Meta:
        model = AHSUser
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email', 'is_active', 'is_staff', 'is_superuser',
            'last_login', 'image', 'uid',
        ]
