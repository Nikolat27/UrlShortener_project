from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Url)
admin.site.register(models.ApprovalRequest)