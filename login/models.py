from django.db import models
from register.models import User

class LoginLog(models.Model):
    username = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.timestamp} (Success: {self.success})"

class LoginCode(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    code = models.CharField(
        max_length=6
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.email} - {self.code}"