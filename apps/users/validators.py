from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import FMSUser


class FMSUserValidators(object):
    def validate_passwords(self, password1, password2):
        error_messages = {
            'password_insecure': _('Password should contain at least 8 characters, 1 alpha numeric and 1 digit'),
            'not_confirmed': _("Account is not confirmed. Confirmation email has been resent")
        }
        if not password1 or not password2:
            raise ValidationError(_("Please provide the password"))
        if password1 != password2:
            raise ValidationError(_("Passwords don't match!"))
        if len(password2) < 8:
            raise ValidationError(error_messages['password_insecure'], code='password_insecure')
        if not any(char.isdigit() for char in password2):
            raise ValidationError(error_messages['password_insecure'], code='password_insecure')
        if not any(char.isalpha() for char in password2):
            raise ValidationError(error_messages['password_insecure'], code='password_insecure')

        return password2

    def validate_username(self, username):
        try:
            FMSUser.objects.get(username=username)
        except FMSUser.DoesNotExist:
            return username
        raise ValidationError(
            _("User with that username already exists."),
            code='duplicate_username',
        )