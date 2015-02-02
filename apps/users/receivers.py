from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from models import FMSUser, FMSSettings, FMSUserToken, FMSPasswordResetToken
from .views import TokenConfirmationView
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from datetime import datetime

import signals


@receiver(post_save, sender=FMSUserToken)
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
        current_user = FMSUser.objects.get(pk=instance.pk)
    except FMSUser.DoesNotExist:
        pass
    else:
        # Update 'user' token when email is changed
        # This will trigger email
        if not current_user.email == instance.email:
            instance.is_confirmed = False
            token = current_user.fms_user_token.generate_new()
            token.save()
        # Change rest API auth token when password changes
        if not current_user.password == instance.password:
            new_key = current_user.auth_token.generate_key()
            auth_token = Token.objects.filter(user=current_user).update(key=new_key)


@receiver(post_save, sender=FMSUser)
def user_created(sender, instance, created, **kwargs):
    if created:
        FMSSettings.objects.create(user=instance)  # Create user settings object
        FMSUserToken.objects.create(user=instance)  # Create token
        Token.objects.create(user=instance) # Create rest framework auth token

@receiver(signals.user_confirmed, sender=TokenConfirmationView)
def email_councillor(sender, user, **kwargs):
    reports = user.reports.filter(is_active=True)
    for report in reports:
        report.email_councillor()
