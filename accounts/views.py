import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from catalog.models import Book
from .models import UserMembership
from django.http import HttpResponseForbidden

from django.shortcuts import render

from catalog.models import Book


def home(request):
    bestsellers = Book.objects.filter(is_bestseller=True, is_available=True)[:5]
    early_releases = Book.objects.filter(is_early_release=True, is_available=True)[:5]
    trending = Book.objects.order_by('-popularity_score').filter(is_available=True)[:5]
    best_fiction = Book.objects.filter(genres__genre_name='fiction', is_available=True)[:5]
    best_nonfiction = Book.objects.filter(genres__genre_name='nonfiction', is_available=True)[:5]

    # Debugging: Print the number of books returned by each query
    print(f"Bestsellers: {len(bestsellers)}")
    print(f"Early Releases: {len(early_releases)}")
    print(f"Trending: {len(trending)}")
    print(f"Fiction: {len(best_fiction)}")
    print(f"Nonfiction: {len(best_nonfiction)}")

    context = {
        'bestsellers': bestsellers,
        'early_releases': early_releases,
        'trending': trending,
        'fiction': best_fiction,
        'nonfiction': best_nonfiction,
    }
    return render(request, 'home/Home_page.html', context)

from django.http import JsonResponse

def search_books(request):
    query = request.GET.get('q', '').lower()
    if query:
        books = Book.objects.filter(title__icontains=query, is_available=True).values(
            'title', 'cover_image'
        )
        return JsonResponse(list(books), safe=False)
    return JsonResponse([], safe=False)

from django.http import JsonResponse

def get_books_by_category(request, category_name):
    # Determine the filtering conditions based on the category
    if category_name == 'bestsellers':
        books = Book.objects.filter(is_bestseller=True, is_available=True)
    elif category_name == 'early_releases':
        books = Book.objects.filter(is_early_release=True, is_available=True)
    elif category_name == 'trending':
        books = Book.objects.filter(is_available=True).order_by('-popularity_score')  # Assuming trending by popularity
    elif category_name == 'fiction':
        books = Book.objects.filter(genres__name='Fiction', is_available=True)
    elif category_name == 'nonfiction':
        books = Book.objects.filter(genres__name='Nonfiction', is_available=True)
    else:
        # If the category doesn't match any of the predefined categories, return empty or a message
        return JsonResponse({'error': 'Invalid category'}, status=400)

    # Prepare the response with book details
    books_data = []
    for book in books:
        books_data.append({
            'title': book.title,
            'author': book.author.name if book.author else 'Unknown',  # Assuming 'name' is a field in the Author model
            'description': book.description,
            'published_year': book.published_year,
            'isbn': book.isbn,
            'price': str(book.price),
            'rent_price': str(book.rent_price) if book.rent_price else 'N/A',
            'cover_image': book.cover_image.url if book.cover_image else None,
            'detail_page': f'/book/{book.book_id}/',  # Assuming detail pages exist for each book
            'rating': book.rating,
            'read_count': book.read_count,
            'popularity_score': str(book.popularity_score),
            'genres': [genre.name for genre in book.genres.all()]
        })
    
    return JsonResponse({'books': books_data})


# @login_required
# def buy_book(request, book_id):
#     book = get_object_or_404(Book, pk=book_id)
#     user_membership = UserMembership.objects.filter(user=request.user).first()

#     discount = 0
#     if user_membership and user_membership.is_membership_active():
#         discount = user_membership.membership_plan.discount_percentage

#     final_price = book.price * (1 - discount / 100)

#     # Process purchase logic here
#     # Example: Deduct price from user's wallet, add book to user's purchased list, etc.

#     return render(request, 'buy_success.html', {'book': book, 'final_price': final_price})

# @login_required
# def rent_book(request, book_id):
#     book = get_object_or_404(Book, pk=book_id)
#     user_membership = UserMembership.objects.filter(user=request.user).first()

#     if not user_membership or not user_membership.is_subscription_active():
#         return HttpResponseForbidden("You need an active subscription to rent books.")

