from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category
# Create your views here.

class IndexView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'single'
