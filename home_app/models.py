from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# Create your models here.

class Url(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="urls")
    session_id = models.CharField(max_length=100, null=True, blank=True)
    long_url = models.CharField(max_length=1024)
    short_url = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    expiration_time = models.DateTimeField(null=True, blank=True)
    max_usage = models.PositiveSmallIntegerField(null=True, blank=True, help_text="null means it is unlimited")
    used_times = models.PositiveSmallIntegerField(default=0)
    requires_approval = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Long: {self.long_url:30} - Short: {self.short_url}"
    
    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super(Url, self).save(*args, **kwargs)

class ApprovalRequest(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="approval_requests")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="approved_requests", null=True, blank=True)
    url = models.ForeignKey(Url, on_delete=models.CASCADE, related_name="approval_requests")
    choices = [("approved", "Approved"), ("pending", "Pending"), ("rejected", "Rejected"), ]
    approved = models.CharField(max_length=10, choices=choices)
    # approved = models.BooleanField(null=True, blank=True, help_text="False means rejected!")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Approved: {self.approved}"
