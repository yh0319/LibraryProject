from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),   #http://127.0.0.1:8000/
    path('/search/', views.HomePageView.as_view(), name='search'),   #http://127.0.0.1:8000/
]