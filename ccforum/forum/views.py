from django.shortcuts import render
from django.views.generic import ListView, DetailView
from forum.models import Category, Thread, Post

class CategoryView(ListView):
    model = Category

class ThreadView(ListView):
    def get_queryset(self):
        return Thread.objects.filter(is_reported=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()

class PostView(DetailView):
    def get_queryset(self):
        return Post.objects.filter(is_reported=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thread'] = Thread.objects.all(Post.thread)