from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q
from django.core.paginator import Paginator

from django.http import HttpResponse, HttpResponseRedirect
from pages.models import Book, Bestbook
import random

from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet

class HomePageView(TemplateView):
    print('---HomePageView---')
    template_name = 'home.html'

    def get_context_data(self,*args, **kwargs):
        print('--get_context_data--')
        context = super(HomePageView, self).get_context_data(**kwargs)
        data = Book.objects.order_by('-loanCnt')[:100]
        print('--data : ', data)
        my_ids = data.values_list('bName', flat=True)
        my_ids = list(my_ids)
        n = 4   
        rand_ids = random.sample(my_ids, n)
        print('--random id :', rand_ids)
        random_records = Book.objects.filter(bName__in = rand_ids)
        print('---random :',random_records)       
        context['object_list'] = random_records
        return context


class SearchPageView(SearchView):
    print('---SearchPageView---')
    template_name = 'search/search.html'
    queryset = SearchQuerySet().order_by('-loanCnt')
    print('----queryset', queryset)




class BookListView(ListView):
    print('----bookListView---')
    model= Bestbook
    template_name = 'pages/book.html'

    def get_queryset(self):
        return  Bestbook.objects.all().order_by('ranking')

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        context['teen'] = Bestbook.objects.filter(age__in=[10])
        context['twenty'] = Bestbook.objects.filter(age__in=[20])
        context['thirty'] = Bestbook.objects.filter(age__in=[30])
        print('---thirty', context['thirty'])
        
        context['forty'] = Bestbook.objects.filter(age__in=[40])
        context['fifty'] = Bestbook.objects.filter(age__in=[50])        
        # Add any other variables to the context here
        return context



class MovieListView(ListView):
    print('----MovieListView---')
    model= Book
    template_name = 'pages/movie.html'


