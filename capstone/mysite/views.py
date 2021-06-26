from django.shortcuts import render
from .forms import GiveFeedbackForm
from .models import UserFeedback
from django.contrib.auth import get_user_model


def index(request):
	services: list(str) = [
		{
			'title': 'Classic Cut $30 - 30minutes',
			'description': 'Relax while your barber achieves your tailored look. If you’re looking for a bald fade or if your hair is currently longer than earlobe length please book from our other options.'
		},
		{
			'title': 'Skin Fade $40 - 45minutes',
			'description': 'Also known as a bald fade or a zero fade, this service requires a little extra time. Hair is faded from skin or “0” length to your desired length on top.'
		},
		{
			'title': 'Cut & Beard Trim $48 - 45min',
			'description': 'Combination of a classic cut and beard/mustache shaping.'
		},
		
		{
			'title': 'Skin Fade & Beard Trim $55 - 1hr',
			'description': 'Combination of skin fade and beard/mustache shaping.'
		},
		{
			'title': 'Long Cut $60 - 1hr',
			'description': 'If your hair is currently past your ear lobes, this is the service for you; whether you’re keeping your long locks or chopping them off for a new look.'
		},
		{
			'title': 'Beard Trim $20 - 30min',
			'description': 'Let your barber apply their artistry to help you create the perfectly shaped beard or mustache style you envision.'
		},
		{
			'title': 'Buzz $20 - 15min',
			'description': 'Ask for a buzz cut if you\'re looking for a no-nonsense low maintenance look at a uniform length as close as you\'d like.'
		},
		{
			'title': 'Shave $33 - 30min',
			'description': 'Experience a traditional hot towel shave with a straight razor and warm shaving cream that will leave your face smooth to the touch.'
		},
		{
			'title': 'Buzz & Beard Trim $40 - 45min',
			'description': 'Combination of single length buzz cut and beard/mustache shaping. '
		},
	]

	feedback_form = GiveFeedbackForm()
	user_feedbacks = UserFeedback.objects.order_by('-created_at').all()[:3]

	return render(request, 'mysite/index.html', { 'services': services,
												  'feedback_form': feedback_form,
												  'user_feedbacks': user_feedbacks })


def waiting_queue(request):
	from controlqueue.consumers import QueueConsumer
	
	ROOM_NAME = QueueConsumer.GROUP_NAME
	return render(request, 'mysite/waiting_queue.html', { 'room_name': ROOM_NAME })


def booking_form(request):
	return render(request, 'mysite/bookingForm.html')
