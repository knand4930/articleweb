from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Main(models.Model):
    name = models.CharField(max_length=150)
    about = models.TextField()
    abouttxt = models.TextField(default="")
    news_detail = models.TextField(default="")
    twitter = models.CharField(default="-", max_length=60)
    youtube = models.CharField(default="-", max_length=60)
    facebook = models.CharField(default="-", max_length=60)
    pinterest = models.CharField(default="-", max_length=60)
    linkedin = models.CharField(default="-", max_length=60)
    tell = models.CharField(default="-", max_length=60)
    link = models.CharField(default="-", max_length=60)
    set_name = models.CharField(default="-", max_length=50)
    seo_txt = models.CharField(default="-", max_length=200)
    seo_keyword = models.TextField(default="-")
    picurl = models.TextField()
    picname = models.TextField()

    picurl2 = models.TextField()
    picname2 = models.TextField()

    picurl3 = models.TextField(default="-")
    picname3 = models.TextField(default="-")

    def __str__(self):
        return self.set_name + "|" + str(self.pk)

