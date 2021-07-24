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
	created_at = models.DateTimeField(auto_now=True)

	def serialize(self):
		return {
			'id': self.id,
			'content': self.content,
			'author': self.author.serialize(),
			'created_at': self.created_at
		}

	def __str__(self):
		return f'Feedback: {self.content[:20]}...'
