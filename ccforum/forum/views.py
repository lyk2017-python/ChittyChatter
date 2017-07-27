from django.shortcuts import render
from django.views.generic import ListView, DetailView
from forum.models import Category, Thread, Post

class CategoryView(ListView):
    model = Category

class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["thread"] = Thread.objects.all()
        return context
class ThreadView(DetailView):
    model = Thread

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        return context