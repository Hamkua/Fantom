from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Category, Tag
from .forms import PostCreationForm, PostUpdateForm
# Create your views here.

class IndexView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['categories'] = Category.objects.all()
        context['slider_posts'] = Post.objects.all().filter(slider_post=True)
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


class TagDetail(ListView):
    model = Post
    template_name = 'tags/tag_detail.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(tag=self.tag).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        context['tag'] = self.tag
        return context

@method_decorator(login_required(login_url='users/login'), name="dispatch")
class CreatePostView(CreateView):
    model = Post
    form_class = PostCreationForm
    template_name = 'posts/create-post.html'

    def get_success_url(self):
        return reverse('detail', kwargs={'pk':self.object.pk, 'slug':self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()

        tags = self.request.POST.get('tag').split(",")

        # 강의에서는 다음과 같이 구현,
        # for tag in tags:
        #     current_tag = Tag.objects.filter(slug=slugify(tag))
        #     if current_tag.count() < 1:
        #         create_tag = Tag.objects.create(title=tag)
        #         form.instance.tag.add(create_tag)
        #     else:
        #         exist_tag = Tag.objects.get(title=tag)
        #         form.instance.tag.add(exist_tag)
        # return super(CreatePostView, self).form_valid(form)

        # Mastering Djnago 교재로 공부하며 배운 get_or_create 사용, 위와 똑같은 기능이다.
        for tag in tags:
            current_tag = Tag.objects.get_or_create(title=tag)

            form.instance.tag.add(current_tag[0])
        return super().form_valid(form)

class UpdatePostView(UpdateView):
    model = Post
    template_name = 'posts/post-update.html'
    form_class = PostUpdateForm

    def get_success_url(self):
        return reverse('detail', kwargs={'pk':self.object.pk, 'slug':self.object.slug})

