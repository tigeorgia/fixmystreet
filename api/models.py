from django.db import models
from django.contrib.auth.models import User


class ChemikuchaUser(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    api_read = models.BooleanField(default=False)
    api_write = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.email