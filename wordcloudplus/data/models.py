from __future__ import unicode_literals

from django.db import models

class Docs(models.Model):
	title = models.CharField(max_length=50)				#name of file
	file = models.FileField()							#the file itself
	
	
	def __str__(self):
		return self.title
