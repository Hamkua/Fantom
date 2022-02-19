from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post, Category, Tag
from .forms import PostCreationForm, PostUpdateForm

from braces.views import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

class IndexView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'

    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['categories'] = Category.objects.all()
        context['slider_posts'] = Post.objects.all().filter(slider_post=True)
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'single'

    def get(self, request, *args, **kwargs):
        self.hit = Post.objects.filter(id=self.kwargs['pk']).update(hit=F('hit')+1)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['previous'] = Post.objects.all().filter(id__lt=self.kwargs['pk']).order_by('-pk').first()
        context['next'] = Post.objects.all().filter(id__gt=self.kwargs['pk']).order_by('pk').first()
        return context


class CategoryDetail(ListView):
    model = Post
    template_name = 'categories/category_detail.html'
    context_object_name = 'posts'
    paginate_by = 5

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
    paginate_by = 5

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

# @method_decorator(login_required(login_url='users/login'), name="dispatch")
# braces의 mixin 임포트하여 사용해 보았음.
class UpdatePostView(LoginRequiredMixin,UpdateView):
    model = Post
    template_name = 'posts/post-update.html'
    form_class = PostUpdateForm

    def get_success_url(self):
        return reverse('detail', kwargs={'pk':self.object.pk, 'slug':self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user

        #기존 값 삭제
        form.instance.tag.clear()

        tags = self.request.POST.get('tag').split(",")
        for tag in tags:
            current_tag = Tag.objects.get_or_create(title=tag)

            form.instance.tag.add(current_tag[0])
        return super().form_valid(form)

    # braces의 UserPassesTestMixin을 사용해도 됨.
    # get 메서드 처음봄. CBV의 메서드인데, get_context_data를 실행, context를 렌더링하는 메서드로 전달하는 역할을 하는 것 같다. https://ccbv.co.uk/projects/Django/4.0/django.views.generic.base/TemplateView/
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super().get(request, *args, **kwargs)

#강의에서는 사용하지 않은 braces의 Mixin을 사용해 보았다.
class DeletePostView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'posts/delete.html'

    redirect_unauthenticated_users = True
    raise_exception = True
    def test_func(self, user):
        self.object = self.get_object()
        return self.object.user == user

    # 강의에서는 다음과 같이 구현,
    # def delete(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     if self.object.user == request.user:
    #         self.object.delete()
    #         return HttpResponseRedirect(self.success_url)
    #     else:
    #         return HttpResponseRedirect(self.success_url)
    #
    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_queryset()
    #     if self.object.user != request.user:
    #         return HttpResponseRedirect('/')
    #     return super().get(request, *args, **kwargs)

class SearchView(ListView):
    model = Post
    template_name = 'posts/search.html'
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.all().filter(Q(title__icontains=query)|Q(content__icontains=query)|Q(tag__title__icontains=query)).order_by('-publishing_date').distinct()

        return Post.objects.all().order_by('-publishing_date')