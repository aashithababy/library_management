import datetime
import logging
import re
from venv import logger
from django.db import IntegrityError
from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Book, Author,Genre
from .forms import BookForm,AuthorForm
from django.http import HttpResponseForbidden
from django.contrib import messages
from accounts.models import UserMembership

# List all available books
from django.db.models import Q


def book_list(request):
    query = request.GET.get('q', '')  # Get the query parameter from the URL
    if query:
        # Filter books based on the search query (title or author's name)
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)
        )
    else:
        # Show all books if no search query
        books = Book.objects.all()

    # Pass the books queryset to the template
    return render(request, 'catalog/book_list.html', {'books': books})


def book_detail(request, pk):
    # Retrieve the book by its primary key
    book = get_object_or_404(Book, pk=pk)

    # Clean up the description by removing unwanted newlines and replacing them with spaces
    cleaned_description = book.description.replace('\n', ' ').replace('\r', ' ').replace('/n', ' ').replace('/r', ' ')

    # Split the cleaned description into paragraphs (separated by double newlines)
    paragraphs = cleaned_description.split('  ')  # Double space to split paragraphs

    # Retrieve the user's membership and subscription details if authenticated
    user_membership = None
    if request.user.is_authenticated:
        try:
            user_membership = UserMembership.objects.get(user=request.user)
        except UserMembership.DoesNotExist:
            user_membership = None

    # Pass book and membership details to the template, along with the list of paragraphs
    context = {
        'book': book,
        'user_membership': user_membership,
        'paragraphs': paragraphs,  # List of paragraphs
    }
    return render(request, 'catalog/book_detail.html', context)

@login_required
def add_book(request):
    book_form_data = request.session.get('book_form_data', None)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Clear the stored session data after successful save
            if 'book_form_data' in request.session:
               del request.session['book_form_data']

            return redirect('book_list')
    else:
        form = BookForm(initial=book_form_data if book_form_data else {})

    return render(request, 'catalog/add_book.html', {'form': form})

from django.http import JsonResponse
from .forms import BookForm


def validate_form(request):
    if request.method == 'POST' and request.is_ajax():
        form = BookForm(request.POST)
        errors = {}

        # Validate each field individually
        for field in form.fields:
            # Only validate if the field is being processed
            form_field = form.fields[field]
            field_value = request.POST.get(field)
            if field_value:
                form_field.widget.attrs['value'] = field_value
            if not form_field.is_valid():
                errors[field] = form_field.errors

        return JsonResponse({'errors': errors})

    return JsonResponse({'errors': {}})


def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_author_name_unique(author_name):
    return Author.objects.filter(name=author_name).exists()

def validate_author_name(author_name):
    if is_author_name_unique(author_name):
        raise ValidationError("Author with this name already exists.")

@login_required
def author_validate(request):
    if request.method == 'POST':
        field = request.POST.get('field')
        value = request.POST.get('value')

        errors = {}
        try:
            if field == 'new_author_name':
                if not value:
                    raise ValidationError("Author name is required.")
                if Author.objects.filter(name=value).exists():
                    raise ValidationError("Author with this name already exists.")

            elif field == 'new_author_nationality' and value and len(value) < 2:
                raise ValidationError("Nationality must be at least 2 characters long.")

            elif field == 'new_author_birth_date' and value and not validate_date(value):
                raise ValidationError("Invalid date format. Use YYYY-MM-DD.")
                
        except ValidationError as e:
            errors[field] = str(e)

        return JsonResponse({'valid': not bool(errors), 'errors': errors})

    return JsonResponse({'valid': False, 'errors': {'non_field': ['Invalid request method.']}})

@login_required
def search_author(request):
    author_name = request.GET.get('name', '').strip()
    exists = Author.objects.filter(name=author_name).exists()
    return JsonResponse({'exists': exists})

@login_required
def search_genre(request):
    genre_name = request.GET.get('name', '').strip()
    exists = Genre.objects.filter(name=genre_name).exists()
    return JsonResponse({'exists': exists})

@login_required
def confirm_add_author(request):
    author_name = request.session.get('new_author_name')
    if not author_name:
        # Handle the case where session data is missing
        messages.error(request, "No author data found in session.")
        return redirect('add_book')

    if request.method == 'POST':
        author = Author(name=author_name)
        author.save()
        request.session['new_author_name'] = None  # Clear session data after saving
        messages.success(request, f"Author '{author_name}' added successfully!")
        return redirect('add_book')  # Redirect to book form

    return render(request, 'catalog/confirm_add_author.html', {'author_name': author_name})

from django.shortcuts import render, redirect
from .forms import GenreForm
from .models import Genre

@login_required
def add_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        
        if form.is_valid():
            genre_name = form.cleaned_data.get('genre_name').strip()

            # Check for duplicate genre
            if Genre.objects.filter(genre_name__iexact=genre_name).exists():
                form.add_error('genre_name', 'This genre already exists.')
            else:
                form.save()  # Save the genre to the database
                return redirect('add_book')  # Redirect back to the book form

    else:
        form = GenreForm()

    # Fetch existing genres to display
    existing_genres = Genre.objects.all()

    return render(request, 'catalog/add_genre.html', {'form': form, 'existing_genres': existing_genres})


