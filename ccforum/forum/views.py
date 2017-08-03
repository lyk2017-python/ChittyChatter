from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView
from forum.forms import *
from django.views import generic
from django.conf import settings
from django.core.mail import send_mail
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm


class CategoryView(ListView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["threads"] = Thread.objects.order_by("-likes")
        return context


class CategoryDetailView(DetailView):
    model = Category
    slug_url_kwarg = "cslug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        # latest_posts = []
        # for i in context["object"].thread_set.all():
        #     latest_posts.append(i.post_set.latest("sent_date"))
        #  context['latest_posts'] = latest_posts
        return context


"""    @method_decorator(login_required)
    def post(self, request, *a, **kw):
        return super().post(request, *a, **kw)
"""


class ThreadCreateView(FormView):
    form_class = ThreadCreateForm
    success_url = "/"
    template_name = "forum/thread_create.html"


    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_category(self):
        query = Category.objects.filter(slug=self.kwargs["cslug"])
        if query.exists():
            return query.get()
        else:
            raise Http404("Category not found")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ["POST", "PUT"]:
            post_data = kwargs["data"].copy()
            post_data["category"] = self.get_category().id
            kwargs["data"] = post_data
        return kwargs


class ThreadView(generic.CreateView):
    form_class = PostForm
    template_name = "forum/thread_form.html"
    success_url = "."

    def get_thread(self):
        thread = Thread.objects.get(slug=self.kwargs["tslug"])
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


def like(request):
    id = request.POST.get("id", default=None)
    like = request.POST.get("like")
    obj = get_object_or_404(Post, id=int(id))
    if like == "true":
        obj.score = F("like") + 1
        obj.save(update_fields=["like"])
    elif like == "false":
        obj.score = F("like") - 1
        obj.save(update_fields=["like"])
    else:
        return HttpResponse(status=400)
    obj.refresh_from_db()
    return JsonResponse({"like": obj.like, "id": id})


class RegistrationView(generic.FormView):
    form_class = CustomUserCreationForm
    template_name = "forum/signup.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
