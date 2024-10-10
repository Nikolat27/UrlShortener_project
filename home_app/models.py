from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Url(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="urls", null=True, blank=True)
    long_url = models.CharField(max_length=255)
    short_url = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Long: {self.long_url:30} - Short: {self.short_url}"
