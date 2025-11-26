# Гость мероприятия и всё что будет связано с ним
from django.db import models


class Guest(models.Model):
    telegram_id = models.IntegerField(unique=True, verbose_name="ID в Telegram")
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''} ({self.telegram_id})"