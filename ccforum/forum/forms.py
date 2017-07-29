from django import forms
from django.db.models import TextField
from django.forms import HiddenInput, Textarea, TextInput
from forum.models import Post, Thread

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['content_text'].widget.attrs['rows'] = 3

    class Meta:
        model = Post
        exclude = ["id",
                   "like",
                   "is_reported",
                   ]
        widgets = {"thread": forms.HiddenInput()}





