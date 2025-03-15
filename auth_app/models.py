from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    avatar = CloudinaryField("image", blank=True, null=True)
    profession = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    

    def __str__(self):
        return self.email


class OTP(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.user.email}"
