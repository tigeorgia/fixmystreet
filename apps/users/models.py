from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone
from django.db.utils import IntegrityError
from apps.mainapp.models import Report

from django.db import models


class FMSUserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
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
    first_name = models.CharField(_('first name'), max_length=35)
    last_name = models.CharField(_('last name'), max_length=35)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_staff = models.BooleanField(_('staff'), default=False)
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
            user = cls.objects.get(username=username)
            return True
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

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __unicode__(self):
        return " ".join([self.first_name, self.email])


class FMSSettings(models.Model):
    LANGUAGE_CHOICES = (
        ('ka', _('Georgian')),
        ('en', _('English'))
    )  # ISO 639-1

    user = models.OneToOneField(FMSUser, primary_key=True)
    language = models.CharField(_('language'), max_length=2, choices=LANGUAGE_CHOICES, default='ka')

