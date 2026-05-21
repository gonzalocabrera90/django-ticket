from django.db import models

class MainDashboard(models.Model):
    title = models.CharField(max_length=100)
    welcome_message = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
