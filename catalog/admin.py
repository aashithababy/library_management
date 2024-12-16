from django.contrib import admin
from .models import Book,Author
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
from .forms import BookForm
from django.urls import reverse

from django.shortcuts import render, redirect
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors_name', 'genre', 'published_year', 'price')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['add_book_button'] = format_html(
            '<a class="button" href="{}" style="margin-bottom: 15px;">+ Add Book</a>',
            reverse('admin:catalog_book_add')
        )
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Book, BookAdmin)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'nationality', 'birth_date', 'death_date')
    search_fields = ('name', 'nationality')