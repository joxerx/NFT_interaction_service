from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from .models import Token


class TokenSerializer(serializers.Serializer):
    unique_hash = serializers.CharField(max_length=255)
    tx_hash = serializers.CharField(max_length=255)
    media_url = serializers.URLField(max_length=255)
    owner = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Token.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.tx_hash = validated_data.get('tx_hash', instance.tx_hash)
        instance.save()
        return instance
