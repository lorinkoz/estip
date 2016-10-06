# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Trace(models.Model):

	timestamp = models.DateTimeField(verbose_name='marca de tiempo', auto_now_add=True)
	ref_user = models.ForeignKey('users.User', verbose_name='usuario de referencia', on_delete=models.SET_NULL, blank=True, null=True, related_name='traces')

	message = models.CharField(verbose_name='mensaje', max_length=1024)
	details = models.TextField(verbose_name='detalles', blank=True)

	class Meta:
		verbose_name = 'traza'
		verbose_name_plural = 'trazas'
		ordering = ('-timestamp',)

	def __str__(self):
		return '[{}] {}'.format(self.timestamp, self.message)

	def clean(self):
		self.message = self.message.strip()
		self.details = self.details.strip()

	@staticmethod
	def log(message, user=None, details=''):
		return Trace.objects.create(message=message, ref_user=user, details=details)