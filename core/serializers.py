from adrf.serializers import ModelSerializer
from rest_framework import serializers
from core.models import Host


class HostSerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    address = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Host
        fields = '__all__'
