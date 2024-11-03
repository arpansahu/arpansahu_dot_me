from django.utils import timezone

from django.db import models

# Create your models here.
from arpansahu_dot_me.models import AbstractBaseModel


class EmailsOtpRecord(AbstractBaseModel):
    class Meta:
        unique_together = ('email', 'date')

    email = models.EmailField()
    date = models.DateField(default=timezone.now)
    count = models.IntegerField(default=1)
