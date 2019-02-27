from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from community.models import board

class BoardList(ListView):
    model = board

class BoardView(DetailView):
    model = board

class BoardCreate(CreateView):
    model = board
    fields = ['user','image', 'title','date','category','place', 'entry', 'intro']
    success_url = reverse_lazy('Board_list')


class BoardUpdate(UpdateView):
    model = board
    fields = ['user', 'image', 'title','date','category','place', 'entry', 'intro']
    success_url = reverse_lazy('Board_list')

class BoardDelete(DeleteView):
    model = board
    success_url = reverse_lazy('Board_list')


    

