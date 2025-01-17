import datetime
from django import forms
from .models import Author, Book, Genre

class BookForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=True)
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), required=False)

    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'published_year', 'isbn', 'price', 'rent_price', 'is_bestseller', 'is_early_release', 'cover_image', 'is_available', 'genres','content_link', 'content_file', 
                  'cover_image', 'rating','is_available','stock']
        
    def clean(self):
        cleaned_data = super().clean()
        is_available = cleaned_data.get('is_available')
        stock = cleaned_data.get('stock')

        if is_available is not None and stock is not None:
            if not is_available and stock > 0:
                raise forms.ValidationError("A book marked as unavailable cannot have stock greater than zero.")
            if is_available and stock == 0:
                raise forms.ValidationError("A book marked as available must have stock greater than zero.")
        return cleaned_data

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if len(isbn) not in [10, 13]:
            raise forms.ValidationError("ISBN must be 10 or 13 digits long.")
        return isbn

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError("Price must be a positive value.")
        return price

    def clean_published_year(self):
        year = self.cleaned_data.get('published_year')
        if year < 1000 or year > 9999:
            raise forms.ValidationError("Please enter a valid year between 1000 and 9999.")
        return year

    def clean_genre_name(self):
        genre_name = self.cleaned_data.get('genre_name')
        if genre_name and Genre.objects.filter(genre_name=genre_name).exists():
            raise forms.ValidationError("This genre already exists.")
        return genre_name
    
    def clean_title_and_isbn(self):
        title = self.cleaned_data.get('title')
        isbn = self.cleaned_data.get('isbn')

        # Check if a book with the same title and ISBN already exists
        if Book.objects.filter(title=title, isbn=isbn).exists():
            raise forms.ValidationError("A book with this title and ISBN already exists.")

        return self.cleaned_data
    
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        
        # Add 'form-control' class to all form fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Add 'form-select' class to select fields like author and genres
        self.fields['author'].widget.attrs.update({'class': 'form-select'})
        self.fields['genres'].widget.attrs.update({'class': 'form-select'})

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio', 'nationality', 'birth_date', 'death_date', 'profile_picture']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Author name is required.')
        return name

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if bio and len(bio) < 10:
            raise forms.ValidationError('Bio must be at least 10 characters long.')
        return bio

    def clean_nationality(self):
        nationality = self.cleaned_data.get('nationality')
        if nationality:
            if len(nationality) < 2:
                raise forms.ValidationError('Please enter a valid nationality (at least 2 characters).')
            if not nationality.replace(" ", "").isalpha():
                raise forms.ValidationError('Nationality should only contain alphabetic characters.')
        return nationality

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            if birth_date > datetime.date.today():
                raise forms.ValidationError('Birth date cannot be in the future.')
        return birth_date

    def clean_death_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        death_date = self.cleaned_data.get('death_date')

        if death_date:
            if death_date > datetime.date.today():
                raise forms.ValidationError('Death date cannot be in the future.')
            if birth_date and death_date < birth_date:
                raise forms.ValidationError('Death date cannot be earlier than birth date.')
            
        return death_date

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['genre_name']

    def clean_genre_name(self):
        genre_name = self.cleaned_data.get('genre_name').strip()

        # Check for alphabetic characters only
        if not genre_name.isalpha():
            raise forms.ValidationError('Genre name must contain only letters.')

        # Capitalize the first letter
        genre_name = genre_name.capitalize()

        # Check if the genre already exists
        if Genre.objects.filter(genre_name__iexact=genre_name).exists():
            raise forms.ValidationError('This genre already exists.')

        return genre_name