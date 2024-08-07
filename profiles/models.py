from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    '''
    Profile model.
    '''
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50, blank=True, default="")
    feeling = models.CharField(max_length=50, blank=True, default="")
    would_like_to = models.CharField(max_length=50, blank=True, default="")
    image = models.ImageField(
        upload_to='images/',
        default='../IRL/1F47D_color_nztbks'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    '''
    Create a profile instance for a new user
    '''
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
