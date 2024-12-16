from django import forms
from .models import Book, Genre,Author
class BookForm(forms.ModelForm):
    authors_name = forms.CharField(
        max_length=255,
        required=True,
        label='Author Name',
        widget=forms.TextInput(attrs={'placeholder': 'Type author name'})
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
            try:
                Author.objects.get(name=authors_name)
            except Author.DoesNotExist:
                raise forms.ValidationError(f"Author '{authors_name}' does not exist. Please add them first.")
        return authors_name

    def save(self, commit=True):
        authors_name = self.cleaned_data.get('authors_name')
        author, created = Author.objects.get_or_create(name=authors_name)

        # Save the book with the correct author
        book = super().save(commit=False)
        book.authors_name = authors_name  # Assign the author's name field
        if commit:
            book.save()
            author.books.add(book)  # Add the book to the author's book set
        return book

    # Optional custom validation for the price fields
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('Price must be greater than 0.')
        return price

    def clean_rent_price(self):
        rent_price = self.cleaned_data.get('rent_price')
        if rent_price is None:
            raise forms.ValidationError('Rent price is required.')
        if rent_price <= 0:
            raise forms.ValidationError('Rent price must be greater than 0.')
        return rent_price

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio', 'nationality', 'birth_date', 'death_date']

        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'death_date': forms.DateInput(attrs={'type': 'date'}),
        }