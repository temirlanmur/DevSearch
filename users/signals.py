from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Profile


# Receiver
# @receiver(post_save, sender=Profile)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.username)
        print('PROFILE CREATED')


def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        fullname = profile.name.split()
        user.first_name = fullname[0]
        if len(fullname) >= 2:
            user.last_name = profile.name.split()[1]
        user.username = profile.username
        user.email = profile.email
        user.save()


# @receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(create_profile, sender=User)
post_save.connect(update_user, sender=Profile)
post_delete.connect(delete_user, sender=Profile)