# Add Genre Confirmation View
@login_required
def confirm_add_genre(request):
    genre_id = request.session.get('new_genre_id')
    genre_name = request.session.get('new_genre_name')
    if request.method == 'POST':
        genre = Genre.objects.create(name=genre_name)
        request.session['new_genre_id'] = None  # Clear session data
        messages.success(request, f"Genre '{genre_name}' added successfully!")
        return redirect('add_book')  # Return to the book form

    return render(request, 'catalog/confirm_add_genre.html', {'genre_name': genre_name})

logger = logging.getLogger(__name__)

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the author to the database
            request.session['book_form_data'] = request.POST
            return redirect('add_book')  # Redirect to the book form
    else:
        form = AuthorForm()
    
    return render(request, 'catalog/add_author.html', {'form': form})
    

def author_list(request):
    authors = Author.objects.all()

    return render(request, 'catalog/author_list.html', {'authors': authors})

def author_detail(request, id):
    author = get_object_or_404(Author, id=id)
    return render(request, 'catalog/author_detail.html', {'author': author})


def search_author_suggestions(request):
    query = request.GET.get('query', '').strip()
    suggestions = list(Author.objects.filter(name__icontains=query).values_list('name', flat=True))[:5]
    return JsonResponse(suggestions, safe=False)

def check_author_existence(request):
    query = request.GET.get('query', '').strip()
    author_exists = Author.objects.filter(name__iexact=query).exists()
    return JsonResponse({'exists': author_exists})

# Update a book (Admin Only)
@login_required
def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'catalog/update_book.html', {'form': form})

from django.http import JsonResponse

from django.http import FileResponse, Http404
import os
from django.conf import settings

@login_required
def serve_pdf(request, file_name):
    pdf_directory = os.path.join(settings.MEDIA_ROOT, 'books')  
    pdf_path = os.path.join(pdf_directory, file_name)

    if os.path.exists(pdf_path):
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    else:
        raise Http404("PDF file not found.")

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Book, Cart,CartItem
from django.utils import timezone
from accounts.models import User  # Import the custom User model

@login_required
def add_to_cart(request, book_id):
    # Retrieve the book object
    try:
        book = Book.objects.get(book_id=book_id)
    except Book.DoesNotExist:
        return HttpResponse("Book not found", status=404)

    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if not logged in

    # Ensure the user is an instance of the custom User model
    if not isinstance(request.user, User):
        return HttpResponse("Invalid user", status=400)

    # Get or create the cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user, status='active')

    # Check if the book is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

    # Update the quantity
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    # Return a JSON response with the new quantity
    return JsonResponse({
        'status': 'success',
        'message': 'Book added to cart',
        'new_quantity': cart_item.quantity
    })


# View for displaying the cart
@login_required
def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not logged in

    # Get the active cart for the logged-in user
    cart = Cart.objects.filter(user=request.user, status='active').first()
    if not cart:
        return render(request, 'catalog/cart_empty.html')  # Render an empty cart if no active cart is found

    # Get the items in the cart
    cart_items = cart.items.all()

    # Calculate the total price for each item and add it to the context
    cart_items_with_totals = []
    for item in cart_items:
        item_total = item.book.price * item.quantity  # Calculate total price for this item
        cart_items_with_totals.append({
            'item': item,
            'item_total': item_total
        })

    # Calculate the overall total price for the cart
    total_price = sum(item['item_total'] for item in cart_items_with_totals)

    # Pass the cart items with totals and overall total price to the template
    return render(request, 'catalog/cart.html', {
        'cart_items_with_totals': cart_items_with_totals,
        'total_price': total_price
    })

# Remove item from cart
@login_required
def remove_from_cart(request, book_id):
    try:
        book = Book.objects.get(book_id=book_id)  # Use 'book_id' instead of 'id'
    except Book.DoesNotExist:
        return HttpResponse("Book not found", status=404)

    if not request.user.is_authenticated:
        return redirect('login')

    # Get the active cart for the user
    cart = Cart.objects.filter(user=request.user, status='active').first()
    if not cart:
        return HttpResponse("Cart not found", status=404)

    # Get the cart item and remove it
    cart_item = cart.items.filter(book=book).first()
    if cart_item:
        cart_item.delete()

    return redirect('cart')  # Redirect to cart page after removal

@login_required
def checkout_view(request):
    """
    Redirects to the choose payment page when the user proceeds to checkout.
    """
    # Redirect to choose_payment page
    return redirect(reverse('choose_payment') + "?source_page=cart")

