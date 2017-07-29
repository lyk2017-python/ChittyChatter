from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from forum.models import Category, Thread
from forum.forms import PostForm
from django.views import generic


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

class ThreadView(generic.CreateView):
    form_class = PostForm
    template_name = "forum/thread_detail.html"
    success_url = "."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["thread"] = Thread.objects.filter(slug=self.kwargs["slug"])
        return context

class PostView(CreateView):
    form_class = PostForm
    template_name = "forum/thread_detail.html"
    success_url = "."


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_category()
        return context