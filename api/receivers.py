from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import ApiUser


@receiver(post_save, sender=User)
def create_apiuser(sender, instance, created, **kwargs):
    if created:
        ApiUser.objects.create(user=instance)
