from django.db import models


class Queue(models.Model):
	num_of_people = models.PositiveSmallIntegerField()

	def __str__(self):
		return f'Number of people {self.num_of_people}'
