from django.shortcuts import render
from django.db.models import Q
from catalog.models import Book

def home(request):
    query = request.GET.get('q', '').strip()  # Get the search query
    search_results = []
    
    if query:
        search_results = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__name__icontains=query) |
            Q(genres__genre_name__icontains=query)
        ).distinct()
    
    # Fetch all books for the default display
    books = Book.objects.all()
    books_by_category = {
        'thriller': books.filter(genres__genre_name__iexact='Thriller'),
        'historical': books.filter(genres__genre_name__iexact='Historical'),
        'horror': books.filter(genres__genre_name__iexact='Horror'),
        'fantasy': books.filter(genres__genre_name__iexact='Fantasy'),
        'mystery': books.filter(genres__genre_name__iexact='Mystery'),
        'comic': books.filter(genres__genre_name__iexact='Comic'),
        'nonfiction': books.filter(genres__genre_name__iexact='Non-Fiction'),
    }

    # Trending books based on popularity_score
    trending = Book.objects.order_by('-popularity_score').filter(is_available=True)[:5]

    # Other featured sections
    bestsellers = books.filter(is_bestseller=True)
    early_releases = books.filter(is_early_release=True)
    fiction = books.filter(genres__genre_name__iexact='Fiction')
    nonfiction = books.filter(genres__genre_name__iexact='Non-Fiction')

    context = {
        'query': query,
        'search_results': search_results,
        'books_by_category': books_by_category,
        'bestsellers': bestsellers,
        'early_releases': early_releases,
        'trending': trending,
        'fiction': fiction,
        'nonfiction': nonfiction,
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


