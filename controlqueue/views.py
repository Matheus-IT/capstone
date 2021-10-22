from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from .consumers import QueueConsumer


def admin_user(user):
	return user.is_superuser

@user_passes_test(admin_user, login_url='controlqueue:notice_admin_only')
def restrict(request):
	ROOM_NAME = QueueConsumer.GROUP_NAME
	return render(request, 'controlqueue/restrict.html', {'room_name': ROOM_NAME})


def notice_admin_only(request):
	return render(request, 'controlqueue/noticeAdminOnly.html')
