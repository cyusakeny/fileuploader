from django.db.models.signals import post_save, post_delete
from .models import Profile
from django.contrib.auth.models import User


def CreateProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        print('Email', instance.email)
        profile = Profile.objects.create(
            user=user,
            name=user.last_name,
            email=user.email,
            phone='0000',
            username=user.username
        )


def DeleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(CreateProfile, sender=User)
post_delete.connect(DeleteUser, sender=Profile)