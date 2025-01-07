from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('add-book/', views.add_book, name='add_book'),
    path('confirm-add-author/', views.confirm_add_author, name='confirm_add_author'),
    path('confirm-add-genre/', views.confirm_add_genre, name='confirm_add_genre'),
    path('update/<int:id>/', views.update_book, name='update_book'),
    path('add-author/', views.add_author, name='add_author'),
    path('authors/', views.author_list, name='author_list'),
    path('author/<int:id>/', views.author_detail, name='author_detail'),
    path('search-genre/', views.search_genre, name='search_genre'),
    path('search-author/', views.search_author, name='search_author'),
    path('search-author-suggestions/', views.search_author_suggestions, name='search_author_suggestions'),
    path('check-author-existence/', views.check_author_existence, name='check_author_existence'),
    path('validate-author/', views.author_validate, name='author_validate'),
    path('validate-author-name/', views.validate_author_name, name='validate_author_name'),
    path('pdf/<str:file_name>/', views.serve_pdf, name='serve_pdf'),
    path('cart/', views.cart_view, name='cart'), 
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('update_cart/', views.update_cart, name='update_cart'), 
    path('buy/<int:book_id>/', views.buy_book, name='buy_book'),
    path('rent/<int:book_id>/', views.rent_book, name='rent_book'),
   
]