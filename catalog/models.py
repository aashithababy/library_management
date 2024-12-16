from django.db import models
import re
from django.core.exceptions import ValidationError
from django.db import models


# Access Restrictions Table
class AccessRestriction(models.Model):
    restriction_id = models.AutoField(primary_key=True)
    membership_type = models.CharField(max_length=255)
    allow_bestseller = models.BooleanField()
    allow_early_release = models.BooleanField()

# Custom validator to allow both URLs and local paths
def validate_url_or_local_path(value):
    # URL validation (basic validation to check if it's a URL)
    url_pattern = r'^(https?://|ftp://|file://)?([a-zA-Z0-9-]+\.)+[a-zA-Z0-9]{2,6}(/[\w\-\._~:/?#[\]@!$&\'()*+,;=]*)?$'
    
    # Local path validation (basic check for local paths)
    local_path_pattern = r'^[a-zA-Z0-9_\-\\\/\.:]+$'
    
    if not re.match(url_pattern, value) and not re.match(local_path_pattern, value):
        raise ValidationError("Invalid URL or local path.")

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)  # ForeignKey to Author
    genre = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    published_year = models.PositiveIntegerField()
    isbn = models.CharField(max_length=13)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_bestseller = models.BooleanField()
    is_early_release = models.BooleanField()
    content_link = models.URLField(null=True, blank=True, validators=[validate_url_or_local_path])
    access_level = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_count = models.PositiveIntegerField(null=True, blank=True)
    popularity_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['author']

    def __str__(self):
        return self.title


class YourModel(models.Model):
    content_link = models.URLField(null=True, blank=True, validators=[validate_url_or_local_path])


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    bio = models.TextField()
    nationality = models.CharField(max_length=255, null=True, blank=True)  # Optional
    birth_date = models.DateField(null=True, blank=True)  # Optional
    death_date = models.DateField(null=True, blank=True)  # Optional
    def __str__(self):
        return self.name


# Genre Table
class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='genres')
    genre_name = models.CharField(max_length=255)
    is_early_release = models.BooleanField()
    is_bestseller = models.BooleanField()

# Subscription Plans Table
class SubscriptionPlan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=255)
    book_rent_limit = models.PositiveIntegerField()
    rent_duration_week = models.PositiveIntegerField()

# Cart Table
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_added = models.DateField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50)

# Rented Books Table
class RentedBook(models.Model):
    rental_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rent_start_date = models.DateField()
    rent_end_date = models.DateField()
    status = models.CharField(max_length=50)

# Admin Book Action Table
class AdminBookAction(models.Model):
    action_id = models.AutoField(primary_key=True)
    admin_id = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
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