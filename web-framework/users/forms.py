from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Customuser

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='아이디(ID)')
    email = forms.CharField(label='이메일(email)')
    sex = forms.CharField(label='성별')
    birth = forms.CharField(label='생년월일')
    mName = forms.CharField(label='이름')

    class Meta(UserCreationForm):
        model = Customuser
        fields = ('username', 'email', 'mName', 'sex', 'birth')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Customuser
        fields = UserChangeForm.Meta.fields


        