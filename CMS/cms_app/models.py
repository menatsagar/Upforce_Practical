import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from dataclasses import dataclass, field
from django.utils import timezone
from typing import Union




class ActivityTracking(models.Model):
    created_at = models.DateTimeField(editable=False, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_active   = models.BooleanField(default=True)
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(ActivityTracking, self).save(*args, **kwargs)



class User(ActivityTracking):
    """
    A User replaces django's default user id with a UUID that should be created by the application, not the database.
    """
    
    
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True, blank=False, null=False)
    password  = models.CharField(max_length=128)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"

class Post(ActivityTracking):
    """This model stores the data into Post table in db"""

    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_all_posts")
    description  = models.TextField()
    content  = models.TextField(null=True, blank=True)
    is_public = models.BooleanField(default=True)


    def __str__(self):
        return self.title

    def soft_delete(self):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        db_table = "post"




class Like(ActivityTracking):
    """This model stores the data into comment table in db"""

   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_all_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes_on_post')

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        db_table = "like"
