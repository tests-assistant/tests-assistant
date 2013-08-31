from django.db import models

from taggit.managers import TaggableManager


class Test(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    html = models.TextField()

    tags = TaggableManager()
