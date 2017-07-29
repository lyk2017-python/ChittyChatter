from django import forms
from django.forms import HiddenInput
from forum.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["id",
                   "like",
                   "is_reported",
                   "thread",
                   ]


