import uuid
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    username = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=500, blank=True)
    name = models.CharField(max_length=200, blank=True)
    short_intro = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    profile_image = models.ImageField(null=True,
        blank=True,
        upload_to='profiles/',
        default='profiles/user-default.png')
    social_github = models.URLField(max_length=400, blank=True)
    social_twitter = models.URLField(max_length=400, blank=True)
    social_linkedin = models.URLField(max_length=400, blank=True)
    social_youtube = models.URLField(max_length=400, blank=True)
    social_website = models.URLField(max_length=400, blank=True)    
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:profile_detail', kwargs={'id': self.id})
    
    def get_update_url(self):
        return reverse('users:update_profile', kwargs={'id': self.id})
    
    def get_delete_url(self):
        return reverse('users:delete_profile', kwargs={'id': self.id})
    
    @property
    def image_URL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url


class Skill(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False)
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='skills')
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_update_url(self):
        return reverse('users:update_skill', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('users:delete_skill', kwargs={'id': self.id})


class Message(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False)
    sender = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_messages')
    recipient = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incoming_messages')
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-date_created']

    def get_absolute_url(self):
        return reverse('users:message', kwargs={'id': self.id})