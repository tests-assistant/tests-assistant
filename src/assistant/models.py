from django.db import models

from taggit.managers import TaggableManager


class Test(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    html = models.TextField()

    tags = TaggableManager()

    def get_absolute_url(self):
        return '/test/detail/%s' % self.pk
