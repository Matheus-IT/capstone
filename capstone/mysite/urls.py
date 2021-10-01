from django.urls import path

from .apps import MysiteConfig
from . import views

app_name = MysiteConfig.name

urlpatterns = [
    path('', views.index, name='index'),
    path('waitingQueue/', views.waiting_queue, name='waiting_queue'),
    path('bookingForm/', views.booking_form, name='booking_form'),
    # ----------------------------- API URLs --------------------------------
    path(
        'more-user-feedback/<int:page_number>/',
        views.get_more_user_feedbacks,
        name='more_user_feedback',
    ),
    path(
        'submit-new-feedback/',
        views.submit_new_feedback,
        name='submit_new_user_feedback',
    ),
]
