from django.contrib import admin
from .models import Book, Author, Genre
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
from .forms import BookForm, forms
from django.urls import reverse
from django.shortcuts import render, redirect

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'nationality', 'birth_date', 'death_date','profile_picture')
    search_fields = ('name', 'nationality')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_genres', 'published_year', 'isbn', 'price','cover_image','content_link_display')  # Display genres in the list view

    def content_link_display(self, obj):
        if obj.content_link:
            # Create a dynamic URL to serve the PDF
            pdf_url = reverse('serve_pdf', args=[obj.content_link.name])
            return format_html('<a href="{}" target="_blank">Open PDF</a>', pdf_url)
        return "No Link"
    content_link_display.short_description = "Content Link"

    # Display genres in a readable format
    def get_genres(self, obj):
        return ", ".join([genre.genre_name for genre in obj.genres.all()])
    get_genres.short_description = 'Genres'

    # Add the genres field to the form
    filter_horizontal = ('genres',)  # Makes the genres field available as a filter in the admin form

    def save_model(self, request, obj, form, change):
        obj.save()
        # Add genre handling logic if needed
        return super().save_model(request, obj, form, change)

    def clean_authors_name(self):
        authors_name = self.cleaned_data.get('authors_name')
        if authors_name:
            # Check if the author exists in the database
            if not Author.objects.filter(name=authors_name).exists():
                raise forms.ValidationError(f"Author '{authors_name}' does not exist. Please add them first.")
        return authors_name

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre_name',)
    search_fields = ('genre_name',)


