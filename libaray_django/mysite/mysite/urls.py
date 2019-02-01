from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('library/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='library/home.html'), name='home')
]