from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    username = models.CharField(max_length=255, unique=True)
    mName = models.CharField(max_length=20)
    birth = models.CharField(max_length=10)
    sex = models.CharField(max_length=1)

    def __str__(self):
        return self.email

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class Customuser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    mName = models.CharField(max_length=20)
    birth = models.CharField(max_length=10)
    sex = models.CharField(max_length=1)
    wImage = models.ImageField(max_length=255)

    def __str__(self):
        return self.email

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']