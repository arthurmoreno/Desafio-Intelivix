from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Urls(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    short_id = models.SlugField(max_length=6, primary_key=True)
    http_url = models.URLField(max_length=200)
    pub_date = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)
