from django.db import models


class Token(models.Model):
    """Token"""
    unique_hash = models.CharField(max_length=255)
    tx_hash = models.CharField(max_length=255)
    media_url = models.URLField(max_length=255)
    owner = models.CharField(max_length=255)

    def __str__(self):
        return self.unique_hash

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"
