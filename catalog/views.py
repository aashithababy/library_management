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
        author_name = request.POST.get('authors_name')
        
        if form.is_valid():
            # Check if the author exists
            try:
                author = Author.objects.get(name=author_name)
            except Author.DoesNotExist:
                # Ask the admin if they want to add the new author
                request.session['new_author_name'] = author_name
                return redirect('confirm_add_author')
            
            # Save the book with the existing author
            book = form.save(commit=False)
            book.author = author
            book.save()
            messages.success(request, "Book added successfully!")
            return redirect('admin:catalog_book_changelist')
    else:
        form = BookForm()
    
    return render(request, 'catalog/add_book.html', {'form': form})

@login_required
def confirm_add_author(request):
    new_author_name = request.session.get('new_author_name')

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'yes' and new_author_name:
            Author.objects.create(name=new_author_name)
            messages.success(request, f"New author '{new_author_name}' added successfully!")
            return redirect('add_book')
        elif action == 'no':
            messages.info(request, "Book addition cancelled.")
            return redirect('add_book')
    
    return render(request, 'catalog/confirm_add_author.html', {'author_name': new_author_name})

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

from django.http import JsonResponse

def search_author(request):
    author_name = request.GET.get('name')
    exists = Author.objects.filter(name=author_name).exists()
    return JsonResponse({'exists': exists})