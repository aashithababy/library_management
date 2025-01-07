import datetime
from django import forms
from .models import Author, Book, Genre
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, URLValidator

import os
import re


# Custom validator to check if the content_link is a valid URL or a local file path
def validate_url_or_local_path(value):
    url_validator = URLValidator()
    try:
        url_validator(value)
        return value
    except ValidationError:
        pass

    # Check for a valid local file path
    if os.path.isfile(value):
        return value
    raise ValidationError('Invalid URL or local file path for content.')

class BookForm(forms.ModelForm):
    author_name = forms.CharField(
        max_length=255,
        required=True,
        label='Author Name',
        widget=forms.TextInput(attrs={'placeholder': 'Type author name', 'id': 'author-name-input'})
    )
    genre_name = forms.CharField(
        required=False, 
        label="New Genre",
        widget=forms.TextInput(attrs={
            'id': 'genre-name-input',
            'class': 'form-control',
            'placeholder': 'Enter genre name'
        })
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    content_link = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'placeholder': 'Upload file or enter URL'}),
        validators=[validate_url_or_local_path]
    )

    class Meta:
        model = Book
        fields = '__all__' 

    def save(self, commit=True):
        # Handle Author Creation
        author_name = self.cleaned_data.get('author_name')
        author, created = Author.objects.get_or_create(name=author_name)

        # Handle Genre Creation
        genre_name = self.cleaned_data.get('genre_name')
        if genre_name:
            genre, created = Genre.objects.get_or_create(genre_name=genre_name)
            self.cleaned_data['genres'].add(genre)

        # Save the book instance
        instance = super().save(commit=False)
        instance.author = author  

        if commit:
            instance.save()
            self.save_m2m()  # Save the many-to-many genres properly
        return instance

# AuthorForm
from django import forms
from .models import Author
import datetime

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio', 'nationality', 'birth_date', 'death_date', 'profile_picture']

    # Custom validation for name
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Author name is required.')
        return name

    # Custom validation for bio
    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if bio and len(bio) < 10:  # Example check: bio should be at least 10 characters long
            raise forms.ValidationError('Bio must be at least 10 characters long.')
        return bio

    # Custom validation for nationality (optional)
    def clean_nationality(self):
        nationality = self.cleaned_data.get('nationality')
        if nationality:  # Only validate if nationality is provided
            if len(nationality) < 2:
                raise forms.ValidationError('Please enter a valid nationality (at least 2 characters).')
            if not nationality.isalpha():
                raise forms.ValidationError('Nationality should only contain alphabetic characters.')
        return nationality
    
    # Custom validation for birth date (optional)
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:  # Only validate if birth date is provided
            if birth_date > datetime.date.today():
                raise forms.ValidationError('Birth date cannot be in the future.')
        return birth_date

    # Custom validation for death date (optional, and consistency with birth date)
    def clean_death_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        death_date = self.cleaned_data.get('death_date')

        if death_date:  # Only validate if death date is provided
            if death_date > datetime.date.today():
                raise forms.ValidationError('Death date cannot be in the future.')
            if birth_date and death_date < birth_date:
                raise forms.ValidationError('Death date cannot be earlier than birth date.')
            
        return death_date

    # Custom validation for profile picture
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture and not profile_picture.name.endswith(('.jpg', '.jpeg', '.png')):
            raise forms.ValidationError("Profile picture must be an image file (.jpg, .jpeg, .png).")
        return profile_picture
    
# GenreForm
class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['genre_name']

    def clean_genre_name(self):
        genre_name = self.cleaned_data.get('genre_name')
        if not genre_name:
            raise ValidationError('Genre name is required.')
        return genre_name
