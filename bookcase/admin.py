from django.contrib import admin

from bookcase.models import Book, Author, Publisher, Borrowing


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Borrowing)
