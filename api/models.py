from django.db import models
from django.contrib.auth.models import User


class ApiUser(models.Model):
    user = models.OneToOneField(User)
    api_read = models.BooleanField(default=False)
    api_write = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.email