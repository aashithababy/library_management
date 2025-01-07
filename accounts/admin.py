from django.contrib import admin
from .models import MembershipPlan, SubscriptionPlan, UserMembership

@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_months', 'discount_percentage', 'access_bestsellers', 'access_early_releases','price')
    search_fields = ('name',)

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_months', 'max_books_rented', 'rent_duration_weeks','price')
    search_fields = ('name',)

@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'membership_plan', 'subscription_plan', 'membership_start_date', 'subscription_start_date')
    search_fields = ('user__username', 'membership_plan__name', 'subscription_plan__name')

from django.contrib import admin
from .models import Role, Address, UserProfile, Order, RenewalMessage, MembershipPlan, SubscriptionPlan, UserMembership

admin.site.register(Role)
admin.site.register(Address)
admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(RenewalMessage)

