from typing import List
from django.test import TestCase
from django.urls import reverse

from ..models import User, UserFeedback
from controlqueue.consumers import QueueConsumer

import json
from django.contrib import auth


def URL_MORE_USER_FEEDBACKS(page_number: int):
    '''Get the url based on the page_number'''
    return reverse(
        'mysite:more_user_feedback', kwargs={'page_number': page_number}
    )


URL_INDEX = reverse('mysite:index')
URL_WAITING_QUEUE = reverse('mysite:waiting_queue')
URL_REGISTER = reverse('mysite:register')
URL_LOGIN = reverse('mysite:login')
URL_LOGOUT = reverse('mysite:logout')
# number of feedbacks per page for the index paginator
from mysite.views import FEEDBACKS_PER_PAGE


# --------------------------- Helper functions ----------------------------
def create_user(**data):
    return User.objects.create_user(**data)


def create_superuser(data):
    return User.objects.create(
        username=data['username'],
        password=data['password'],
        is_staff=True,
        is_superuser=True,
    )


def create_user_feedbacks(n_feedbacks: int, user: User) -> List[UserFeedback]:
    feedbacks = []
    for i in range(n_feedbacks):
        feedbacks.append(
            UserFeedback.objects.create(content=f'content {i}', author=user)
        )
    return feedbacks


# -------------------------------------------------------------------------


class IndexViewTests(TestCase):
    '''Tests for the index view'''

    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'username': 'test_user', 'password': '12345678'}
        cls.sample_user = create_user(**cls.user_data)

        create_user_feedbacks(10, cls.sample_user)

    def test_getting_right_number_of_feedback(self):
        '''Test template is receiving the right number of feedback objects'''
        res = self.client.get(URL_INDEX)
        num_context_feedbacks = res.context.get('user_feedbacks').count()
        self.assertEqual(num_context_feedbacks, FEEDBACKS_PER_PAGE)

    def test_getting_the_latest_feedbacks(self):
        '''Tests the template receives the latest feedbacks by creation'''
        res = self.client.get(URL_INDEX)
        latest_feedbacks_response = res.context.get('user_feedbacks')

        latest_feedbacks = UserFeedback.objects.order_by('-created_at').all()[
            :FEEDBACKS_PER_PAGE
        ]

        # Assert if the response matches with the database values
        for feedback, feedback_res in zip(
            latest_feedbacks, latest_feedbacks_response
        ):
            self.assertEqual(feedback.content, feedback_res.content)
            self.assertEqual(feedback.created_at, feedback_res.created_at)


