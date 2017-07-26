from django.shortcuts import render
from django.views.generic import ListView, DetailView
from forum.models import Category, Thread, Post

class CategoryView(ListView):
    model = Category

class ThreadView(Li stView):
    def get_queryset(self):
        return Post.objects.filter(is_reported=False)

class PostView(DetailView):
    def get_queryset(self):
        return Post.objects.filter(is_reported=False)