from django.contrib.auth.models import User
from django.db import models

class LoginAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    failed_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Failed attempts: {self.failed_attempts} - Locked: {self.is_locked}"
