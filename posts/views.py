from django.shortcuts import render, get_object_or_404
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

class CategoryDetail(ListView):
    model = Post
    template_name = 'categories/category_detail.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Post.objects.filter(category=self.category).order_by('-id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.category= get_object_or_404(Category, pk=self.kwargs['pk'])
        context['category'] = self.category
        return context