from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Customuser

class CustomUserAdmin(UserAdmin):
    model = Customuser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

admin.site.register(Customuser, CustomUserAdmin)