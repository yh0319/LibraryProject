from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Customuser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Customuser
        fields = ('username', 'email', 'mName', 'sex', 'birth')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Customuser
        fields = UserChangeForm.Meta.fields