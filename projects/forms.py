from django import forms
from django.db.models.fields import TextField
from django.forms import ModelForm
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'featured_image',
            'demo_link',
            'source_link',
            'tags'           
        ]
        widgets = {
            'tags': forms.SelectMultiple,
            'description': forms.Textarea(attrs={
                'rows': '4'
            })
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = [
            'value',
            'body']    
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment'}
        widgets = {
            'value': forms.Select(attrs={                
                'class': 'form-select w-auto',                        
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',            
                'rows': '5',
                'placeholder': 'Leave blank if you would like to vote anonymously'
            }),
        }
    
    