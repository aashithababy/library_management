from django.contrib import admin
from .models import Book,Author
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
from .forms import BookForm,forms
from django.urls import reverse
from django.shortcuts import render, redirect


admin.site.register(Book)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'nationality', 'birth_date', 'death_date')
    search_fields = ('name', 'nationality')

class BookAdmin(forms.ModelForm):
    authors_name = forms.CharField(
        max_length=255,
        required=True,
        label='Author Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type author name',
            'id': 'author-name-input'  # Add an ID for JavaScript targeting
        })
    )
    class Meta:
        model = Book
        fields = [
            'title', 'authors_name', 'genre', 'published_year', 'isbn', 'price', 
            'rent_price', 'is_bestseller', 'is_early_release', 'content_link', 
            'access_level', 'read_count', 'popularity_score', 'rating'
        ]

        widgets = {
            'published_year': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
            'isbn': forms.TextInput(attrs={'maxlength': '20'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'rent_price': forms.NumberInput(attrs={'step': '0.01'}),
            'content_link': forms.URLInput(attrs={'placeholder': 'Enter the content link'}),
            'access_level': forms.TextInput(attrs={'maxlength': '50'}),
        }

    def clean_authors_name(self):
        authors_name = self.cleaned_data.get('authors_name')
        if authors_name:
            # Check if the author exists in the database
            if not Author.objects.filter(name=authors_name).exists():
                raise forms.ValidationError(f"Author '{authors_name}' does not exist. Please add them first.")
        return authors_name