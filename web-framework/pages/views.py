from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.views import generic
from pages.models import Books


class HomePageView(TemplateView):
    print('---HomePageView---')
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        print('--get_context_data--')
        context = super(HomePageView, self).get_context_data(**kwargs)
        #context['object_list'] = Book.objects.order_by('-loanCnt')[:5]
        my_ids = Book.objects.values_list('bName', flat=True)
        my_ids = list(my_ids)
        n = 4   
        rand_ids = random.sample(my_ids, n)
        print('--random id :', rand_ids)
        random_records = Book.objects.filter(bName__in=rand_ids)
        print('---random :',random_records)       
        context['object_list'] = random_records
        return context


class SearchPageView(TemplateView):
    print('---SearchPageView---')
    template_name = 'search.html'