class RegisterViewTests(TestCase):
    def setUp(self):
        self.user = dict(
            username='test_user', email='test@example.com', password='12345678'
        )

    def test_get_method_is_allowed(self):
        res = self.client.get(URL_REGISTER)
        self.assertEqual(res.status_code, 200)

    def test_put_method_is_not_allowed(self):
        payload = {'data': 'some_data'}
        res = self.client.put(URL_REGISTER, payload)
        self.assertEqual(res.status_code, 405)

    def test_patch_method_is_not_allowed(self):
        payload = {'data': 'some_data'}
        res = self.client.patch(URL_REGISTER, payload)
        self.assertEqual(res.status_code, 405)

    def test_delete_method_is_not_allowed(self):
        payload = {'data': 'some_data'}
        res = self.client.delete(URL_REGISTER, payload)
        self.assertEqual(res.status_code, 405)

    def test_user_registers_successfully(self):
        payload = {
            'username': self.user['username'],
            'email': self.user['email'],
            'password': self.user['password'],
            'confirmation': self.user['password'],
        }
        res = self.client.post(URL_REGISTER, payload, follow=True)
        self.assertEqual(res.status_code, 200)

    def test_user_do_not_receive_error_message_when_get_to_the_page(self):
        '''A user shouldn't receive an error msg when getting to the page'''
        res = self.client.get(URL_REGISTER)
        self.assertIsNone(res.context.get('error_message'))

    def test_username_is_required(self):
        payload = {
            'email': self.user['email'],
            'password': self.user['password'],
            'confirmation': self.user['password'],
        }
        res = self.client.post(URL_REGISTER, payload, follow=True)
        self.assertEqual(
            res.context.get('error_message'), 'All fields are required.'
        )

    def test_email_is_required(self):
        payload = {
            'username': self.user['username'],
            'password': self.user['password'],
            'confirmation': self.user['password'],
        }
        res = self.client.post(URL_REGISTER, payload, follow=True)
        self.assertEqual(
            res.context.get('error_message'), 'All fields are required.'
        )

    def test_password_is_required(self):
        payload = {
            'username': self.user['username'],
            'email': self.user['email'],
            'confirmation': self.user['password'],
        }
        res = self.client.post(URL_REGISTER, payload, follow=True)
        self.assertEqual(
            res.context.get('error_message'), 'All fields are required.'
        )

    def test_confirmation_is_required(self):
        payload = {
            'username': self.user['username'],
            'email': self.user['email'],
            'password': self.user['password'],
        }
        res = self.client.post(URL_REGISTER, payload, follow=True)
        self.assertEqual(
            res.context.get('error_message'), 'All fields are required.'
        )

    def test_password_with_wrong_confirmation(self):
        payload = {
            'username': self.user['username'],
            'email': self.user['email'],
            'password': self.user['password'],
            'confirmation': 'wrong_confirmation',
        }

        res = self.client.post(URL_REGISTER, payload, follow=True)
        self.assertEqual(
            res.context.get('error_message'), 'Passwords must match.'
        )

    def test_creating_user_that_already_exists(self):
        payload = {
            'username': self.user['username'],
            'email': self.user['email'],
            'password': self.user['password'],
            'confirmation': self.user['password'],
        }

        # Register user for the first time
        self.client.post(URL_REGISTER, payload, follow=True)

        # Try registering again
        res = self.client.post(URL_REGISTER, payload, follow=True)
        self.assertEqual(
            res.context.get('error_message'), 'Username already taken.'
        )


class LoginViewTests(TestCase):
    def setUp(self):
        self.test_user_data = dict(
            username='test_user', email='test@example.com', password='12345678'
        )

    def test_get_method_is_allowed(self):
        res = self.client.get(URL_LOGIN)
        self.assertEqual(res.status_code, 200)

    def test_put_method_is_not_allowed(self):
        payload = {'data': 'some_data'}
        res = self.client.put(URL_LOGIN, payload)
        self.assertEqual(res.status_code, 405)

    def test_patch_method_is_not_allowed(self):
        payload = {'data': 'some_data'}
        res = self.client.patch(URL_LOGIN, payload)
        self.assertEqual(res.status_code, 405)

    def test_delete_method_is_not_allowed(self):
        payload = {'data': 'some_data'}
        res = self.client.delete(URL_LOGIN, payload)
        self.assertEqual(res.status_code, 405)

    def test_user_login_successful(self):
        create_user(**self.test_user_data)

        payload = dict(
            username=self.test_user_data['username'],
            password=self.test_user_data['password'],
        )
        res = self.client.post(URL_LOGIN, payload)

        self.assertIsNone(res.context)  # No error message

    def test_user_is_not_authenticated_before_passing(self):
        '''Tests that the user is not authenticated before login'''
        create_user(**self.test_user_data)

        # User is really NOT logged in
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_user_do_not_receive_error_message_at_first(self):
        '''A user who gets to the login page shouldn't receive an error msg'''
        create_user(**self.test_user_data)
        res = self.client.get(URL_LOGIN)
        self.assertIsNone(res.context.get('error_message'))

    def test_user_is_really_logged_in_after_passing(self):
        '''Tests that the user who passed for this endpoint really logged in'''
        create_user(**self.test_user_data)

        payload = dict(
            username=self.test_user_data['username'],
            password=self.test_user_data['password'],
        )
        self.client.post(URL_LOGIN, payload)

        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_username_is_required(self):
        create_user(**self.test_user_data)

        payload = dict(
            password=self.test_user_data['password'],
        )
        res = self.client.post(URL_LOGIN, payload)
        self.assertIsNotNone(res.context.get('error_message'))

    def test_password_is_required(self):
        create_user(**self.test_user_data)

        payload = dict(
            username=self.test_user_data['username'],
        )
        res = self.client.post(URL_LOGIN, payload)
        self.assertIsNotNone(res.context.get('error_message'))


