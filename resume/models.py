# models.py
from django.db import models
from arpansahu_dot_me.models import AbstractBaseModel

class Resume(AbstractBaseModel):
    file = models.FileField(upload_to='pdfs/')
    
    def __str__(self):
        return self.file.name