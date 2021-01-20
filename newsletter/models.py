from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Newsletter(models.Model):
    name = models.CharField(max_length=50)
    txt = models.CharField(max_length=50)
    status = models.IntegerField()

    def __str__(self):
        return self.txt
