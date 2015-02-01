from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError

from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone
from django.db.utils import IntegrityError
from apps.mainapp.models import Report
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

from django.db import models
import binascii
import os



class FMSUserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True, is_confirmed=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)

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


class FMSUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    username = models.CharField(_('username'), max_length=20)
    first_name = models.CharField(_('first name'), max_length=70)
    last_name = models.CharField(_('last name'), max_length=70)
    phone = models.CharField(_('phone'), max_length=255)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_councillor = models.BooleanField(_('councillor'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_confirmed = models.BooleanField(_('email confirmed'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    USERNAME_ALLOWED_CHARS_REGEX = '^[\w\d_]+$'

    objects = FMSUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @classmethod
    def username_exists(cls, username):
        try:
            cls.objects.get(username=username)
            return True
        except cls.DoesNotExist:
            return False

    @classmethod
    def get_user_by_email(cls, email):
        try:
            user = cls.objects.get(email=email)
            return user
        except cls.DoesNotExist:
            return False

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=settings.EMAIL_FROM_USER, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email,], **kwargs)

    def __unicode__(self):
        return " ".join([self.first_name, self.email])


class FMSSettings(models.Model):
    LANGUAGE_CHOICES = (
        ('ka', _('Georgian')),
        ('en', _('English'))
    )  # ISO 639-1

    user = models.OneToOneField(FMSUser, primary_key=True, related_name='user_settings')
    language = models.CharField(_('language'), max_length=2, choices=LANGUAGE_CHOICES, default='ka')


class AbstractToken(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self._generate_token()
        super(AbstractToken, self).save(*args, **kwargs)

    @staticmethod
    def _generate_token():
        return binascii.hexlify(os.urandom(20)).decode()

    def generate_new(self):
        self.token = self._generate_token()
        return self


class FMSUserToken(AbstractToken):
    user = models.OneToOneField(FMSUser, related_name='fms_user_token')
    token = models.CharField(max_length=40, unique=True, primary_key=True)
    created_at = models.DateTimeField(_('created at'), auto_now=True)

    def get_absolute_url(self):
        url = ''.join(settings.SITE_URL + str(reverse_lazy('users:confirm', kwargs={'token': self.token})))
        return url


class FMSPasswordResetToken(AbstractToken):
    user = models.ForeignKey(FMSUser, related_name='password_reset_token')
    token = models.CharField(max_length=40, unique=True, primary_key=True)
    created_at = models.DateTimeField(_('created at'), auto_now=True)
    ip = models.GenericIPAddressField(null=True)
    used = models.BooleanField(default=False)
    used_ip = models.GenericIPAddressField(help_text="IP of request which used the token", null=True)

    def get_absolute_url(self):
        url = ''.join(settings.SITE_URL + str(reverse_lazy('users:reset_confirm', kwargs={'token': self.token})))
        return url

    @classmethod
    def get_unused_token(cls, user):
        try:
            token = cls.objects.filter(user=user, used=False).latest('created_at')
            return token
        except cls.DoesNotExist:
            return None

from .receivers import *