from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.views import generic
from pages.models import Books


class HomePageView(TemplateView):
    print('---HomePageView---')
    template_name = 'home.html'


class SearchPageView(TemplateView):
    print('---SearchPageView---')
    template_name = 'search.html'

