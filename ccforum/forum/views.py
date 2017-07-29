from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from forum.models import Category, Thread, Post
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
    template_name = "forum/thread_form.html"
    success_url = "."

    def get_thread(self):
        thread = Thread.objects.get(slug=self.kwargs["slug"])
        return thread

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ['POST', 'PUT']:
            post_data = kwargs["data"].copy()
            post_data["thread"] = self.get_thread().id
            kwargs["data"] = post_data
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_thread()
        context["posts"] = context["object"].post_set.all()

        return context

