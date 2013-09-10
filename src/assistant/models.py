from django.db import models

from taggit.managers import TaggableManager


class Test(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    html = models.TextField()

    tags = TaggableManager()

    def get_absolute_url(self):
        return '/test/detail/%s' % self.pk


class Run(models.Model):
    title = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    tests = models.ManyToManyField(Test, through='TestInstance')


class TestInstance(models.Model):
    test = models.ForeignKey(Test)
    run = models.ForeignKey(Run)
    success = models.BooleanField()

    started_at = models.DateTimeField(null=True)
    ended_at = models.DateTimeField(null=True)

    @property
    def version(self):
        return self.run.version
