from django.test import TestCase
from django.urls import reverse

from ..models import User, UserFeedback
from controlqueue.consumers import QueueConsumer

import json




def URL_MORE_USER_FEEDBACKS(page_number: int):
    '''Get the url based on the page_number'''
    return reverse('mysite:more_user_feedback', kwargs={
                                                    'page_number': page_number
                                                })
URL_INDEX = reverse('mysite:index')
URL_WAITING_QUEUE = reverse('mysite:waiting_queue')
# number of feedbacks per page for the index paginator
from mysite.views import FEEDBACKS_PER_PAGE



# --------------------------- Helper functions ----------------------------
def create_user(data):
    return User.objects.create(**data)

def create_superuser(data):
    return User.objects.create(username=data['username'],
                               password=data['password'],
                               is_staff=True,
                               is_superuser=True)

def create_user_feedbacks(n_feedbacks: int, user: User) -> [UserFeedback]:
    feedbacks = []
    for i in range(n_feedbacks):
        feedbacks.append(
            UserFeedback.objects.create(content=f'content {i}',
                                        author=user)
        )
    return feedbacks
# -------------------------------------------------------------------------


class IndexViewTests(TestCase):
    '''Tests for the index view'''
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            'username': 'test_user',
            'password': '12345678'
        }
        cls.sample_user = create_user(cls.user_data)

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

        latest_feedbacks = UserFeedback.objects.order_by('-created_at') \
                                               .all()[:FEEDBACKS_PER_PAGE]

        # Assert if the response matches with the database values
        for feedback, feedback_res in zip(latest_feedbacks, 
                                          latest_feedbacks_response):
            self.assertEqual(feedback.content, feedback_res.content)
            self.assertEqual(feedback.created_at, feedback_res.created_at)


class GetMoreUserFeedbacksTests(TestCase):
    '''Tests for the api view that returns more user feedbacks'''
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            'username': 'test_user',
            'password': '12345678'
        }
        cls.sample_user = create_user(cls.user_data)

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
        cls.my_admin_data = {
            'username': 'test_user',
            'password': '12345678'
        }
        create_superuser(cls.my_admin_data)

    def test_get_as_anonymous_user(self):
        response = self.client.get(URL_WAITING_QUEUE)

        ROOM_NAME = response.context['room_name']
        self.assertEqual(ROOM_NAME, QueueConsumer.GROUP_NAME)
        self.assertEqual(response.status_code, 200)

    def test_get_as_superuser(self):
        self.client.login(
            username=self.my_admin_data['username'],
            password=self.my_admin_data['password']
        )
        response = self.client.get(URL_WAITING_QUEUE)

        ROOM_NAME = response.context['room_name']
        self.assertEqual(ROOM_NAME, QueueConsumer.GROUP_NAME)
        self.assertEqual(response.status_code, 200)
