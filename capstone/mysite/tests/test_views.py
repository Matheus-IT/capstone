from django.test import TestCase
from django.urls import reverse
from ..apps import MysiteConfig

from ..models import User

APP_NAME = MysiteConfig.name

from controlqueue.consumers import QueueConsumer

class Index(TestCase):
	def setUp(self):
		self.my_admin_data = {
			'username': 'test_user',
			'password': '12345'
		}
		self.my_admin = User(username=self.my_admin_data['username'], is_staff=True, is_superuser=True)
		self.my_admin.set_password(self.my_admin_data['password'])
		self.my_admin.save()

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
