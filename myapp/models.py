from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    USER = models.OneToOneField(User,on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    email = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    place = models.CharField(max_length=100)

    bio = models.TextField(
        null=True,
        blank=True
    )

    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True
    )
class Blog(models.Model):

    USER = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    image = models.FileField(upload_to='blog_images/')

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):

    USER = models.ForeignKey(User,on_delete=models.CASCADE)

    BLOG = models.ForeignKey(Blog,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):

    USER = models.ForeignKey(User,on_delete=models.CASCADE)

    BLOG = models.ForeignKey(Blog,on_delete=models.CASCADE)

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
class Save(models.Model):

    USER = models.ForeignKey(User,on_delete=models.CASCADE)

    BLOG = models.ForeignKey(Blog,on_delete=models.CASCADE)