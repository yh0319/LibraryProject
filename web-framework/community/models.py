from django.db import models

from django.urls import reverse
from users.models import Customuser

class board(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(blank=True)
    title = models.CharField(max_length=200)
    date = models.DateField()
    category = models.CharField(max_length=100)
    place = models.CharField(max_length=200)
    entry = models.IntegerField()
    intro = models.CharField(max_length=300)
    user = models.CharField(max_length=20)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('board_edit', kwargs={'pk': self.pk})