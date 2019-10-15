from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default= 'default.png', upload_to='profile_pics')
    work = models.CharField(max_length=100, blank=True, null=True)
    last_login = models.DateTimeField(auto_now=True)
    date_join = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.user} Profile"


def create_profile(sender, **kwargs):
    if kwargs['created']:
       user_profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class Terms_and_Privacy_Policy(models.Model):
    terms = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    