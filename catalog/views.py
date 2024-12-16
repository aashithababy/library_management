from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Author
from .forms import BookForm,AuthorForm
from django.http import HttpResponseForbidden
from django.contrib import messages

# List all available books
def book_list(request):
    books = Book.objects.filter(is_available=True)
    return render(request, 'catalog/book_list.html', {'books': books})

# View details of a specific book
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'catalog/book_detail.html', {'book': book})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully!")
            return redirect('admin:catalog_book_changelist')
    else:
        form = BookForm()
    
    return render(request, 'catalog/add_book.html', {'form': form})


@login_required
def confirm_add_author(request):
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        action = request.POST.get('action')
        
        if action == 'yes' and author_name:
            # Create and save the new author
            Author.objects.create(name=author_name)
            messages.success(request, f"New author '{author_name}' added successfully!")
            return redirect('add_book')  # Redirect to the add book form to continue adding the book
        
        elif action == 'no':
            # Go back to the add book form
            return redirect('add_book')
    
    return redirect('add_book')  # If GET, redirect to the book add form


def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Author added successfully!')
            return redirect('add_author')  # Redirect to the same page or another page
    else:
        form = AuthorForm()

    return render(request, 'catalog/add_author.html', {'form': form})

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