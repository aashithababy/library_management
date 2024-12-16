from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:id>/', views.book_detail, name='book_detail'),
    path('add-book/', views.add_book, name='add_book'),
    path('update/<int:id>/', views.update_book, name='update_book'),
    path('confirm-add-author/', views.confirm_add_author, name='confirm_add_author'),
    path('add-author/', views.add_author, name='add_author'), 

]