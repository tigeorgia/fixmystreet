from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.tokens import default_token_generator

from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from django.core.mail import send_mail
from django.utils import timezone
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
        language = self.user_settings.language or translation.get_language()
        translation.activate(language)
        send_mail(subject, message, from_email, [self.email,], **kwargs)

    def __unicode__(self):
        return self.email


class BaseToken(models.Model):
    token = models.CharField(_('token'), max_length=255)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    @staticmethod
    def generate_token():
        return binascii.hexlify(os.urandom(20)).decode()

    def save(self, *args, **kwargs):
        self.token = self.generate_token()
        super(BaseToken, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class FMSUserTempToken(BaseToken):
    """
    Token for handling confirmations. Such as email or password reset
    """
    user = models.ForeignKey('users.FMSUser', related_name='temp_token')
    ip = models.GenericIPAddressField(null=True)
    used = models.BooleanField(default=False)
    used_ip = models.GenericIPAddressField(help_text="IP of request which used the token", null=True)

    @classmethod
    def get_or_create_token(cls, user):
        try:
            token = cls.objects.filter(user=user, used=False).latest('created_at')
            return token
        except cls.DoesNotExist:
            return cls.objects.create(user=user)

    def get_absolute_url(self):
        url = ''.join(settings.SITE_URL + str(reverse_lazy('users:confirm', kwargs={'token': self.token})))
        return url

    class Meta:
        db_table = 'users_fmsuser_temp_token'


class FMSUserAuthToken(BaseToken):
    user = models.OneToOneField('users.FMSUser', related_name='auth_token')
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    class Meta:
        db_table = 'users_fmsuser_auth_token'


class FMSUserSettings(models.Model):
    LANGUAGE_CHOICES = (
        ('ka', _('Georgian')),
        ('en', _('English'))
    )  # ISO 639-1

    user = models.OneToOneField(FMSUser, primary_key=True, related_name='user_settings')
    language = models.CharField(_('language'), max_length=2, choices=LANGUAGE_CHOICES, default='ka')

    class Meta:
        db_table = 'users_fmsuser_settings'


from .receivers import *