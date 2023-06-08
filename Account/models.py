from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User_OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.IntegerField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
