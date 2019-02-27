from django.urls import path
# from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'mypage'
urlpatterns = [
    path('', views.LoanListView.as_view(), name = 'index'),
]