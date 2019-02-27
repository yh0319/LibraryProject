from django.urls import path
from django_filters.views import FilterView
from pages.filters import BookFilter
from . import views



urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),   #http://127.0.0.1:8000/
    path('/search/', FilterView.as_view(filterset_class=BookFilter, template_name='search/search.html')),
    # path(r'/search/', views.SearchPageView.as_view(), name='search'),   #http://127.0.0.1:8000/search/
    path('book/', views.BookListView.as_view(), name='book'),
    path('movie/', views.MovieListView.as_view(), name='movie'),
]