import uuid
from django.db import models
from django.contrib.auth.models import User
from catalog.models import Book,Cart

# Roles Table
class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return self.role_name


# Addresses Table
class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20,blank=True, null=True)
    country = models.CharField(max_length=255)
    house_number_or_lane = models.CharField(max_length=255, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.house_number_or_lane}, {self.city}, {self.state}, {self.country} - {self.postal_code}"


# User Profile Table
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)  # ForeignKey to Address
    phone_number = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.user.username


# Orders Table
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.user.username}"
    
# OrderItem Table
class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.book.title} - {self.quantity} pcs"


# Renewal Messages Table
class RenewalMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_date = models.DateField()
    read_status = models.BooleanField()


# Membership Plans Table
class MembershipPlan(models.Model):
    PLAN_CHOICES = [
        ('Basic', 'Basic Plan (6 months)'),
        ('Gold', 'Gold Plan (1 year)'),
        ('Platinum', 'Platinum Plan (2 years)'),
    ]
    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    duration_months = models.PositiveIntegerField()
    discount_percentage = models.PositiveIntegerField()
    access_bestsellers = models.BooleanField(default=False)
    access_early_releases = models.BooleanField(default=False)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


# Subscription Plans Table
class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('Basic', 'Basic Plan (6 months)'),
        ('Gold', 'Gold Plan (1 year)'),
        ('Platinum', 'Platinum Plan (2 years)'),
    ]
    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    duration_months = models.PositiveIntegerField()
    max_books_rented = models.PositiveIntegerField()
    rent_duration_weeks = models.PositiveIntegerField()
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

from dateutil.relativedelta import relativedelta
from datetime import date
# User Membership Table
class UserMembership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    membership_start_date = models.DateField(auto_now_add=True)
    subscription_start_date = models.DateField(null=True, blank=True)
    membership_id = models.CharField(max_length=20, unique=True, blank=True)  # MEM ID
    subscription_id = models.CharField(max_length=20, unique=True, blank=True)  # SUB ID

    def save(self, *args, **kwargs):
        if not self.membership_id:
            self.membership_id = f"MEM-{uuid.uuid4().hex[:8].upper()}"
        if not self.subscription_id:
            self.subscription_id = f"SUB-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def is_membership_active(self):
        if self.membership_plan:
            end_date = self.membership_start_date + relativedelta(months=self.membership_plan.duration_months)
            return date.today() <= end_date
        return False

    def is_subscription_active(self):
        if self.subscription_plan:
            end_date = self.subscription_start_date + relativedelta(months=self.subscription_plan.duration_months)
            return date.today() <= end_date
        return False