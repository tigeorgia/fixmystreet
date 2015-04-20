from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import FMSUser


class FMSUserValidators(object):

    def __init__(self):
        self.raised = []
        self.errors = {
            'not_provided': _('Please provide the password'),
            'no_match': _("Passwords don't match!"),
            'password_insecure': _('Password should contain at least 8 characters, 1 alpha numeric and 1 digit'),
            'not_confirmed': _("Account is not confirmed. Confirmation email has been resent"),
            'duplicate_username': _("User with that username already exists."),
            'duplicate_email': _("User with provided email is already registered."),
        }

    def add_error(self, code):
        if code not in self.raised:
            self.raised.append(code)

    def validate(self, **kwargs):
        self.validate_username(kwargs.get('username'))
        self.validate_passwords(kwargs.get('password1'), kwargs.get('password2'))
        self.validate_email(kwargs.get('email'))
        self.finish()

    def validate_passwords(self, password1, password2):
        if not password1 or not password2:
            self.add_error('not_provided')
        else:
            if password1 != password2:
                self.add_error('no_match')
            if len(password2) < 8:
                self.add_error('password_insecure')
            if not any(char.isdigit() for char in password2):
                self.add_error('password_insecure')
            if not any(char.isalpha() for char in password2):
                self.add_error('password_insecure')

    def validate_username(self, username):
        try:
            FMSUser.objects.get(username=username)
        except FMSUser.DoesNotExist:
            return username
        self.add_error('duplicate_username')

    def validate_email(self, email):
        try:
            FMSUser.objects.get(email=email)
        except FMSUser.DoesNotExist:
            return email
        self.add_error('duplicate_email')

    def validation_error_list(self):
        return [ValidationError(self.errors[code], code=code) for code in self.raised]

    def finish(self):
        if self.raised:
            errors = self.validation_error_list()
            raise ValidationError(errors)