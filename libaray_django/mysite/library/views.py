from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.shortcuts import render
from django.http import HttpResponse

from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse


def home(request):
    print("---------home()-------------")
    return render(request, 'library/home.html')


def index(request):
    return HttpResponse("Hello, world. You're at the library index.")