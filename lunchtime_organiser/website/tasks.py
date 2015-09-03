
from __future__ import absolute_import

from celery import shared_task

from .models import *
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings

import datetime


@shared_task(name='tasks.send_buy_ticket_mail')
def send_buy_ticket_mail():

    today = datetime.date.today()

    attendee_ids = AttendedMeal.objects.filter(date=today).values_list('person__id', flat=True)

    for person_id in attendee_ids:
        lesser_meal_ticket = MealTicket.objects.filter(owner=person_id, remaining_meals__gt=0).order_by('remaining_meals').first()

        if lesser_meal_ticket.remaining_meals < 2:
            person = User.objects.get(pk=person_id)

            send_mail(
                'Out of meals',     # Subject
                'You are nearly out of tickets',     # Message
                getattr(settings, 'SENDER_ADDRESS', ''),     # From
                [person.email],     # Recipient list
            )

            print 'Mail sent to %s %s' % (person.first_name, person.last_name)


@shared_task(name='tasks.substract_remaining_meals')
def substract_remaining_meals():

    today = datetime.date.today()

    attendee_ids = AttendedMeal.objects.filter(date=today).values_list('person__id', flat=True)

    for person_id in attendee_ids:
        lesser_meal_ticket = MealTicket.objects.filter(owner=person_id, remaining_meals__gt=0).order_by('remaining_meals').first()

        lesser_meal_ticket.remaining_meals = lesser_meal_ticket.remaining_meals - 1
        lesser_meal_ticket.save()

        if lesser_meal_ticket.remaining_meals == 0:
            lesser_meal_ticket.delete()
