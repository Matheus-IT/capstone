from django.shortcuts import render


def index(request):
	return render(request, 'mysite/index.html')

def waiting_queue(request):
	from controlqueue.consumers import QueueConsumer
	
	ROOM_NAME = QueueConsumer.GROUP_NAME
	return render(request, 'mysite/waiting_queue.html', { 'room_name': ROOM_NAME })
