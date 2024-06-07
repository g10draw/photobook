from django.db import models

from auth_manager.models import CustomUser

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(CustomUser, 
            on_delete=models.CASCADE, related_name='my_posts')
    title = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', 
                                 on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='followers', 
                                  on_delete=models.CASCADE)