class LogoutViewTests(TestCase):
    def setUp(self):
        self.user = create_user(
            username='test_user', email='test@example.com', password='12345678'
        )
        self.client.force_login(self.user)

    def test_post_method_is_not_allowed(self):
        res = self.client.post(URL_LOGOUT)
        self.assertEqual(res.status_code, 405)

    def test_put_method_is_not_allowed(self):
        payload = {'data': 'some_data'}
        res = self.client.put(URL_LOGOUT, payload)
        self.assertEqual(res.status_code, 405)

    def test_patch_method_is_not_allowed(self):
        payload = {'data': 'some_data'}
        res = self.client.patch(URL_LOGOUT, payload)
        self.assertEqual(res.status_code, 405)

    def test_delete_method_is_not_allowed(self):
        payload = {'data': 'some_data'}
        res = self.client.delete(URL_LOGOUT, payload)
        self.assertEqual(res.status_code, 405)

    def test_logout_user_successfully(self):
        res = self.client.get(URL_LOGOUT, follow=True)
        self.assertEqual(res.status_code, 200)

    def test_user_is_actually_being_logged_out(self):
        # Ensure is authenticated before
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

        self.client.get(URL_LOGOUT)

        # Now it's not
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)


class GetMoreUserFeedbacksTests(TestCase):
    '''Tests for the api view that returns more user feedbacks'''

    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'username': 'test_user', 'password': '12345678'}
        cls.sample_user = create_user(**cls.user_data)

        cls.number_feedbacks_created = 5
        create_user_feedbacks(cls.number_feedbacks_created, cls.sample_user)

    def test_get_right_number_of_new_feedbacks(self):
        '''Tests if the endpoint returns the correct number of new
        feedbacks'''
        res = self.client.get(URL_MORE_USER_FEEDBACKS(page_number=1))
        data = json.loads(res.content)

        self.assertEqual(len(data['feedbacks']), FEEDBACKS_PER_PAGE)

    def test_pagination_is_working(self):
        '''Tests if the pagination is working properly'''
        res = self.client.get(URL_MORE_USER_FEEDBACKS(page_number=1))
        data = json.loads(res.content)

        self.assertEqual(len(data['feedbacks']), 3)

        # Since there are 5 feedbacks, now we expect to be returned 2
        res = self.client.get(URL_MORE_USER_FEEDBACKS(page_number=2))
        data = json.loads(res.content)

        self.assertEqual(len(data['feedbacks']), 2)

    def test_get_nonexistent_page(self):
        '''Try to get non-existing page, returns not found'''
        # Since there are just 5 posts created, there is no page number 3
        res = self.client.get(URL_MORE_USER_FEEDBACKS(page_number=3))
        data = json.loads(res.content)

        self.assertEqual(res.status_code, 404)


class WaitingQueue(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.my_admin_data = {'username': 'test_user', 'password': '12345678'}
        create_superuser(cls.my_admin_data)

    def test_get_as_anonymous_user(self):
        response = self.client.get(URL_WAITING_QUEUE)

        ROOM_NAME = response.context['room_name']
        self.assertEqual(ROOM_NAME, QueueConsumer.GROUP_NAME)
        self.assertEqual(response.status_code, 200)

    def test_get_as_superuser(self):
        self.client.login(
            username=self.my_admin_data['username'],
            password=self.my_admin_data['password'],
        )
        response = self.client.get(URL_WAITING_QUEUE)

        ROOM_NAME = response.context['room_name']
        self.assertEqual(ROOM_NAME, QueueConsumer.GROUP_NAME)
        self.assertEqual(response.status_code, 200)
