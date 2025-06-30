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
    
    # Follow system fields
    following = models.ManyToManyField(
        'self',
        through='Follow',
        related_name='followers',
        symmetrical=False
    )

    def __str__(self):
        return self.email

    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()


class Follow(models.Model):
    follower = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following_relationships'
    )
    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower_relationships'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.email} follows {self.following.email}"


class OTP(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.user.email}"
