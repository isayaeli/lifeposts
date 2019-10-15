from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import math
from django.utils import timezone
from django.urls import reverse, reverse_lazy

class Post(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE, max_length= 100)
    post_image = models.ImageField(blank=True, null=True, upload_to='images')
    post_video = models.FileField(blank=True, null=True, upload_to='videos')
    post_description = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    updated = models.DateTimeField(auto_now=True)

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('home')

    def __str__(self):
        return f"POST BY  {self.user}....>{self.post_description}:Time....{self.updated}"
    class Meta:
        ordering = ['-updated']

    def published(self):
        now = timezone.now()

        diff = now - self.updated
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            if seconds == 1:
                return str(seconds) + " second ago"
            else:
                return str(seconds) + " seconds ago"
        
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"
    
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        if diff.days >= 1 and diff.days < 30:
            days = diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"
        
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff/365)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    contents = models.TextField(max_length=100)
    commented_on = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f" COMMENT BY :..<{self.user}>:..<{self.post}>"
    
    def get_absolute_url(self):
        return reverse_lazy('post', kwargs={'id': self.post_id})

    # def get_success_url(self):
    #     return reverse_lazy('post', kwargs={'id':self.post_id})

    def total_comments(self):
        return self.contents.count()



    def commented(self):
        now = timezone.now()

        diff = now - self.commented_on
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            if seconds == 1:
                return str(seconds) + " second ago"
            else:
                return str(seconds) + " seconds ago"
        
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"
    
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        if diff.days >= 1 and diff.days < 30:
            days = diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"
        
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)
            if days == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff/365)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"


    
