from django import forms
from django.forms import HiddenInput
from forum.models import Post, Thread

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["id",
                   "like",
                   "is_reported",
                   ]
        widgets = {"thread": forms.HiddenInput()}

