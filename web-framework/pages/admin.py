from django.contrib import admin

from .models import Book

class BookAdmin(Book):
    model = Book

admin.site.register(Book,)