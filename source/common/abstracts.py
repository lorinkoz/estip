# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from .snippets.fields import AutoSlugField


class SlugManager(models.Manager):
    
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


@python_2_unicode_compatible
class NamedModel(models.Model):

    name = models.CharField(verbose_name='nombre', max_length=512)
    slug = AutoSlugField(verbose_name='slug', max_length=512, populate_from=('name',), overwrite=True)

    objects = SlugManager()

    class Meta:
        abstract = True

    def clean(self):
        super(NamedModel, self).clean()
        self.name = self.name.strip()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.slug,)

    @property
    def html_id(self):
        return self.slug