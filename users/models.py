from django.db import models
from django.contrib.auth.models import User

class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        from datetime import timedelta, timezone
        return self.created_at + timedelta(minutes=10) < timezone.now()
