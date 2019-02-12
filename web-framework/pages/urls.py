from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),   #http://127.0.0.1:8000/
    path('books/', views.BookListView.as_view(), name='books'),   #http://127.0.0.1:8000/books/
]