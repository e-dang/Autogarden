from .models import Garden, Token

from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Garden)
def add_token(sender, instance, created=False, **kwargs):
    if created:
        Token.objects.create(garden=instance)
