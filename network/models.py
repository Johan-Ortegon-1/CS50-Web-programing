from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers_counter = models.IntegerField(default=0)
    following_counter = models.IntegerField(default=0)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")
    
class Post(models.Model):
    content = models.TextField(default="")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    like_counter = models.IntegerField(default=0)
    date = models.DateTimeField()
    
class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doer")
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="receiver")
