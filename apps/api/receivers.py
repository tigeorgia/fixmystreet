from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.conf import settings

from .models import ChemikuchaUser


@receiver(post_save, sender=User)
def create_apiuser(sender, instance, created, **kwargs):
    if created:
        ChemikuchaUser.objects.create(user=instance)

post_save.connect(create_apiuser, sender=settings.AUTH_USER_MODEL)