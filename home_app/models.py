from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Url(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="urls", null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    long_url = models.CharField(max_length=255)
    short_url = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    expiration_time = models.DateTimeField(null=True, blank=True)
    max_usage = models.PositiveSmallIntegerField(null=True, blank=True, help_text="null means it is unlimited")

    def __str__(self):
        return f"Long: {self.long_url:30} - Short: {self.short_url}"
