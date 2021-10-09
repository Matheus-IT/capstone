import json

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.paginator import EmptyPage, Paginator
from django.core.serializers import serialize
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .forms import GiveFeedbackForm
from .models import UserFeedback
from django.views.decorators.http import (
    require_GET,
    require_POST,
    require_http_methods,
)

# number of feedbacks per page for the index paginator
FEEDBACKS_PER_PAGE = 3


# --------------------------- Helper functions ----------------------------
def hasmethod(obj, method: str):
    '''Return True if an obj has an attribute, if not, raise AttributeError'''
    return callable(getattr(obj, method))


def serialize_queryset(queryset):
    '''Return a list of serialized objects'''
    serialized = []

    for obj in queryset:
        if hasmethod(obj, 'serialize'):
            serialized.append(obj.serialize())
    return serialized


def were_all_fields_passed(fields: dict):
    for field_value in fields.values():
        if not field_value:
            return False
    return True


def password_matches_confirmation(fields: dict):
    return fields['password'] == fields['confirmation']


# -------------------------------------------------------------------------


def index(request):
    services: list(str) = [
        {
            'title': 'Classic Cut $30 - 30minutes',
            'description': 'Relax while your barber achieves your tailored look. If you’re looking for a bald fade or if your hair is currently longer than earlobe length please book from our other options.',
        },
        {
            'title': 'Skin Fade $40 - 45minutes',
            'description': 'Also known as a bald fade or a zero fade, this service requires a little extra time. Hair is faded from skin or “0” length to your desired length on top.',
        },
        {
            'title': 'Cut & Beard Trim $48 - 45min',
            'description': 'Combination of a classic cut and beard/mustache shaping.',
        },
        {
            'title': 'Skin Fade & Beard Trim $55 - 1hr',
            'description': 'Combination of skin fade and beard/mustache shaping.',
        },
        {
            'title': 'Long Cut $60 - 1hr',
            'description': 'If your hair is currently past your ear lobes, this is the service for you; whether you’re keeping your long locks or chopping them off for a new look.',
        },
        {
            'title': 'Beard Trim $20 - 30min',
            'description': 'Let your barber apply their artistry to help you create the perfectly shaped beard or mustache style you envision.',
        },
        {
            'title': 'Buzz $20 - 15min',
            'description': 'Ask for a buzz cut if you\'re looking for a no-nonsense low maintenance look at a uniform length as close as you\'d like.',
        },
        {
            'title': 'Shave $33 - 30min',
            'description': 'Experience a traditional hot towel shave with a straight razor and warm shaving cream that will leave your face smooth to the touch.',
        },
        {
            'title': 'Buzz & Beard Trim $40 - 45min',
            'description': 'Combination of single length buzz cut and beard/mustache shaping. ',
        },
    ]

    form = GiveFeedbackForm()
    feedbacks = UserFeedback.objects.order_by('-created_at')[
        :FEEDBACKS_PER_PAGE
    ]

    return render(
        request,
        'mysite/index.html',
        {
            'services': services,
            'feedback_form': form,
            'user_feedbacks': feedbacks,
        },
    )


def get_more_user_feedbacks(request, page_number):
    '''Returns more user feedbacks using pagination'''
    user_feedbacks = UserFeedback.objects.order_by('-created_at')
    paginator = Paginator(user_feedbacks, FEEDBACKS_PER_PAGE)

    try:
        page = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({'msg': 'This page does\'t exist'}, status=404)

    serialized_feedbacks = serialize_queryset(page.object_list)

    return JsonResponse({'feedbacks': serialized_feedbacks}, status=200)


def waiting_queue(request):
    from controlqueue.consumers import QueueConsumer

    ROOM_NAME = QueueConsumer.GROUP_NAME
    return render(
        request, 'mysite/waiting_queue.html', {'room_name': ROOM_NAME}
    )


def booking_form(request):
    return render(request, 'mysite/bookingForm.html')


@require_http_methods(["GET", "POST"])
def register(request):
    TEMPLATE_PATH = 'mysite/register.html'

    if request.method == 'GET':
        return render(request, TEMPLATE_PATH)

    fields = dict(
        username=request.POST.get('username'),
        email=request.POST.get('email'),
        password=request.POST.get('password'),
        confirmation=request.POST.get('confirmation'),
    )

    if not were_all_fields_passed(fields):
        return render(
            request,
            TEMPLATE_PATH,
            {'error_message': 'All fields are required.'},
        )

    if not password_matches_confirmation(fields):
        return render(
            request,
            TEMPLATE_PATH,
            {'error_message': 'Passwords must match.'},
        )

    # Attempt to create new user
    try:
        user = get_user_model().objects.create_user(
            fields['username'], fields['email'], fields['password']
        )
        user.save()
    except IntegrityError:
        return render(
            request,
            TEMPLATE_PATH,
            {'error_message': 'Username already taken.'},
        )

    login(request, user)
    return HttpResponseRedirect(reverse('mysite:index'))


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'GET':
        return render(request, 'mysite/login.html')

    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)

    # Check if authentication successful
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("mysite:index"))
    else:
        return render(
            request,
            "mysite/login.html",
            {"error_message": "Invalid username and/or password."},
        )


@require_GET
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('mysite:index'))
