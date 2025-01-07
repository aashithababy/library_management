from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Book

@receiver([post_save, post_delete], sender=Book)
def update_home_page(sender, instance, **kwargs):
    """
    Signal to handle updates to the home page when books are added, updated, or deleted.
    """
    # Example: Logging or triggering cache invalidation
    print(f"Book '{instance.title}' has been updated. Consider refreshing the home page.")
