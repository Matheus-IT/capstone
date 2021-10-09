from django.urls import path

from .apps import MysiteConfig
from . import views

app_name = MysiteConfig.name

urlpatterns = [
    # --------------------------- Normal Views ------------------------------
    path('', views.index, name='index'),
    path('waiting-queue/', views.waiting_queue, name='waiting_queue'),
    path('booking-form/', views.booking_form, name='booking_form'),
    path('register', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    # ----------------------------- API URLs --------------------------------
    path(
        'more-user-feedback/<int:page_number>/',
        views.get_more_user_feedbacks,
        name='more_user_feedback',
    ),
]
