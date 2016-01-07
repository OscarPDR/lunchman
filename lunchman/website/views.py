
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.shortcuts import render, redirect
from django_ajax.decorators import ajax

from .forms import LoginForm, UserSettingsForm
from .models import *

import datetime


def get_or_none(model, *args, **kwargs):

    try:
        return model.objects.get(*args, **kwargs)

    except model.DoesNotExist:
        return None


###     home()
####################################################################################################

def home(request):

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if (user is not None) and (user.is_active):
                login(request, user)

    else:
        form = LoginForm()

    today = datetime.date.today()

    user = request.user

    ordinary_attendance = AttendedMeal.objects.filter(date=today, preferred_time=u'ordinary').order_by('person__first_name')
    delayed_attendance = AttendedMeal.objects.filter(date=today, preferred_time=u'delayed').order_by('person__first_name')
    non_attendance = AttendedMeal.objects.filter(date=today, preferred_time=u'non-attending').order_by('person__first_name')

    confirmed_person_ids = AttendedMeal.objects.filter(date=today).values_list('person__id', flat=True)
    non_confirmed = User.objects.all().exclude(id__in=confirmed_person_ids)

    remaining_meals = MealTicket.objects.filter(owner=user.id).aggregate(total=Sum('remaining_meals'))

    monday = today - datetime.timedelta(days=today.weekday())
    tuesday = monday + datetime.timedelta(days=1)
    wednesday = monday + datetime.timedelta(days=2)
    thursday = monday + datetime.timedelta(days=3)
    friday = monday + datetime.timedelta(days=4)

    return_dict = {
        'form': form,
        'ordinary_attendance': ordinary_attendance,
        'delayed_attendance': delayed_attendance,
        'non_attendance': non_attendance,
        'non_confirmed_attendance': non_confirmed,
        'user': user,
        'remaining_meals': remaining_meals['total'],
        'monday_menu': get_or_none(Menu, date=monday),
        'tuesday_menu': get_or_none(Menu, date=tuesday),
        'wednesday_menu': get_or_none(Menu, date=wednesday),
        'thursday_menu': get_or_none(Menu, date=thursday),
        'friday_menu': get_or_none(Menu, date=friday),
        'today': today,
        'before_lunchtime': datetime.datetime.now().time() < datetime.time(13),
    }

    return render(request, 'index.html', return_dict)


###     logout_view()
####################################################################################################

def logout_view(request):
    logout(request)

    return redirect('home')


###     update_attendance(action)
####################################################################################################

@login_required
def update_attendance(request, action):
    meal, created = AttendedMeal.objects.get_or_create(
        person=request.user,
        date=datetime.date.today(),
    )

    meal.preferred_time = action
    meal.save()

    return redirect('home')


###     update_attendance_ajax()
####################################################################################################

@ajax
@login_required
def update_attendance_ajax(request):

    remaining_meals = 7     # Just needs to be > 1

    if MealTicket.objects.filter(owner=request.user.id).count() == 0:
        remaining_meals = 0

    else:
        remaining_meals_aggregate = MealTicket.objects.filter(owner=request.user.id).aggregate(total=Sum('remaining_meals'))
        remaining_meals = remaining_meals_aggregate['total']

    return {'remaining_meals': remaining_meals}


###     new_meal_ticket()
####################################################################################################

@ajax
@login_required
def new_meal_ticket(request):
    meal_ticket, created = MealTicket.objects.get_or_create(
        owner=request.user,
        purchased=datetime.date.today(),
    )

    return


###     user_settings()
####################################################################################################

@login_required
def user_settings(request):

    user = request.user
    user_settings, created = UserSettings.objects.get_or_create(user=user)
    remaining_meals_obj = MealTicket.objects.filter(owner=user.id).aggregate(total=Sum('remaining_meals'))
    remaining_meals = remaining_meals_obj['total']

    if request.method == "POST":
        form = UserSettingsForm(data=request.POST)

        if form.is_valid():

            if request.POST['username'] != u'':
                user.username = request.POST['username']

            if request.POST['first_name'] != u'':
                user.first_name = request.POST['first_name']

            if request.POST['last_name'] != u'':
                user.last_name = request.POST['last_name']

            if request.POST['email'] != u'':
                user.email = request.POST['email']

            user.save()

            user_settings.default_behaviour = request.POST['default_behaviour']
            user_settings.save()

            post_remaining_meals = request.POST['remaining_meals']

            if post_remaining_meals != remaining_meals:

                less_meal_ticket = MealTicket.objects.filter(owner=user.id, remaining_meals__gt=0).order_by('remaining_meals').first()
                less_meal_ticket.remaining_meals = post_remaining_meals
                less_meal_ticket.save()

            return redirect(reverse('user_settings'))

    else:
        form = UserSettingsForm(initial={'remaining_meals': remaining_meals})

    return_dict = {
        'default_behaviour': user_settings.default_behaviour,
        'form': form,
        'remaining_meals': remaining_meals,
        'user': user,
    }

    return render(request, 'user_settings.html', return_dict)
