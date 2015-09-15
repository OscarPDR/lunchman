
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect

from .forms import LoginForm
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


###     ordinary_attendance()
####################################################################################################

@login_required
def ordinary_attendance(request):
    attended_meal, created = AttendedMeal.objects.get_or_create(
        person=request.user,
        date=datetime.date.today(),
    )

    attended_meal.preferred_time = u'ordinary'
    attended_meal.save()

    return redirect('home')


###     delay_attendance()
####################################################################################################

@login_required
def delay_attendance(request):
    delayed_meal, created = AttendedMeal.objects.get_or_create(
        person=request.user,
        date=datetime.date.today(),
    )

    delayed_meal.preferred_time = u'delayed'
    delayed_meal.save()

    return redirect('home')


###     cancel_attendance()
####################################################################################################

@login_required
def cancel_attendance(request):
    cancelled_meal, created = AttendedMeal.objects.get_or_create(
        person=request.user,
        date=datetime.date.today(),
    )

    cancelled_meal.preferred_time = u'non-attending'
    cancelled_meal.save()

    return redirect('home')


###     new_meal_ticket()
####################################################################################################

@login_required
def new_meal_ticket(request):
    MealTicket(
        owner=request.user,
        purchased=datetime.date.today(),

    ).save()

    return redirect('home')
