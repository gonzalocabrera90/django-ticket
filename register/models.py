from django.db import models

class RegistrationProfile(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    registered_at = models.DateTimeField(auto_now_add=True)
    newsletter_opt_in = models.BooleanField(default=False)

    def __str__(self):
        return self.username
