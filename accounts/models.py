from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.CharField(max_length=100)
    avatar=models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    follower= models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following= models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow')
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('follower', 'following')

    def __str__(self):
        return self.follower.username