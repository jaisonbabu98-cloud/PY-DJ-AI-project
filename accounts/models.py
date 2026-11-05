from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)

    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = None
        super().save(*args, **kwargs)


class EmailOTP(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="email_otp",)
    code_hash = models.CharField(max_length=128)
    sent_at = models.DateTimeField(auto_now=True)
    attempts = models.PositiveSmallIntegerField(default=0)

    def is_expired(self):
        return timezone.now() > self.sent_at + timedelta(minutes=1)