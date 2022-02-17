from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=50)
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        # User 모델을 사용하는 것은 쉽고 간단하지만, User모델에 정의되어 있지 않은 추가 필드가 필요한 경우, 아주 까다롭기 때문에 권장X
        model = User
        fields = ['username', 'email', 'password1', 'password2']