@login_required
def update_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not logged in

    # Get the active cart for the logged-in user
    cart = Cart.objects.filter(user=request.user, status='active').first()
    if not cart:
        return render(request, 'catalog/cart_empty.html')  # Render an empty cart if no active cart is found

    # Loop through the form data to update the quantities
    for key, value in request.POST.items():
        if key.startswith('quantity_'):
            item_id = key.split('_')[1]
            try:
                quantity = int(value)
                cart_item = CartItem.objects.get(id=item_id, cart=cart)
                cart_item.quantity = quantity
                cart_item.save()
            except (ValueError, CartItem.DoesNotExist):
                pass  # Handle invalid values or non-existing cart items gracefully

    # Redirect back to the cart page to reflect changes
    return redirect('cart')

@login_required
def cart_page(request):
    success = request.GET.get("success")
    membership_id = request.GET.get("membership_id")
    return render(request, 'cart.html', {'success': success, 'membership_id': membership_id})


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart, CartItem, Book
from accounts.models import UserMembership, MembershipPlan, SubscriptionPlan

from decimal import Decimal

@login_required
def buy_book(request, book_id):
    # Retrieve the book or return 404 if not found
    book = get_object_or_404(Book, book_id=book_id)
    
    discounted_price = book.price  # Default price (no discount)

    try:
        # Check if the user has a membership and apply discounts
        user_membership = UserMembership.objects.get(user=request.user)
        membership_plan = user_membership.membership_plan

        if membership_plan:
            if membership_plan.name == 'Basic':
                discount = 5  # 5% discount
            elif membership_plan.name == 'Gold':
                discount = 10  # 10% discount
            elif membership_plan.name == 'Platinum':
                discount = 15  # 15% discount
            else:
                discount = 0

            from decimal import Decimal

            discounted_price = book.price * (Decimal('1') - Decimal(discount) / Decimal('100'))

    except UserMembership.DoesNotExist:
        # If no membership, no discount is applied
        pass

    # Add to cart or create an order
    cart, created = Cart.objects.get_or_create(user=request.user, status='active')
    
    # Get or create a CartItem
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

    # Increment the quantity of the cart item
    cart_item.quantity += 1
    cart_item.save()

    # Fetch all cart items and calculate their totals (price * quantity)
    cart_items = cart.items.all()  # This will retrieve all cart items for the active cart
    cart_items_with_totals = []

    cart_total = Decimal('0.00')  # Initialize cart total

    for item in cart_items:
        # Calculate the total price for each item (quantity * discounted price)
        item_total_price = item.quantity * discounted_price
        item_total_price = Decimal(item_total_price).quantize(Decimal('0.01'))  # Round to 2 decimal places
        
        # Add item with its total price to the list
        cart_items_with_totals.append({
            'item': item,
            'total_price': item_total_price
        })
        
        # Add the item's total price to the overall cart total
        cart_total += item_total_price

    # Pass the cart items with totals and the total cart price to the template
    return render(request, 'catalog/cart.html', {
        'cart': cart,
        'cart_items_with_totals': cart_items_with_totals,
        'cart_total': cart_total,
        'discounted_price': discounted_price
    })

from .forms import GenreForm  # Assuming you have created a form for Genre

@login_required
def rent_book(request, book_id):
    book = Book.objects.get(book_id=book_id)

    # Check if the user has a subscription
    try:
        user_membership = UserMembership.objects.get(user=request.user)
        
        if not user_membership.is_subscription_active():
            return redirect('subscription_plans')  # Redirect to subscription page if no active subscription

        # Subscription details
        subscription_plan = user_membership.subscription_plan
        max_books_rented = subscription_plan.max_books_rented
        rented_books = CartItem.objects.filter(cart__user=request.user, cart__status='active', book__isnull=False).count()

        # Ensure user has not exceeded the rental limit
        if rented_books >= max_books_rented:
            return JsonResponse({"error": f"You can only rent {max_books_rented} books at a time."}, status=400)

        # Check if the book can be rented based on the subscription plan
        if (subscription_plan.name == 'Basic' and book.is_bestseller) or \
           (subscription_plan.name == 'Gold' and book.is_early_release):
            return JsonResponse({"error": "This book is not available for rent based on your subscription plan."}, status=400)

    except UserMembership.DoesNotExist:
        # If no membership exists, redirect to subscription page
        return redirect('subscription_plans')

    # Add book to the active cart
    cart, created = Cart.objects.get_or_create(user=request.user, status='active')
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

    cart_item.quantity += 1
    cart_item.save()

    return JsonResponse({"message": "Book added to cart for rent."}, status=200)


def genre_books_view(request, genre_name):
    # Fetch the genre based on the genre_name (slug or name)
    genre = Genre.objects.get(genre_name__iexact=genre_name)
    books = Book.objects.filter(genres=genre)

    # Pass the genre and books to the template
    return render(request, 'catalog/genre_books.html', {'genre': genre, 'books': books})

def genre_list_view(request):
    genres = Genre.objects.all()  # Get all genres
    return render(request, 'catalog/genre_list.html', {'genres': genres})