#     if user_membership.membership_plan:
#         # Check access restrictions
#         if not user_membership.membership_plan.access_bestsellers and book.is_bestseller:
#             return HttpResponseForbidden("Your membership plan does not allow access to bestsellers.")
#         if not user_membership.membership_plan.access_early_releases and book.is_early_release:
#             return HttpResponseForbidden("Your membership plan does not allow access to early releases.")

#     # Check rental limit
#     rented_books_count = RentedBook.objects.filter(user=request.user, status='Rented').count()
#     if rented_books_count >= user_membership.subscription_plan.max_books_rented:
#         return HttpResponseForbidden("You have reached your rental limit.")

#     return render(request, 'rent_success.html', {'book': book})

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import User, MembershipPlan, SubscriptionPlan, UserMembership
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Address,Role
from .forms import RegistrationForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegistrationForm
from .models import UserProfile, User

def home(request):
    return render(request, 'home/Home_page.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )

            # Create address object if address details are provided
            address = None
            if form.cleaned_data.get('house_number_or_lane') or form.cleaned_data.get('city') or \
               form.cleaned_data.get('state') or form.cleaned_data.get('postal_code') or \
               form.cleaned_data.get('country'):
                address = Address.objects.create(
                    house_number_or_lane=form.cleaned_data.get('house_number_or_lane'),
                    city=form.cleaned_data.get('city'),
                    state=form.cleaned_data.get('state'),
                    postal_code=form.cleaned_data.get('postal_code'),
                    country=form.cleaned_data.get('country'),
                )

            # Create user profile with phone number and address
            UserProfile.objects.create(
                user=user,
                address=address,
                phone_number=form.cleaned_data['phone_number'],
            )

            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('home_page')


        else:
            messages.error(request, 'There were some errors in your form.')

    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

# Login View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def user_login(request):
    if request.method == 'POST':
        login_input = request.POST['login']
        password = request.POST['password']

        # Authenticate with username or email
        user = authenticate(request, username=login_input, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=login_input)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user:
            login(request, user)  # Log the user in
            messages.success(request, "Login successful!")

            # Debugging: Print user details
            print(f"Logged in user: {user.username}, is_staff: {user.is_staff}")

            # Redirect based on `is_staff` field
            if user.is_staff:
                return redirect('admin_home_page')
            else:
                return redirect('home_page')
        else:
            messages.error(request, "Invalid login credentials. Do you want to register?")
            return redirect('register')

    return render(request, "accounts/login.html")


# Logout View
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


# @login_required
# def admin_dashboard(request):
#     print(f"Admin dashboard accessed by: {request.user.username}, is_staff: {request.user.is_staff}")
#     return render(request, 'accounts/admin_home_page.html')

from catalog.models import Book, Author, Genre
def admin_home_page(request):
    # Fetch data from models
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    total_genres = Genre.objects.count()
    total_memberships = MembershipPlan.objects.count()
    total_subscriptions = SubscriptionPlan.objects.count()
    user_memberships = UserMembership.objects.select_related('user', 'membership_plan', 'subscription_plan')

    context = {
        'total_books': total_books,
        'total_authors': total_authors,
        'total_genres': total_genres,
        'total_memberships': total_memberships,
        'total_subscriptions': total_subscriptions,
        'user_memberships': user_memberships,
    }

    return render(request, 'accounts/admin_home_page.html', context)


# View to update Membership and Subscription plans
@login_required
def update_membership_and_subscription(request):
    if request.method == "POST":
        membership_plan_id = request.POST["membership_plan"]
        subscription_plan_id = request.POST["subscription_plan"]

        user_membership, created = UserMembership.objects.get_or_create(user=request.user)

        membership_plan = MembershipPlan.objects.get(id=membership_plan_id)
        subscription_plan = SubscriptionPlan.objects.get(id=subscription_plan_id)

        user_membership.membership_plan = membership_plan
        user_membership.subscription_plan = subscription_plan
        user_membership.save()

        messages.success(request, "Your membership and subscription plans have been updated.")
        return redirect("profile")  # Redirect to user profile page or any other page

    membership_plans = MembershipPlan.objects.all()
    subscription_plans = SubscriptionPlan.objects.all()

    return render(request, "update_membership_subscription.html", {
        "membership_plans": membership_plans,
        "subscription_plans": subscription_plans
    })


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MembershipPlan, SubscriptionPlan, UserMembership
from datetime import date, timedelta

@login_required
def membership_plans(request):
    plans = MembershipPlan.objects.all()
    return render(request, 'accounts/membership_plans.html', {'plans': plans})

@login_required
def subscription_plans(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'accounts/subscription_plans.html', {'plans': plans})

@login_required
def subscribe(request):
    if request.method == 'POST':
        membership_id = request.POST.get('membership_plans')
        subscription_id = request.POST.get('subscription_plans')

        membership_plan = MembershipPlan.objects.get(id=membership_id)
        subscription_plan = SubscriptionPlan.objects.get(id=subscription_id)

        user_membership, created = UserMembership.objects.get_or_create(user=request.user)
        user_membership.membership_plan = membership_plan
        user_membership.subscription_plan = subscription_plan
        user_membership.membership_start_date = date.today()
        user_membership.subscription_start_date = date.today()
        user_membership.save()

        messages.success(request, 'You have successfully subscribed!')
        return redirect('membership_plans')

    return redirect('membership_plans')

@login_required
def redirect_membership(request):
    user_membership = UserMembership.objects.filter(user=request.user).first()

    if user_membership and user_membership.is_membership_active():
        # Redirect to the membership details page
        return redirect('membership_details')
    else:
        # Redirect to the membership plans page
        return redirect('membership_plans')

@login_required
def redirect_subscription(request):
    user_subscription = UserMembership.objects.filter(user=request.user).first()

    if user_subscription and user_subscription.is_subscription_active():
        # Redirect to the subscription details page
        return redirect('subscription_details')
    else:
        # Redirect to the subscription plans page
        return redirect('subscription_plans')
    
@login_required
def membership_details(request):
    user_membership = UserMembership.objects.filter(user=request.user).first()
    return render(request, 'accounts/membership_details.html', {'user_membership': user_membership})

@login_required
def subscription_details(request):
    user_membership = UserMembership.objects.filter(user=request.user).first()
    return render(request, 'accounts/subscription_details.html', {'user_membership': user_membership})


@login_required
def rented_books(request):
    user_membership = UserMembership.objects.filter(user=request.user).first()
    
    if not user_membership or not user_membership.is_subscription_active():
        return redirect('subscription_plans')  # Redirect if no active subscription
    
    subscription_plan = user_membership.subscription_plan
    rented_books = CartItem.objects.filter(cart__user=request.user, cart__status='active', book__isnull=False)

    rented_books_details = []
    for item in rented_books:
        rented_books_details.append({
            'title': item.book.title,
            'author': item.book.author.name if item.book.author else 'Unknown',
            'rent_date': item.cart.created_at,  # Assuming cart created_at is the rental start date
            'end_date': item.cart.created_at + timedelta(days=subscription_plan.rental_period_days),
            'cover_image': item.book.cover_image.url if item.book.cover_image else None,
        })
    
    # Remaining books to rent
    rented_books_count = rented_books.count()
    remaining_books = subscription_plan.max_books_rented - rented_books_count

    return render(request, 'accounts/rented_books.html', {
        'rented_books': rented_books_details,
        'remaining_books': remaining_books
    })

from django.utils import timezone
from catalog.models import CartItem
@login_required
def return_book(request, book_id):
    cart_item = CartItem.objects.filter(cart__user=request.user, book_id=book_id, cart__status='active').first()

    if cart_item:
        # Check if rental period has passed
        user_membership = UserMembership.objects.get(user=request.user)
        subscription_plan = user_membership.subscription_plan
        rental_period_end = cart_item.cart.created_at + timedelta(days=subscription_plan.rental_period_days)

        if timezone.now() > rental_period_end:
            return JsonResponse({"error": "The rental period has ended, you cannot return this book now."}, status=400)

        # Delete the cart item (returning the book)
        cart_item.delete()
        return JsonResponse({"message": "Book successfully returned."}, status=200)
    else:
        return JsonResponse({"error": "Book not found in your rented list."}, status=404)


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

def choose_payment(request):
    """
    Render the choose payment page.
    """
    return render(request, 'accounts/choose_payment.html')

@login_required
def process_payment(request):
    if request.method == "POST":
        user = request.user
        membership_plan_name = request.POST.get("membership_plan")
        # subscription_plan_name = request.POST.get("subscription_plan")

        try:
            membership_plan = MembershipPlan.objects.get(name=membership_plan_name)
            # subscription_plan = SubscriptionPlan.objects.get(name=subscription_plan_name)
        except (MembershipPlan.DoesNotExist, SubscriptionPlan.DoesNotExist):
            # except (MembershipPlan.DoesNotExist, SubscriptionPlan.DoesNotExist):
            return render(request, "error.html", {"message": "Selected plan does not exist."})

        # Simulate payment success
        payment_success = True  # Replace this with actual payment gateway logic
        if payment_success:
            # Create or update UserMembership
            user_membership, created = UserMembership.objects.get_or_create(user=user)
            user_membership.membership_plan = membership_plan
            # user_membership.subscription_plan = subscription_plan
            user_membership.membership_start_date = date.today()
            user_membership.save()  # Generates and saves membership_id and subscription_id

            return redirect("payment_success_page")  # Redirect to success page

        return render(request, "payment_failure.html")  # Payment failed
    return render(request, "error.html", {"message": "Invalid request method"})

def payment_success(request):
    user_membership = UserMembership.objects.get(user=request.user)
    return render(request, "accounts/payment_success.html", {"user_membership": user_membership})

def payment_failure(request):
    return render(request, "accounts/payment_failure.html")

# def process_payment(request):
#     """
#     Handle payment processing and redirect based on the source page.
#     """
#     if request.method == "POST":
#         payment_method = request.POST.get("payment_method")
#         source_page = request.POST.get("source_page")  # Source page: cart, membership, or subscription

#         if not payment_method or not source_page:
#             return HttpResponse("Invalid payment request: Missing payment_method or source_page", status=400)

#         # Simulate payment processing
#         if source_page == "cart":
#             # Generate random order ID for cart
#             order_id = f"ITEM-{int.from_bytes(os.urandom(3), 'big')}"
#             request.session["order_id"] = order_id
#             # Redirect to the cart page
#             return redirect(reverse('cart_page') + f"?success=true&order_id={order_id}")
        
#         elif source_page == "membership":
#             # Generate random membership ID
#             membership_id = f"MEM-{int.from_bytes(os.urandom(3), 'big')}"
#             request.session["membership_id"] = membership_id
#             # Redirect to the membership plans page
#             return redirect(reverse('membership_plan') + f"?success=true&membership_id={membership_id}")
        
#         elif source_page == "subscription":
#             # Generate random subscription ID
#             subscription_id = f"SUB-{int.from_bytes(os.urandom(3), 'big')}"
#             request.session["subscription_id"] = subscription_id
#             # Redirect to the subscription plans page
#             return redirect(reverse('subscription_plan') + f"?success=true&subscription_id={subscription_id}")
        
#         return HttpResponse("Invalid source page", status=400)

#     return HttpResponse("Invalid payment request: Not a POST request", status=400)


def user_info_page(request):
    users = User.objects.all()
    addresses = Address.objects.all()
    user_profiles = UserProfile.objects.all()
    
    context = {
        'users': users,
        'addresses': addresses,
        'user_profiles': user_profiles,
    }
    return render(request, 'user_info_page.html', context)

# Update user details
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'User details updated successfully!')
        return redirect('user_info_page')
    
    context = {
        'user': user,
    }
    return render(request, 'update_user.html', context)

# Delete user
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('user_info_page')