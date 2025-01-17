import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from catalog.models import Book
from .models import OrderItem, UserMembership
from django.http import HttpResponseForbidden

from django.shortcuts import render

from catalog.models import Book
from .models import UserProfile, UserMembership, Address
from django.contrib.auth.models import User

from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserProfile, UserMembership


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
from .forms import AddressForm, RegistrationForm, UserProfileForm

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

def generate_invoice(order):
    # Example invoice generation logic
    Invoice.objects.create(order=order, amount=order.total_amount)

from django.utils.timezone import now
import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from catalog.models import Cart, CartItem

@login_required
def process_payment(request):
    if request.method == "POST":
        user = request.user
        source_page = request.POST.get("source_page")
        payment_method = request.POST.get("payment_method")

        try:
            # ✅ Fetch the active cart for the user
            cart = Cart.objects.get(user=user, status='active')
            cart_items = CartItem.objects.filter(cart=cart)
            total_amount = sum(item.book.price * item.quantity for item in cart_items)
        except Cart.DoesNotExist:
            return render(request, "error.html", {"message": "No active cart found."})

        # ✅ Simulating payment success (Replace with actual payment gateway)
        payment_success = True  

        if payment_success:
            # ✅ Create an order record and save the payment method
            order = Order.objects.create(
                user=user,
                order_date=now().date(),
                total_amount=total_amount,
                payment_method=payment_method  # Save the payment method here
            )

            # ✅ Move cart items to order and clear the cart
            for item in cart_items:
                order_item = OrderItem(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    price=item.book.price,
                    cart=cart  # Ensure cart is set here
                )
                order_item.save()

            # ✅ Mark the cart as completed
            cart.status = "completed"
            cart.save()

            # ✅ Generate invoice including order items
            invoice_data = f"""
            Invoice for Order ID: {order.order_id}
            User: {user.username}
            Order Date: {order.order_date}
            Total Amount: Rs. {total_amount}
            Payment Method: {payment_method}

            Items Purchased:
            """

            # ✅ List all order items and prices in the invoice
            for item in cart_items:
                invoice_data += (
                    f"{item.book.title} - Rs. {item.book.price} x {item.quantity} = Rs. {item.book.price * item.quantity}\n"
                )

            invoice_data += f"\nGrand Total: Rs. {total_amount}"

            # ✅ Save the invoice as a .txt file
            invoice_path = f"media/invoices/invoice_{order.order_id}.txt"
            os.makedirs(os.path.dirname(invoice_path), exist_ok=True)
            with open(invoice_path, "w") as file:
                file.write(invoice_data)

            # ✅ Redirect to the success page and pass the order ID
            return redirect("payment_success_page", order_id=order.order_id)

        # ✅ Payment failure scenario
        return render(request, "accounts/payment_failure.html")

    # ✅ Invalid request method handling
    return render(request, "error.html", {"message": "Invalid request method"})


@login_required
def payment_success(request, order_id):
    try:
        # ✅ Fetch the order and order items using the correct primary key
        order = Order.objects.get(order_id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)  # Fetch order items directly
    except Order.DoesNotExist:
        return render(request, "error.html", {"message": "Order not found."})

    # ✅ Pass the order and order items to the template, including the payment method
    return render(request, "accounts/payment_success.html", {
        "order": order,
        "order_items": order_items,
        "payment_method": order.payment_method  # Fetch the payment method dynamically from the order
    })

def payment_failure(request):
    return render(request, "accounts/payment_failure.html")

def view_order_details(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'accounts/order_details.html', {'order': order, 'order_items': order_items})

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


def user_info_page(request):
    # Use select_related to optimize fetching related data (userprofile, usermembership)
    users = User.objects.select_related('userprofile', 'usermembership').all()

    user_data = []
    for user in users:
        # Safely retrieve profile and membership, account for None values
        user_profile = getattr(user, 'userprofile', None)  # None if no userprofile exists
        user_membership = getattr(user, 'usermembership', None)  # None if no usermembership exists
        
        # Append the data, including None for optional fields
        user_data.append({
            'user': user,
            'user_profile': user_profile,
            'user_membership': user_membership
        })

    # Debugging Output
    print("User Data:", user_data)  # Check if this shows what you expect

    # Ensure data is passed correctly to the template
    return render(request, 'user_info_page.html', {'user_data': user_data})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile, Address, UserMembership, Order
from catalog.models import Cart, CartItem, RentedBook, Book

def user_profile(request, user_id):
    # Fetch the user object using the provided user_id
    user = get_object_or_404(User, id=user_id)
    
    # Get the user profile, address, and membership information
    try:
        user_profile = UserProfile.objects.get(user=user)
        address = user_profile.address
    except UserProfile.DoesNotExist:
        user_profile = None
        address = None
    
    try:
        membership = UserMembership.objects.get(user=user)
    except UserMembership.DoesNotExist:
        membership = None

    # Fetch user's active cart and cart items
    cart = Cart.objects.filter(user=user, status='active').first()
    cart_items = CartItem.objects.filter(cart=cart) if cart else []

    # Fetch user's orders
    orders = Order.objects.filter(user=user)

    # Fetch rented books
    rented_books = RentedBook.objects.filter(user=user)

    # Fetch all books for the user
    books = Book.objects.all()

    context = {
        'user': user,
        'user_profile': user_profile,
        'address': address,
        'membership': membership,
        'cart_items': cart_items,
        'orders': orders,
        'rented_books': rented_books,
        'books': books,
    }
    
    return render(request, 'user_profile.html', context)

def edit_user_profile(request, user_id):
    # Fetch the user using the user_id
    user = get_object_or_404(User, id=user_id)

    # Get the existing user profile and address, if they exist
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=user)  # Create a new profile if it doesn't exist
    
    try:
        address = user_profile.address
    except Address.DoesNotExist:
        address = Address(user=user)  # Create a new address if it doesn't exist

    # Handle the form submission
    if request.method == 'POST':
        print("POST request received.")  # Debugging
        # Updating the User fields alongside forms
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        address_form = AddressForm(request.POST, instance=address)
            
        if user_profile_form.is_valid() and address_form.is_valid():
            print("Forms are valid. Saving data.")  # Debugging
            user.save()  # Save the updated User fields
            user_profile_form.save()
            address_form.save()
            return redirect('user_profile', user_id=user.id)
        else:
            print("Forms are not valid.")  # Debugging
            print("User Profile Errors:", user_profile_form.errors)
            print("Address Form Errors:", address_form.errors)
    else:
        # Prepopulate the forms with existing data if available
        user_profile_form = UserProfileForm(instance=user_profile)
        address_form = AddressForm(instance=address)

    context = {
        'user': user,  # Pass user data (first_name, last_name, email)
        'user_profile_form': user_profile_form,  # Pass UserProfile form for phone_number, photo
        'address_form': address_form,  # Pass Address form for address fields
    }

    return render(request, 'edit_user_profile.html', context)
