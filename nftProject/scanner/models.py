from django.db import models
from django.db.models import UniqueConstraint


class Event(models.Model):
    """Event"""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    blockHash = models.CharField(max_length=255)
    blockNumber = models.BigIntegerField()
    transactionHash = models.CharField(max_length=255, null=False)
    removed = models.BooleanField(default=False)
    logIndex = models.IntegerField()

    def __str__(self):
        return self.transactionHash

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['transactionHash', 'logIndex'], name='unique_event')
        ]
        verbose_name = "Event"
        verbose_name_plural = "Events"

