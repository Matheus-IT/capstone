from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	def serialize(self):
		return {
			'id': self.id,
			'username': self.username
		}

	def __str__(self):
		return f'User {self.username}'


class UserFeedback(models.Model):
	content = models.TextField()
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def __str__(self):
		return f'Feedback title: {self.title}'
