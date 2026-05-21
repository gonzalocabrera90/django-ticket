from django.db import models

class LoginLog(models.Model):
    username = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.timestamp} (Success: {self.success})"
