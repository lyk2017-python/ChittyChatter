from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView
from forum.models import Category, Thread, Post
from forum.forms import *
from django.views import generic
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


class CategoryView(ListView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["threads"] = Thread.objects.order_by("-likes")
        return context

class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        # latest_posts = []
        # for i in context["object"].thread_set.all():
        #     latest_posts.append(i.post_set.latest("sent_date"))
        #  context['latest_posts'] = latest_posts
        return context


class ThreadCreateView(FormView):
    form_class = ThreadCreateForm
    success_url = "/"
    template_name = "forum/thread_create.html"

    @method_decorator(login_required)
    def post(self, request, *a, **kw):
        return super().post(request, *a, **kw)

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

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


class ContactFormView(generic.FormView):
    form_class = ContactForm
    template_name = "forum/contact.html"
    success_url = "/"


    def form_valid(self, form):
        data = form.cleaned_data
        send_mail(
            "CcForum ContactForm : {}".format(data["title"]),
            ("Bildiriminiz var!\n"
             "---\n"
             "{}\n"
             "---\n"
             "eposta={}\n"
             "ip={}").format(data["body"], data["email"], self.request.META["REMOTE_ADDR"]),
            settings.DEFAULT_FROM_EMAIL,
            ["noreply@ccforum.com"])
        return super().form_valid(form)


class RulesView(TemplateView):
    template_name = "forum/rules.html"