from django import forms
from forum.models import Post, Thread, Category
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['content_text'].widget.attrs['rows'] = 3

    class Meta:
        model = Post
        exclude = ["id",
                   "is_reported",
                   ]
        widgets = {"thread": forms.HiddenInput(),
                   "like": forms.HiddenInput(),
                   }


class ContactForm(forms.Form):
    email = forms.EmailField()
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()


class ThreadCreateForm(forms.Form):
    title = forms.CharField()
    content_text = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.HiddenInput())

    def save(self):
        with transaction.atomic():
            thread = Thread.objects.create(title=self.cleaned_data["title"], category=self.cleaned_data["category"])
            Post.objects.create(thread=thread, content_text=self.cleaned_data["content_text"])
        return thread
