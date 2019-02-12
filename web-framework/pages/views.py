from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.views import generic
from pages.models import Books


class HomePageView(TemplateView):
    print('---HomePageView---')
    template_name = 'home.html'

class BookListView(ListView):
    print('---BookListView---')
    class Meta:
        model = Books
        print('---모델 : ',model)
    
    template_name = 'pages/books.html' #pages/templates/pages/books.html
    
    paginate_by = 10  # Display 10 objects per page

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 10  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context
