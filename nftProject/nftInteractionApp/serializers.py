from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from .models import Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ("unique_hash", "tx_hash", "media_url", "owner")

    def create(self, validated_data):
        return Token.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.tx_hash = validated_data.get('tx_hash', instance.tx_hash)
        instance.save()
        return instance
