from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ContactForm(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    date = models.CharField(max_length=12)
    time = models.CharField(max_length=10)
    website = models.TextField()
    txt = models.TextField()






    def __str__(self):
        return self.name