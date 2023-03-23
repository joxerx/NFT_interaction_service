from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("name", "address", "blockHash", "blockNumber", "transactionHash", "removed")

    def create(self, validated_data):
        return Event.objects.create(**validated_data)
