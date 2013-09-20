from django.db import models
from django.core.urlresolvers import reverse

from taggit_machinetags.managers import MachineTaggableManager


class Test(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    html = models.TextField()

    tags = MachineTaggableManager()

    def get_absolute_url(self):
        return reverse('test-detail', args=(self.pk,))

    def last_runs(self):
        return self.run_set.order_by('-created_on')[:10]


class Run(models.Model):
    title = models.CharField(max_length=255)
    tests = models.ManyToManyField(Test, through='TestInstance')
    created_on = models.DateTimeField(auto_now_add=True)

    tags = MachineTaggableManager()

    class Meta:
        ordering = ('-created_on', ) 


class TestInstance(models.Model):
    test = models.ForeignKey(Test)
    run = models.ForeignKey(Run)
    success = models.BooleanField()
    comment = models.TextField(null=True, blank=True)
    html = models.TextField(null=True, blank=True)
    started_at = models.DateTimeField(null=True)
    ended_at = models.DateTimeField(null=True)
