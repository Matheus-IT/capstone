from django.test import TestCase
from django.urls import reverse
from ..apps import MysiteConfig

from ..models import User

APP_NAME = MysiteConfig.name

from controlqueue.consumers import QueueConsumer


class Index(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.my_admin_data = {
			'username': 'test_user',
			'password': '12345'
		}
		cls.my_admin = User(username=cls.my_admin_data['username'], is_staff=True, is_superuser=True)
		cls.my_admin.set_password(cls.my_admin_data['password'])
		cls.my_admin.save()

	def test_get_as_anonymous_user(self):
		response = self.client.get(reverse(f'{APP_NAME}:index'))
		self.assertEqual(response.status_code, 200)
	
	def test_get_as_superuser(self):
		self.client.login(
			username=self.my_admin_data['username'],
			password=self.my_admin_data['password']
		)

		response = self.client.get(reverse(f'{APP_NAME}:index'))
		self.assertEqual(response.status_code, 200)


class WaitingQueue(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.my_admin_data = {
			'username': 'test_user',
			'password': '12345'
		}
		cls.my_admin = User(username=cls.my_admin_data['username'], is_staff=True, is_superuser=True)
		cls.my_admin.set_password(cls.my_admin_data['password'])
		cls.my_admin.save()

	def test_get_as_anonymous_user(self):
		response = self.client.get(reverse(f'{APP_NAME}:waiting_queue'))

		ROOM_NAME = response.context['room_name']
		self.assertEqual(ROOM_NAME, QueueConsumer.GROUP_NAME)
		self.assertEqual(response.status_code, 200)
	
	def test_get_as_superuser(self):
		self.client.login(
			username=self.my_admin_data['username'],
			password=self.my_admin_data['password']
		)
		response = self.client.get(reverse(f'{APP_NAME}:waiting_queue'))

		ROOM_NAME = response.context['room_name']
		self.assertEqual(ROOM_NAME, QueueConsumer.GROUP_NAME)
		self.assertEqual(response.status_code, 200)
