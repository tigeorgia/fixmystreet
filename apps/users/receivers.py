from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FMSUser, FMSSettings

@receiver(post_save, sender=FMSUser)
def create_settings(sender, instance, created, **kwargs):
    if created:
        FMSSettings.objects.create(user=instance)