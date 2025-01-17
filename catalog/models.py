from django import forms
from django.db import models
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Validator for URLs, local file paths, and PDF filenames
def validate_url_or_local_path(value):
    # Define the regular expression patterns
    url_pattern = r'^(https?://|ftp://|file://).+$'  # For URLs
    local_path_pattern = r'^[a-zA-Z]:\\\\(?:[^<>:"/\\\\|?*]+\\\\)*[^<>:"/\\\\|?*]*$'  # For local file paths
    pdf_filename_pattern = r'^.+\.pdf$'  # For PDF filenames
    
    if isinstance(value, str):  # If the value is already a string, proceed with validation
        if not (re.match(url_pattern, value) or 
                re.match(local_path_pattern, value) or 
                re.match(pdf_filename_pattern, value)):
            raise ValidationError("Invalid value. Must be a URL, a local file path, or a PDF filename.")
    elif hasattr(value, 'url'):  # If the value is a FileField (FieldFile), access its URL
        file_url = value.url
        if not (re.match(url_pattern, file_url) or re.match(pdf_filename_pattern, file_url)):
            raise ValidationError("Invalid value. Must be a URL or a PDF filename.")
    elif hasattr(value, 'path'):  # If it's a local file, access its path
        file_path = value.path
        if not (re.match(local_path_pattern, file_path) or re.match(pdf_filename_pattern, file_path)):
            raise ValidationError("Invalid value. Must be a local file path or a PDF filename.")
    else:
        raise ValidationError("Invalid value. Must be a URL, a local file path, or a PDF filename.")

# Genre Table
class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=255)

    def __str__(self):
        return self.genre_name

# Author Table
class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    bio = models.TextField()
    nationality = models.CharField(max_length=255, null=True, blank=True)  # Optional
    birth_date = models.DateField(null=True, blank=True)  # Optional
    death_date = models.DateField(null=True, blank=True)  # Optional
    profile_picture = models.ImageField(upload_to='authors/', blank=True, null=True)

    def __str__(self):
        return self.name

# Book Table
class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)  # ForeignKey to Author
    genres = models.ManyToManyField(Genre, blank=True)
    description = models.TextField(null=True, blank=True)
    published_year = models.PositiveIntegerField()
    isbn = models.CharField(max_length=13,unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_bestseller = models.BooleanField()
    is_early_release = models.BooleanField()
    content_link = models.URLField(blank=True, null=True)
    content_file = models.FileField(upload_to='books/', blank=True, null=True)    
    access_level = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_count = models.PositiveIntegerField(null=True, blank=True)
    popularity_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True,validators=[MinValueValidator(1), MaxValueValidator(5)] )
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    cover_image = models.ImageField(upload_to='books/', null=True, blank=True)  
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['author']
        unique_together = ['title', 'isbn']

    def __str__(self):
        return self.title
    
    def clean(self):
        if not self.is_available and self.stock > 0:
            raise forms.ValidationError("A book marked as unavailable cannot have stock greater than zero.")
        if self.is_available and self.stock == 0:
            raise forms.ValidationError("A book marked as available must have stock greater than zero.")

# CatalogBookGenre Table
class CatalogBookGenre(models.Model):
    catalog_book_genre_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title} - {self.genre.genre_name}"

# YourModel Table
class YourModel(models.Model):
    content_link = models.URLField(null=True, blank=True, validators=[validate_url_or_local_path])

# Cart Table
# models.py in the catalog app

from django.db import models
from django.contrib.auth.models import User


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='active')

    def __str__(self):
        return f"Cart for {self.user.username} - {self.status}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book.title} x {self.quantity} in cart {self.cart.id}"

# RentedBooks Table
class RentedBook(models.Model):
    rental_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rent_start_date = models.DateField()
    rent_end_date = models.DateField()
    status = models.CharField(max_length=50)

# Admin Book Action Table
class AdminBookAction(models.Model):
    action_id = models.AutoField(primary_key=True)
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    action_date = models.DateField()
    details = models.TextField()

# Our Bestsellers Table
class OurBestseller(models.Model):
    bestseller_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_bestseller = models.BooleanField()
    is_early_release = models.BooleanField()

    def __str__(self):
        return f"Bestseller: {self.book.title}"

# Everyone's Talking About Table
class EveryoneTalkingAbout(models.Model):
    talking_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_bestseller = models.BooleanField()
    is_early_release = models.BooleanField()

    def __str__(self):
        return f"Talking About: {self.book.title}"

# Our Best Fiction Books Table
class OurBestFictionBook(models.Model):
    fantasy_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_bestseller = models.BooleanField()
    is_early_release = models.BooleanField()

    def __str__(self):
        return f"Best Fiction: {self.book.title}"

# Early Releases Table
class EarlyRelease(models.Model):
    early_release_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_bestseller = models.BooleanField()
    is_early_release = models.BooleanField()

    def __str__(self):
        return f"Early Release: {self.book.title}"

# Author Book Table
class AuthorBook(models.Model):
    author_book_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author.name} - {self.book.title}"

# Our Best Non-Fiction Books Table
class OurBestNonFictionBook(models.Model):
    nonfiction_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_bestseller = models.BooleanField()
    is_early_release = models.BooleanField()

    def __str__(self):
        return f"Best Non-Fiction: {self.book.title}"
