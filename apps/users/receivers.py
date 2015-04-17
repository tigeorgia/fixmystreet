from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from models import FMSUser, FMSUserSettings, FMSUserAuthToken, FMSUserTempToken
from .views import TokenConfirmationView
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

import signals


@receiver(post_save, sender=FMSUserTempToken)
def token_changed(sender, instance, created, **kwargs):
    """
    Email user to confirm their email after token is changed.
    """
    url = instance.get_absolute_url()
    subject = _('Veify Email')
    message = render_to_string('users/email_confirm.txt',
                               {'user': instance.user, 'confirmation_url': url}
    )

    instance.user.email_user(subject=subject, message=message)

@receiver(pre_save, sender=FMSUser)
def generate_new_tokens(sender, instance, **kwargs):
    """
    Process data changes if email or password is changed.
    """
    try:
        old_user = FMSUser.objects.get(pk=instance.pk)
    except FMSUser.DoesNotExist:
        pass
    else:
        # Update 'user' token when email is changed
        # This will trigger email
        if not old_user.email == instance.email:
            instance.is_confirmed = False
            token = old_user.fms_user_token.generate_new()
            token.save()
        # Change auth token when password changes
        if not old_user.password == instance.password:
            instance.auth_token.save()


@receiver(post_save, sender=FMSUser)
def user_created(sender, instance, created, **kwargs):
    if created:
        FMSUserSettings.objects.create(user=instance)  # Create user settings object
        FMSUserAuthToken.objects.create(user=instance)  # Create token

@receiver(signals.user_confirmed, sender=TokenConfirmationView)
def email_councillor(sender, user, **kwargs):
    reports = user.reports.filter(is_active=True)
    for report in reports:
        report.email_councillor()
