from django.shortcuts import render
from django.views.generic import ListView, DetailView
from forum.models import Category, Thread, Post

class CategoryView(ListView):
    model = Category

class CategoryDetailView(DetailView):
    model = Category

class ThreadView(DetailView):
    model = Thread