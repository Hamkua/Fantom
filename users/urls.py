from django.urls import path
from .views import *

from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
app_name = 'users'

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('update-profile/<slug:slug>/', UserProfileUpdateView.as_view(), name='update_profile'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]
