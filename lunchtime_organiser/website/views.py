
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
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

    today = datetime.date.today()

    user = request.user

    attendee_ids = []

    ordinary_attendance = AttendedMeal.objects.filter(date=today, preferred_time=u'ordinary').order_by('person__first_name')
    delayed_attendance = AttendedMeal.objects.filter(date=today, preferred_time=u'delayed').order_by('person__first_name')

    for attendance_item in ordinary_attendance:
        attendee_ids.append(attendance_item.person.id)

    for attendance_item in delayed_attendance:
        attendee_ids.append(attendance_item.person.id)

    non_confirmed_attendance = User.objects.exclude(id__in=attendee_ids).order_by('first_name')

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if (user is not None) and (user.is_active):
                login(request, user)

            else:
                # contact admin to add user
                pass

    else:
        form = LoginForm()

    try:
        meal_ticket = MealTicket.objects.filter(owner=user.id).order_by('purchased').first()

    except ObjectDoesNotExist:
        meal_ticket = None

    monday = today - datetime.timedelta(days=today.weekday())
    tuesday = monday + datetime.timedelta(days=1)
    wednesday = monday + datetime.timedelta(days=2)
    thursday = monday + datetime.timedelta(days=3)
    friday = monday + datetime.timedelta(days=4)

    return_dict = {
        'form': form,
        'ordinary_attendance': ordinary_attendance,
        'delayed_attendance': delayed_attendance,
        'non_confirmed_attendance': non_confirmed_attendance,
        'user': user,
        'meal_ticket': meal_ticket,
        'monday_menu': get_or_none(Menu, date=monday),
        'tuesday_menu': get_or_none(Menu, date=tuesday),
        'wednesday_menu': get_or_none(Menu, date=wednesday),
        'thursday_menu': get_or_none(Menu, date=thursday),
        'friday_menu': get_or_none(Menu, date=friday),
        'today': today,
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
        date=date.today(),
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
        date=date.today(),
    )

    delayed_meal.preferred_time = u'delayed'
    delayed_meal.save()

    return redirect('home')


###     cancel_attendance()
####################################################################################################

@login_required
def cancel_attendance(request):
    AttendedMeal.objects.get(
        person=request.user,
        date=date.today(),
    ).delete()

    return redirect('home')


###     new_meal_ticket()
####################################################################################################

@login_required
def new_meal_ticket(request):
    MealTicket(
        owner=request.user,
        purchased=date.today(),

    ).save()

    return redirect('home')
