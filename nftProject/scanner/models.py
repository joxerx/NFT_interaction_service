from django.db import models


class Event(models.Model):
    """Event"""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    blockHash = models.CharField(max_length=255)
    blockNumber = models.CharField(max_length=255)
    transactionHash = models.CharField(max_length=255, unique=True)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.transactionHash

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
