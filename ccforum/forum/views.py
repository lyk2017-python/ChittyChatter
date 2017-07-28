from django.shortcuts import render
from django.views.generic import ListView, DetailView
from forum.models import Category, Thread, Post
from django.db.models import Min

class CategoryView(ListView):
    model = Category

class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        latest_posts = []
        for i in context["object"].thread_set.all():
            latest_posts.append(i.post_set.latest("sent_date"))
        context['latest_posts'] = latest_posts
        return context

class ThreadView(DetailView):
    model = Thread

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        context["post"] = context["object"].post_set.all()
        return context