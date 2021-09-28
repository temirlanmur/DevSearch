from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Message, Profile, Skill, User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [                        
            'username',
            'email',
            'password1',
            'password2']
        # labels = {'first_name': 'Name'}
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = (
            'id',
            'user'
        )
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': '6'
            })
        }
        labels = {
            'social_github': 'GitHub',
            'social_twitter': 'Twitter',
            'social_linkedin': 'LinkedIn',
            'social_youtube': 'YouTube',
            'social_website': 'Personal website'
        }
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        exclude = ('owner',)
        labels = {
            'name': 'Skill Name',            
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add skill name, e.g. "Django"'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Add description related to technology, your experience with it, etc., or leave blank'
            })
        }


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = [
            'name',
            'email',
            'subject',
            'body'
        ]
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': '5'
            })
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})