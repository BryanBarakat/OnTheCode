from email.policy import default
from statistics import mode
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    sur_name = models.CharField(max_length=200, default='')
    website = models.URLField(max_length=300, default='')
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="profile_images", default= 'user.png')
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'post_images',default='back-color.jpg')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    no_of_inaccurate = models.IntegerField(default=0)
    no_of_dislikes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user
    
    
class LikePost(models.Model):
        post_id = models.CharField(max_length=500)
        username = models.CharField(max_length=200)
        
        def __str__(self):
            return self.username
        
        
class FollowersCount(models.Model):
    user = models.CharField(max_length=200)
    follower = models.CharField(max_length=200)
    
    def __str__(self):
        return self.user