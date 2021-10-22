from django.test import TestCase
from django.urls import reverse
from mysite.models import User
from ..apps import ControlqueueConfig

APP_NAME = ControlqueueConfig.name

class Restrict(TestCase):
	def setUp(self):
		self.my_admin_data = {
			'username': 'user_test',
			'password': '12345'
		}
		
		self.my_admin = User(username=self.my_admin_data['username'], is_staff=True, is_superuser=True)
		self.my_admin.set_password(self.my_admin_data['password'])
		self.my_admin.save()
	
	def test_get_as_anonymous_user(self):
		response = self.client.get(reverse(f'{APP_NAME}:restrict'))
		self.assertEqual(response.status_code, 302)

	def test_get_as_anonymous_user_following_redirects(self):
		response = self.client.get(reverse(f'{APP_NAME}:restrict'), follow=True)
		self.assertEqual(response.status_code, 200)

	def test_get_as_superuser(self):
		self.client.login(
			username = self.my_admin_data['username'],
			password = self.my_admin_data['password']
		)
		response = self.client.get(reverse(f'{APP_NAME}:restrict'))

		self.assertEqual(response.status_code, 200)


class NoticeAdminOnly(TestCase):
	def setUp(self):
		self.my_admin_data = {
			'username': 'user_test',
			'password': '12345'
		}
		
		self.my_admin = User(username=self.my_admin_data['username'], is_staff=True, is_superuser=True)
		self.my_admin.set_password(self.my_admin_data['password'])
		self.my_admin.save()
	
	def test_get_as_anonymous_user(self):
		response = self.client.get(reverse(f'{APP_NAME}:notice_admin_only'))
		self.assertEqual(response.status_code, 200)

	def test_get_as_superuser(self):
		self.client.login(
			username = self.my_admin_data['username'],
			password = self.my_admin_data['password']
		)
		response = self.client.get(reverse(f'{APP_NAME}:notice_admin_only'))

		self.assertEqual(response.status_code, 200)
