from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView

from posts.models import Post
from .forms import RegisterForm, UserProfileForm
from .models import UserProfile

from braces.views import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = '/'


class UserLoginView(LoginView):

    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    template_name = 'users/login.html'

# braces의 Mixin을 사용해보았다. 강의에서는 get메서드를 오버라이드하여 구현.
#@method_decorator(login_required(login_url='users/login'), name="dispatch")
class UserProfileUpdateView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin, UpdateView):
    model = UserProfile
    template_name = 'users/profile-update.html'
    form_class = UserProfileForm

    success_message = 'Your Profile Has Been Updated!!!'


    redirect_unauthenticated_users = True
    raise_exception = True

    def test_func(self, user):
        user_slug = get_object_or_404(UserProfile, slug=self.kwargs.get('slug'))
        #return user_slug == self.request.user로 잘못 작성했었다. 프로파일을 업데이트하려는 유저가 현재 로그인 되어있는 유저가 같더라도 403 에러 발생.
        return user_slug.user == self.request.user

    # def get(self, request, *args, **kwargs):
    #     self.object =self.get_object()
    #     if self.object.user != request.user:
    #         return HttpResponseRedirect('/')
    #     return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)    #return 까먹지마라

    def get_success_url(self):
        return reverse('users:update_profile', kwargs={"slug":self.object.slug})

@method_decorator(login_required(login_url='users/login'), name="dispatch")
class UserProfileView(ListView):
    model = Post
    template_name = 'users/my-profile.html'
    context_object_name = 'userposts'

    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userprofile'] = UserProfile.objects.get(user=self.request.user)
        return context

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-publishing_date')


class UserPostView(ListView):
    template_name = 'users/user-post.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(user=self.kwargs['pk'])    #self.kwargs.get('pk')

class UserListView(ListView):
    template_name = 'users/user-list.html'
    model = UserProfile
    context_object_name = 'profiles'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
