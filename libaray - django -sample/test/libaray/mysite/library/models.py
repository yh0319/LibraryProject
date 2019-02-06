# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # add additional fields in here
    name = models.CharField(max_length=1024)
    birth = models.DateField()
    sex = models.CharField(max_length=1024)

    def __str__(self):
        return self.email

    def __str__(self):
        return self.name

    def __str__(self):
        return self.sex

    def __str__(self):
        return self.birth