from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path('', views.home, name='home_page'),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
     path('admin/dashboard/', views.admin_home_page, name='admin_home_page'),
    path('redirect_membership/', views.redirect_membership, name='redirect_membership'),
    path('redirect_subscription/', views.redirect_subscription, name='redirect_subscription'),
    path('membership_plans/', views.membership_plans, name='membership_plans'),
    path('subscription_plans/', views.subscription_plans, name='subscription_plans'),
    path('membership_details/', views.membership_details, name='membership_details'),
    path('subscription_details/', views.subscription_details, name='subscription_details'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path("update-membership-subscription/", views.update_membership_and_subscription, name="update_membership_subscription"),
    path('rented-books/', views.rented_books, name='rented_books'),
    path('return-book/<int:book_id>/', views.return_book, name='return_book'),
    path('choose-payment/', views.choose_payment, name='choose_payment'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('payment_success/', views.payment_success, name='payment_success_page'),
    path('payment_failure/', views.payment_failure, name='payment_failure_page'),
    path('user-info/', views.user_info_page, name='user_info_page'),
    path('update-user/<int:user_id>/', views.update_user, name='update_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
]
