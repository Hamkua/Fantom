from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


from users.models import UserProfile


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=50)
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        # User 모델을 사용하는 것은 쉽고 간단하지만, User모델에 정의되어 있지 않은 추가 필드가 필요한 경우, 아주 까다롭기 때문에 권장X
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.field_class = 'mt-10'

        self.helper.layout = Layout(
            Field("birth_day", css_class="single-input"),
            Field("bio", css_class="single-input"),
            Field("image", css_class="single-input"),
        )
        self.helper.add_input(Submit('submit', 'Update', css_class="genric-btn success-border medium"))
    class Meta:
        model = UserProfile
        fields = [
            'birth_day',
            'bio',
            'image'
        ]
        widgets = {
            'birth_day':forms.DateInput(attrs={'type':'date'})
        }
