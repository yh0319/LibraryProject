import django_filters
from pages.models import Book


class BookFilter(django_filters.FilterSet):

    bName = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Book
        fields = ['bName', 'author','publisher', ]